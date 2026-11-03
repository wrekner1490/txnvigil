"""
Synthetic UPI transaction simulator (PaySim-style) with injected fraud typologies.

Real bank transaction data is confidential, so - like PaySim - we simulate
realistic customer behaviour and then inject known fraud patterns on top.

Legit behaviour per customer:
  * own spending level (log-normal amounts), own activity rate, own "active hours"
  * a small set of regular payees (merchants + contacts) used most of the time
  * occasional new payees, rare big purchases, and one-off phone (device) changes
    -> these create realistic false-positive pressure

Fraud typologies injected (fraud_type column):
  ATO          account takeover: new device, burst of high-value txns to mule accounts
  MULE_FANIN   collect-request / fake-KYC scam: many victims pay the SAME mule in a short window
  VPA_TESTING  credential testing: several Rs.1-10 txns, then large txns
  APP_SCAM     authorised push payment (social engineering): victim's own device,
               one unusually large payment to a new payee - the hardest case

Realism / false-positive pressure: legit customers also pay never-seen VPAs, make
big one-off payments, send Rs.1 txns and have shopping bursts; half the mule
accounts are 'aged' (warmed up with small txns weeks earlier); 35% of ATO uses a
remote-access app on the victim's own phone, so there is no new-device signal.

Usage:
    python src/simulate.py --users 20000 --days 60 --out data/transactions.csv
"""
import argparse
import numpy as np
import pandas as pd

N_MERCHANTS = 3000
MULE_BASE = 900_000          # payee ids >= this are mule accounts
ONE_OFF_BASE = 100_000       # payee ids in [100k, 500k) are rarely-used legit VPAs (first half = small merchants)
MULE_MERCHANT_BASE = 800_000 # fake "merchant" VPAs opened by fraudsters
START = pd.Timestamp("2026-07-01")


def simulate_legit(rng, n_users, days):
    rows = []
    for u in range(n_users):
        rate = rng.lognormal(np.log(0.7), 0.6)              # txns per day
        mu = rng.normal(np.log(400), 0.7)                   # spending level
        peak = rng.normal(14, 3)                            # active hour
        n_reg = rng.integers(4, 12)
        regulars = np.where(rng.random(n_reg) < 0.75,
                            rng.integers(0, N_MERCHANTS, n_reg),
                            N_MERCHANTS + rng.integers(0, n_users, n_reg))
        reg_w = 1 / np.arange(1, n_reg + 1); reg_w /= reg_w.sum()
        device = f"D{u}_0"
        change_day = rng.integers(5, days) if rng.random() < 0.10 else None

        n = rng.poisson(rate * days)
        if n == 0:
            continue
        day = rng.integers(0, days, n)
        hour = rng.normal(peak, 3.2, n) % 24

        # shopping / bill-split bursts: a few extra txns minutes apart
        nb = rng.binomial(n, 0.04)
        if nb:
            src = rng.integers(0, n, nb)
            reps = rng.integers(1, 4, nb)
            src = np.repeat(src, reps)
            day = np.concatenate([day, day[src]])
            hour = np.concatenate([hour, (hour[src] + rng.uniform(0.01, 0.5, len(src))) % 24])
            n = len(day)
        ts = START + pd.to_timedelta(day, "D") + pd.to_timedelta(hour * 3600, "s")

        new_payee = rng.random(n) < 0.15
        payee = rng.choice(regulars, n, p=reg_w)
        r = rng.random(n)
        rand_payee = np.where(r < 0.45, rng.integers(0, N_MERCHANTS, n),
                     np.where(r < 0.65, N_MERCHANTS + rng.integers(0, n_users, n),
                              ONE_OFF_BASE + rng.integers(0, 400_000, n)))   # never-seen VPA (new shop, landlord, friend)
        payee = np.where(new_payee, rand_payee, payee)

        amount = rng.lognormal(mu, 0.8, n)
        big = rng.random(n) < 0.012                         # legit big payment (rent, fees, gadget)
        amount = np.where(big, amount * rng.uniform(4, 20, n), amount)
        payee = np.where(big & (rng.random(n) < 0.6), ONE_OFF_BASE + rng.integers(0, 400_000, n), payee)
        micro = rng.random(n) < 0.02                        # legit Rs.1-10 txns (verification, small P2P)
        amount = np.where(micro, rng.integers(1, 11, n).astype(float), amount)

        dev = np.full(n, device, dtype=object)
        if change_day is not None:
            dev[day >= change_day] = f"D{u}_1"
        if rng.random() < 0.05:                             # second device used now and then
            dev[rng.random(n) < 0.3] = f"D{u}_tab"

        for i in range(n):
            rows.append((ts[i], u, int(payee[i]), round(float(amount[i]), 2), dev[i], 0, "LEGIT"))
    return rows, None


def user_profile(df):
    g = df.groupby("user_id")
    return g["amount"].median(), g["device_id"].first()


def inject_fraud(rng, legit, n_users, days):
    med, dev = user_profile(legit)
    users = med.index.values
    rows = []
    mule_id = [MULE_BASE]

    def rand_time(lo=1):
        return START + pd.Timedelta(days=int(rng.integers(lo, days - 1)),
                                    seconds=int(rng.integers(0, 86400)))

    def mule(t):
        """Half the mules are fresh; half were 'warmed up' weeks earlier with small
        txns from random customers so they look like an ordinary, aged account."""
        mule_id[0] += 1
        m = mule_id[0] if rng.random() < 0.65 else mule_id[0] - MULE_BASE + MULE_MERCHANT_BASE
        if rng.random() < 0.5:
            for _ in range(rng.integers(5, 20)):
                tw = t - pd.Timedelta(hours=float(rng.uniform(48, 30 * 24)))
                if tw > START:
                    rows.append((tw, int(rng.choice(users)), m, round(float(rng.lognormal(np.log(300), 0.7)), 2),
                                 None, 0, "LEGIT"))
        return m

    victims = rng.choice(users, 1400, replace=False)
    ato, rest = victims[:350], victims[350:]
    testing, rest = rest[:200], rest[200:]
    app, mule_pool = rest[:400], rest[400:]

    # 1. Account takeover - stolen credentials on a new phone, OR remote-access
    #    app (AnyDesk-style) on the victim's OWN phone (no new-device signal)
    for u in ato:
        t = rand_time()
        if rng.random() < 0.45:
            t = t.normalize() + pd.Timedelta(hours=float(rng.uniform(0, 5)))
        m = mule(t)
        d = dev[u] if rng.random() < 0.35 else f"FRAUD_DEV_{u}"
        for k in range(rng.integers(2, 6)):
            t += pd.Timedelta(minutes=float(rng.uniform(1, 15)))
            rows.append((t, u, m, round(min(med[u] * rng.uniform(2, 10), 100000), 2), d, 1, "ATO"))

    # 2. Mule fan-in campaigns: many victims of a fake-KYC / collect-request scam pay one mule over ~3 days
    vi = 0
    for c in range(45):
        t0 = rand_time(4)
        m = mule(t0)
        for _ in range(rng.integers(8, 26)):
            if vi >= len(mule_pool):
                vi = 0
            u = mule_pool[vi]; vi += 1
            t = t0 + pd.Timedelta(hours=float(rng.uniform(0, 72)))
            for _ in range(rng.integers(1, 3)):
                t += pd.Timedelta(minutes=float(rng.uniform(1, 30)))
                rows.append((t, u, m, round(float(rng.uniform(1000, 15000)), 2), dev[u], 1, "MULE_FANIN"))

    # 3. VPA / credential testing: micro txns, then cash-out
    for u in testing:
        t = rand_time()
        m = mule(t)
        d = f"FRAUD_DEV_{u}" if rng.random() < 0.5 else dev[u]
        for _ in range(rng.integers(2, 5)):
            t += pd.Timedelta(minutes=float(rng.uniform(0.5, 10)))
            rows.append((t, u, m, float(rng.integers(1, 11)), d, 1, "VPA_TESTING"))
        for _ in range(rng.integers(1, 3)):
            t += pd.Timedelta(minutes=float(rng.uniform(1, 30)))
            rows.append((t, u, m, round(min(med[u] * rng.uniform(2, 10), 100000), 2), d, 1, "VPA_TESTING"))

    # 4. Authorised push payment scam - victim's own phone, normal hours, one large payment
    for u in app:
        t = rand_time()
        t = t.normalize() + pd.Timedelta(hours=float(rng.uniform(9, 21)))
        rows.append((t, u, mule(t), round(min(med[u] * rng.uniform(3, 15), 100000), 2), dev[u], 1, "APP_SCAM"))

    out = pd.DataFrame(rows, columns=["ts", "user_id", "payee_id", "amount", "device_id", "is_fraud", "fraud_type"])
    out["device_id"] = out.device_id.fillna(out.user_id.map(dev))   # warm-up txns come from senders' own phones
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--users", type=int, default=20000)
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="data/transactions.csv")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    cols = ["ts", "user_id", "payee_id", "amount", "device_id", "is_fraud", "fraud_type"]
    legit = pd.DataFrame(simulate_legit(rng, a.users, a.days)[0], columns=cols)
    fraud = inject_fraud(rng, legit, a.users, a.days)
    df = pd.concat([legit, fraud]).sort_values("ts").reset_index(drop=True)
    df = df[df.ts < START + pd.Timedelta(days=a.days)]
    p = df.payee_id
    is_merchant = (p < N_MERCHANTS) | ((p >= ONE_OFF_BASE) & (p < ONE_OFF_BASE + 200_000)) | \
                  ((p >= MULE_MERCHANT_BASE) & (p < MULE_BASE))
    df["channel"] = np.where(is_merchant, "P2M", "P2P")
    df.insert(0, "txn_id", np.arange(len(df)))
    import os; os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    df.to_csv(a.out, index=False)
    print(f"{len(df):,} transactions | {df.is_fraud.sum():,} fraud ({df.is_fraud.mean():.3%})")
    print(df[df.is_fraud == 1].fraud_type.value_counts().to_string())


if __name__ == "__main__":
    main()
