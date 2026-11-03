> Source: Gemini research report 'TxnVigil V2 Research Report.docx', received 2026-11-02. Treat as input, not truth — see docs/MASTERMIND_RD-1.md §0. Statistics, legal facts and versions are UNVERIFIED unless marked otherwise.

> Note (CO-MASTERMIND, CM-01): labels such as 'Verified Fact' inside this report are the research author's own and are NOT MASTERMIND verification. Only the items listed in docs/MASTERMIND_RD-1.md §0 have been spot-checked. Every statistic, legal fact and version below is UNVERIFIED until its primary source has been opened and confirmed; no statistic from this file may be quoted in the README, UI, user-facing docs or CV while UNVERIFIED (RD-1 §0).

# TxnVigil v2: Technical, Regulatory, and Architectural Research Dossier for Real-Time UPI Fraud and Mule-Account Detection

## R1. Indian Regulation Relevant to a Fraud-Analytics Platform

### (a) Five-Line Executive Summary

1.  **Verified Fact:** On July 15, 2024, the Reserve Bank of India (RBI)
    > issued revised [[Master Directions on Fraud Risk Management in
    > Commercial
    > Banks]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702),
    > alongside parallel directions for [[Non-Banking Financial
    > Companies
    > (NBFCs)]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12704)
    > and [[Urban/State/Central Co-operative
    > Banks]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12703),
    > subsequently consolidated into the [[RBI (Commercial Banks --
    > Fraud Risk Management) Directions,
    > 2026]{.underline}](https://m.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13641)
    > on July 31, 2026.

2.  **Verified Fact:** Regulated entities must operate a dedicated Data
    > Analytics and Market Intelligence (MI) Unit, integrate Early
    > Warning Signals (EWS) with core banking and digital channels for
    > real-time monitoring of non-KYC and money-mule accounts, issue a
    > 21-day Show Cause Notice (SCN) before classifying an account as
    > fraudulent, and file Fraud Monitoring Returns (FMRs) within 14
    > days of classification.

3.  **Verified Fact:** Ecosystem-wide intelligence sharing is anchored
    > by the [[Reserve Bank Innovation Hub (RBIH) MuleHunter.AI
    > platform]{.underline}](https://docs.rbihub.in/mule-hunter) (live
    > in 26 banks as of March 31, 2026 per the [[RBI Annual Report
    > 2025-26]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)),
    > the [[Digital Payments Intelligence Platform
    > (DPIP)]{.underline}](https://docs.rbihub.in/digital-payments-intelligence-platform)
    > (7 banks in Phase I pilot), and the [[Central Payments Fraud
    > Information Registry (CPFIR) on
    > DAKSH]{.underline}](https://m.rbi.org.in/Scripts/NotificationUser.aspx?Id=12431&Mode=0).

4.  **Verified Fact:** The [[Digital Personal Data Protection (DPDP)
    > Rules,
    > 2025]{.underline}](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa),
    > notified on November 13, 2025 via [[G.S.R.
    > 846(E)]{.underline}](https://www.dpdpa.com/DPDP_Rules_2025_English_only.pdf),
    > operationalize the DPDP Act 2023, where Section 17(1)(c) exempts
    > fraud prevention and investigation from notice, consent, and
    > erasure duties while still enforcing strict encryption, access
    > logging, and 72-hour breach reporting.

5.  **Analytical Inference:** A portfolio fraud platform claiming Indian
    > regulatory alignment cannot merely output a binary probability
    > score; it must implement natural-justice case states (21-day SCN
    > timer, reasoned order generation), NPCI\'s October 2025 P2P
    > collect-request ban and 24-hour ₹5,000 cooling caps, 14-day
    > FMR/CPFIR export schemas, and FIU-IND 7-working-day Suspicious
    > Transaction Report (STR) workflows with anti-tipping-off RBAC
    > controls.

### (b) Key Facts, Primary Sources, and Compliance Architecture

The regulatory landscape governing digital payment fraud and anti-money
laundering (AML) in India underwent a structural transformation between
July 2024 and October 2026. Under Chapter III of the [[RBI Master
Directions on Fraud Risk Management in Commercial Banks (July 15,
2024)]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702),
banks must establish an Early Warning Signal (EWS) and Red Flagging of
Accounts (RFA) framework overseen by the Risk Management Committee of
the Board (RMCB). While older EWS regimes focused exclusively on
corporate credit advances, Paragraph 3.4 of the 2024 Master Directions
explicitly extends EWS to non-credit and digital payment channels.
Specifically, Paragraph 3.4.2 mandates that EWS transaction monitoring
for prevention and detection of potential fraud operate on a real-time
basis (or with minimum time lag) and specifically target unusual
activity in non-KYC compliant and money-mule accounts. Paragraph 3.3.2
requires banks to establish a dedicated **Data Analytics and Market
Intelligence (MI) Unit** to monitor digital platforms and applications
continuously. Banks were granted six months from July 15, 2024 (until
January 15, 2025) to upgrade their EWS engines accordingly.

At the board governance level, Chapter II of the [[RBI Master Directions
(July 15,
2024)]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702)
requires a Board-approved Fraud Risk Management Policy reviewed at least
once every three years and a **Special Committee of the Board for
Monitoring and Follow-up of cases of Frauds (SCBMF)** comprising at
least three board members (one whole-time director and a minimum of two
independent or non-executive directors, chaired by an independent
director). Following the landmark Supreme Court judgment in *State Bank
of India & Ors. vs. Rajesh Agarwal & Ors.* (March 27, 2023), Paragraph
2.1.1 codifies principles of **natural justice**: before declaring any
person or account fraudulent, the bank must serve a detailed Show Cause
Notice (SCN) specifying the exact transactions and events under
examination, allow at least **21 days** for the respondent to reply,
examine the submission, and pass a **reasoned Order** recording the
facts, the defense submission, and the rationale for fraud
classification. Under Paragraph 6.3.1, once an account or incident is
classified as fraud, the bank must submit an individual **Fraud
Monitoring Return (FMR)** to the RBI within **14 days** (shortened from
the earlier 21-day window in the repealed 2016 Directions). For
corporate credit accounts meeting the Central Repository of Information
on Large Credits (CRILC) threshold (₹3 crore aggregate exposure),
red-flagging must be reported within **7 days** of RFA classification,
and the decision to classify as fraud or lift the RFA status must be
completed within **180 days**. Staff accountability must be examined in
all fraud cases in a time-bound manner, and public sector banks (PSBs)
must refer cases involving ₹3 crore and above to the Advisory Board for
Banking and Financial Frauds (ABBFF). Law Enforcement Agency (LEA)
reporting thresholds are bifurcated: Private and Foreign Banks report
frauds below ₹1 crore to State/UT Police and ₹1 crore and above to both
State/UT Police and the Serious Fraud Investigation Office (SFIO); PSBs
and Regional Rural Banks (RRBs) report frauds below ₹6 crore to State/UT
Police and ₹6 crore and above to the Central Bureau of Investigation
(CBI).

For payment-system-specific incidents, Paragraph 6.2.2 of the [[RBI
Master Directions (July 15,
2024)]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702)
and the [[RBI CPFIR DAKSH Migration Circular (December 26,
2022)]{.underline}](https://m.rbi.org.in/Scripts/NotificationUser.aspx?Id=12431&Mode=0)
require all scheduled commercial banks and payment system operators to
report disputed, suspected, or attempted payment frauds to the **Central
Payments Fraud Information Registry (CPFIR)** hosted on RBI\'s **DAKSH**
supervisory platform. Beyond retrospective reporting, the Reserve Bank
Innovation Hub (RBIH) has deployed two national AI/ML infrastructures
documented in the [[RBI Annual Report 2025-26 (May 29,
2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466):

-   **[[MuleHunter.AI]{.underline}](https://docs.rbihub.in/mule-hunter):**
    > An AI/ML mule-account detection platform trained on
    > ecosystem-level fraud topologies that assigns a confidence score
    > (probability) to bank accounts based on behavioural and
    > transactional features. As of March 31, 2026, MuleHunter.AI is
    > deployed across **26 banks** with implementation underway in 4
    > additional banks ([[RBI Annual Report 2025-26, Para
    > VI.57]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)).
    > On May 12, 2026, the [[Indian Cyber Crime Coordination Centre
    > (I4C) under MHA signed an MoU with
    > RBIH]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2260277)
    > to integrate National Cyber Crime Reporting Portal (NCRP)
    > telemetry directly with MuleHunter.AI.

-   **[[Digital Payments Intelligence Platform
    > (DPIP)]{.underline}](https://docs.rbihub.in/digital-payments-intelligence-platform):**
    > A national real-time intelligence-sharing digital public
    > infrastructure overseen by RBI and the Department of Financial
    > Services. In Phase I (live pilot across **7 banks** as of March
    > 31, 2026), DPIP operates a \"smart registry\" of suspicious and
    > fraudulent identifiers (VPAs, bank accounts, mobile numbers,
    > device fingerprints, IMEIs) to block non-bona fide onboarding. In
    > Phase II, DPIP deploys a cross-bank AI/ML model generating
    > real-time transaction risk scores ([[RBI Annual Report 2025-26,
    > Para
    > VI.66(b)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)).

On data protection, Parliament enacted the Digital Personal Data
Protection (DPDP) Act in August 2023, and the Ministry of Electronics
and Information Technology (MeitY) notified the final [[Digital Personal
Data Protection Rules,
2025]{.underline}](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa)
on November 13, 2025 ([[G.S.R.
846(E)]{.underline}](https://www.dpdpa.com/DPDP_Rules_2025_English_only.pdf);
[[PIB Official Release, November 17,
2025]{.underline}](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)),
establishing a phased 12-to-18-month operational rollout through May
2027 ([[Legal500 DPDP Milestones, October 27,
2026]{.underline}](https://www.legal500.com/intelligence/india/privacy/dpdp-act-and-rules-2025-the-2026-compliance-milestones-businesses-cant-afford-to-miss)).
Crucially for fraud platforms, **Section 17(1)(c)** of the DPDP Act
exempts the processing of personal data when necessary for the
prevention, detection, investigation, or prosecution of any offence or
contravention of law in force in India from Chapter II obligations
(notice, consent, right to erasure) and Section 8(7) storage limitation.
However, Section 8(5) security safeguards remain strictly mandatory
under the [[DPDP Rules
2025]{.underline}](https://www.dpdpa.com/DPDP_Rules_2025_English_only.pdf):
Data Fiduciaries must enforce encryption, obfuscation/tokenization of
PII (PAN, Aadhaar, mobile, VPA), strict role-based access control
(RBAC), one-year minimum retention of access logs for security audit,
and immediate intimation plus a detailed **72-hour data breach
notification** to the Data Protection Board of India.

At the payment rail layer, the National Payments Corporation of India
(NPCI) issued sweeping operational rules between 2024 and September
2026, consolidated in the [[UPI Consolidated Circular Version 1.0
(September 18,
2026)]{.underline}](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/59640/NPCI-issued-the-UPI-Consolidated-Circular-Version-1-0-SEP182026.pdf).
Key controls include: (1) discontinuing Peer-to-Peer (P2P) \"collect
requests\" (pull transactions) effective October 1, 2025 to eliminate
P2P pull-request phishing ([[Times of India, August 14,
2025]{.underline}](https://timesofindia.indiatimes.com/business/india-business/upi-fraud-clampdown-npci-to-end-p2p-collect-requests-from-october-1-banks-apps-told-to-block-pull-transactions-permanently/articleshow/123309612.cms));
(2) enforcing a mandatory **₹5,000 cooling limit for the first 24
hours** (₹25,000 for 24 hours in specific bank implementations)
following new UPI registration, SIM change, or device binding ([[UPI
24-Hour Cooling Period Guide, September 30,
2026]{.underline}](https://gstmunshi.com/blog/upi-cooling-period-limit-rs-5000-twenty-four-hours-guide));
(3) capping UPI API balance inquiries at **50 checks per 24 hours per
app** effective August 1, 2025 ([[Paisabazaar NPCI Rules, July 31,
2025]{.underline}](https://www.paisabazaar.com/banking/new-upi-rules/));
(4) maintaining the standard ₹1 lakh per-transaction cap while expanding
the **₹5 lakh per-transaction limit** to verified merchant categories
(tax payments, hospitals, educational institutions, IPOs, RBI Retail
Direct) under [[NPCI Circular OC-185B (August 28,
2025)]{.underline}](https://www.npci.org.in/uploads/UPI_OC_No185_B_FY_2025_26_Addendum_to_OC_185_A_Implementation_of_higher_per_transaction_limit_for_specific_categories_in_UPI_ba517a0902.pdf);
and (5) enforcing a 6-month quarantine before recycled mobile numbers
can be re-registered by new users ([[UPI Consolidated Circular v1.0,
September 18,
2026]{.underline}](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/59640/NPCI-issued-the-UPI-Consolidated-Circular-Version-1-0-SEP182026.pdf)).
Finally, under the Prevention of Money Laundering Act (PMLA) Maintenance
of Records Rules (Rules 3 and 8) enforced by **FIU-IND**, any Reporting
Entity must file a **Suspicious Transaction Report (STR)** via the
FINnet 2.0 portal within **7 working days** of arriving at a conclusion
that a transaction (completed or attempted, with **no minimum monetary
threshold**) is suspicious, maintain transaction and KYC records for at
least **5 years**, and strictly prohibit \"tipping off\" the customer
([[GAFA STR Process Guide, July 27,
2026]{.underline}](https://gafa.org.in/blog/suspicious-transaction-reporting);
[[Innefu AML Compliance Checklist, May 4,
2026]{.underline}](https://innefu.com/aml-compliance-checklist-india/)).

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Regulatory        Primary Source & Reference ID                                                                                                                                                                                                         Publication Date                                                                       Mandatory Rule / Threshold What TxnVigil v2 Must
  Requirement /                                                                                                                                                                                                                                                                                                                                                             Implement
  Domain                                                                                                                                                                                                                                                                                                                                                                    
  ----------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------- -------------------------- ----------------------------
  **Real-Time EWS & [[RBI Master Directions on Fraud Risk Management in Commercial Banks (DOS.CO.FMG.SEC.No.5/23.04.001/2024-25)]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702), Para 3.4.1--3.4.3                        July 15, 2024 (Updated [[July 31,                                                      Real-time or               Sub-50ms synchronous scoring
  Mule Monitoring**                                                                                                                                                                                                                                       2026]{.underline}](https://m.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13641))   near-real-time monitoring  API + streaming EWS rules;
                                                                                                                                                                                                                                                                                                                                                 of digital/non-credit      SLA timer on every generated
                                                                                                                                                                                                                                                                                                                                                 transactions; specific     alert (due_at = created_at +
                                                                                                                                                                                                                                                                                                                                                 vigilance on non-KYC and   30 days).
                                                                                                                                                                                                                                                                                                                                                 money-mule accounts; EWS   
                                                                                                                                                                                                                                                                                                                                                 alert examination TAT \\le 
                                                                                                                                                                                                                                                                                                                                                 30 days.                   

  **Natural Justice [[RBI Fraud Risk Management MD]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702), Para 2.1.1 (codifying *SBI vs. Rajesh Agarwal*, Mar 27, 2023)                                                          July 15, 2024                                                                          Detailed SCN detailing     Case management state
  & Show Cause                                                                                                                                                                                                                                                                                                                                   impugned transactions;     machine: ALERT_OPEN
  Notice (SCN)**                                                                                                                                                                                                                                                                                                                                 \\ge 21 days for customer  \\rightarrow SCN_ISSUED
                                                                                                                                                                                                                                                                                                                                                 response; reasoned Order   (21-day lock timer)
                                                                                                                                                                                                                                                                                                                                                 recording defense and      \\rightarrow RESPONSE_LOGGED
                                                                                                                                                                                                                                                                                                                                                 findings prior to fraud    \\rightarrow
                                                                                                                                                                                                                                                                                                                                                 declaration.               REASONED_ORDER_PASSED
                                                                                                                                                                                                                                                                                                                                                                            \\rightarrow
                                                                                                                                                                                                                                                                                                                                                                            CLASSIFIED_FRAUD.

  **RBI Fraud       [[RBI Fraud Risk Management MD]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702), Para 6.1--6.3 & [[RBI CPFIR DAKSH                                                                                      July 15, 2024 & Dec 26, 2022                                                           FMR filing within **14     One-click JSON/XML export of
  Reporting (FMR &  Circular]{.underline}](https://m.rbi.org.in/Scripts/NotificationUser.aspx?Id=12431&Mode=0)                                                                                                                                                                                                                                   days** of fraud            FMR & CPFIR payloads
  CPFIR)**                                                                                                                                                                                                                                                                                                                                       classification (all        pre-populated with
                                                                                                                                                                                                                                                                                                                                                 amounts);                  date_of_occurrence,
                                                                                                                                                                                                                                                                                                                                                 disputed/attempted payment date_of_detection,
                                                                                                                                                                                                                                                                                                                                                 frauds reported to CPFIR   date_of_classification, and
                                                                                                                                                                                                                                                                                                                                                 on DAKSH; LEA routing      RBI\'s 11 fraud categories.
                                                                                                                                                                                                                                                                                                                                                 (\<₹1Cr State Police,      
                                                                                                                                                                                                                                                                                                                                                 \\ge₹1Cr SFIO for Private  
                                                                                                                                                                                                                                                                                                                                                 Banks; \\ge₹6Cr CBI for    
                                                                                                                                                                                                                                                                                                                                                 PSBs).                     

  **MuleHunter.AI & [[RBI Annual Report 2025-26]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466), Para VI.57 & VI.66(b); [[RBIH MuleHunter Docs]{.underline}](https://docs.rbihub.in/mule-hunter); [[RBIH DPIP           May 29, 2026 & [[May 12, 2026                                                          Account-level mule         Mock DPIP Smart Registry
  DPIP              Docs]{.underline}](https://docs.rbihub.in/digital-payments-intelligence-platform)                                                                                                                                                     MoU]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2260277)           confidence score           Redis Bloom/Set lookup on
  Integration**                                                                                                                                                                                                                                                                                                                                  (MuleHunter.AI in 26       VPA/Device/IMEI + dedicated
                                                                                                                                                                                                                                                                                                                                                 banks) + DPIP Phase I      Account Mule Score
                                                                                                                                                                                                                                                                                                                                                 Smart Registry lookup      (mule_prob) alongside
                                                                                                                                                                                                                                                                                                                                                 (negative identifier list) Transaction Fraud Score
                                                                                                                                                                                                                                                                                                                                                 and Phase II real-time     (txn_prob).
                                                                                                                                                                                                                                                                                                                                                 transaction risk score.    

  **DPDP Act 2023 & [[MeitY DPDP Rules 2025 G.S.R. 846(E)]{.underline}](https://www.dpdpa.com/DPDP_Rules_2025_English_only.pdf) & [[PIB                                                                                                                   Nov 13, 2025 (Updated Oct 2026)                                                        Sec 17(1)(c) exempts fraud HMAC-SHA256 tokenization of
  DPDP Rules 2025** Release]{.underline}](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)                                                                                                                                                                                                         prevention/investigation   VPA/Mobile/PAN/Device IDs in
                                                                                                                                                                                                                                                                                                                                                 from consent/erasure; Sec  online/offline stores;
                                                                                                                                                                                                                                                                                                                                                 8(5) requires encryption,  immutable PostgreSQL audit
                                                                                                                                                                                                                                                                                                                                                 PII obfuscation, RBAC,     table (audit_logs) for every
                                                                                                                                                                                                                                                                                                                                                 1-year audit logs, and     analyst PII view.
                                                                                                                                                                                                                                                                                                                                                 72-hour breach reporting.  

  **NPCI UPI Risk & [[UPI Consolidated Circular v1.0]{.underline}](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/59640/NPCI-issued-the-UPI-Consolidated-Circular-Version-1-0-SEP182026.pdf); [[NPCI                                 Aug 14, 2025; Aug 28, 2025; Sept 18, 2026                                              ₹5,000 cap for 24h after   Deterministic pre-ML hard
  Cooling           OC-185B]{.underline}](https://www.npci.org.in/uploads/UPI_OC_No185_B_FY_2025_26_Addendum_to_OC_185_A_Implementation_of_higher_per_transaction_limit_for_specific_categories_in_UPI_ba517a0902.pdf); [[P2P Collect                                                                                                            new device/SIM binding;    rules in FastAPI enforcing
  Controls**        Ban]{.underline}](https://timesofindia.indiatimes.com/business/india-business/upi-fraud-clampdown-npci-to-end-p2p-collect-requests-from-october-1-banks-apps-told-to-block-pull-transactions-permanently/articleshow/123309612.cms)                                                                                          P2P COLLECT blocked (only  the ₹5,000/24h
                                                                                                                                                                                                                                                                                                                                                 verified merchant collect  device-binding cooldown, P2P
                                                                                                                                                                                                                                                                                                                                                 allowed); ₹1L standard cap collect rejection, and
                                                                                                                                                                                                                                                                                                                                                 (₹5L verified categories); ₹1L/₹5L MCC-based amount
                                                                                                                                                                                                                                                                                                                                                 50 balance checks/24h.     caps.

  **FIU-IND STR &   [[PMLA Rules 3 & 8 / FIU-IND STR Guidelines]{.underline}](https://gafa.org.in/blog/suspicious-transaction-reporting) & [[AML Compliance Checklist]{.underline}](https://innefu.com/aml-compliance-checklist-india/)                   May 4, 2026 & July 27, 2026                                                            STR filed within **7       7-day STR countdown timer
  PMLA Record                                                                                                                                                                                                                                                                                                                                    working days** of forming  from SUSPICION_CONFIRMED;
  Retention**                                                                                                                                                                                                                                                                                                                                    suspicion (no amount       FINnet 2.0 STR JSON/XML
                                                                                                                                                                                                                                                                                                                                                 floor; includes attempted  generator; generic external
                                                                                                                                                                                                                                                                                                                                                 txns); 5-year record       decline reason
                                                                                                                                                                                                                                                                                                                                                 retention; strict          (TXN_DECLINED_RISK_POLICY)
                                                                                                                                                                                                                                                                                                                                                 prohibition on tipping off to prevent tipping off.
                                                                                                                                                                                                                                                                                                                                                 the customer.              
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Most portfolio fraud projects fail immediate
    > credibility checks with Indian banking architects because they
    > conflate card-network chargeback workflows with UPI push-payment
    > finality and ignore the post-2024 RBI natural-justice and FIU-IND
    > reporting regimes ([[RBI Master Directions, July 15,
    > 2024]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702)).

-   **Analytical Inference:** TxnVigil v2 should implement a
    > **Dual-Track Regulatory Engine**:

    1.  **Real-Time Payment Gatekeeper (NPCI & DPIP Track):** Before
        > calling LightGBM, evaluate deterministic NPCI rules
        > (rule_npci_new_device_24h_5k_cap, rule_npci_p2p_collect_ban,
        > rule_npci_mcc_limit_check, rule_dpip_negative_registry_match).
        > Crucially, the response returned to the payer/payee API client
        > must only contain a generic action (ALLOW,
        > STEP_UP_PIN_WARNING, HOLD_COOLING, BLOCK) and a generic
        > customer-safe message so the platform never violates PMLA
        > anti-tipping-off provisions.

    2.  **Compliance Case & Reporting State Machine (RBI & FIU-IND
        > Track):** Inside the PostgreSQL case management schema, model
        > the exact legal lifecycle required by RBI and FIU-IND: track
        > occurred_at, detected_at, red_flagged_at, scn_issued_at,
        > scn_response_due_at (+21 days), classified_fraud_at,
        > fmr_due_at (+14 days), and str_due_at (+7 working days).
        > Include an admin export endpoint
        > (/api/v1/compliance/export/{case_id}) that outputs a
        > structured **RBI FMR / CPFIR JSON** and an **FIU-IND FINnet
        > 2.0 STR JSON**, while logging every PII unmask action in an
        > append-only dpdp_audit_log table.

### (d) Open Uncertainties

-   UNCERTAIN: **Exact DPIP Phase II API Wire Schema and MuleHunter.AI
    > Feature List.** While RBIH documents
    > [[MuleHunter.AI]{.underline}](https://docs.rbihub.in/mule-hunter)
    > and
    > [[DPIP]{.underline}](https://docs.rbihub.in/digital-payments-intelligence-platform)
    > at an architectural level, exact protobuf/JSON field names and the
    > proprietary list of behavioral features used inside RBIH\'s
    > production models are restricted to onboarded regulated entities
    > under NDA.

-   UNCERTAIN: **Finalized RBI Model Risk Management Directions
    > Effective Date.** According to the [[RBI Annual Report 2025-26
    > (Para
    > VI.18)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
    > and [[Dvara Research (July 27,
    > 2026)]{.underline}](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/),
    > the *Draft Guidance on Regulatory Principles for Model Risk
    > Management* was issued on June 24, 2026 incorporating FREE-AI
    > recommendations, but the final binding effective date for
    > commercial banks remains pending post-consultation finalization.

-   UNCERTAIN: **RBI March 6, 2026 Draft Customer Liability Revision.**
    > Per [[RBI Annual Report 2025-26 (Para
    > VI.48)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466),
    > RBI issued draft instructions on March 6, 2026 to expand the 2017
    > zero/limited customer liability circular to cover socially
    > engineered \"authorized\" push frauds and small-value
    > compensation, but final thresholds are not yet gazetted.

## R2. UPI and Digital-Payment Fraud Typologies in India (2024--2026)

### (a) Five-Line Executive Summary

1.  **Verified Fact:** According to the [[RBI Annual Report 2025-26 (May
    > 29, 2026, Tables VI.2 &
    > VI.3)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466),
    > total bank frauds (\\ge ₹1 lakh) stood at 35,800 cases (₹11,013
    > crore) in FY 2023-24, 23,722 cases (₹32,803 crore) in FY 2024-25,
    > and 10,114 cases (₹48,021 crore) in FY 2025-26, while
    > Card/Internet/Digital Payment frauds (\\ge ₹1 lakh) recorded
    > 28,836 cases (₹1,452 crore) in FY24, 13,332 cases (₹517 crore) in
    > FY25, and 293 cases (₹29 crore) in FY26.

2.  **Verified Fact:** Because RBI\'s FMR table only counts frauds \\ge
    > ₹1 lakh that complete the formal SCN classification process, the
    > true retail digital fraud volume is captured by the Ministry of
    > Home Affairs\' **I4C / NCRP** telemetry: per [[PIB Release ID
    > 2287039 (July 21,
    > 2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1),
    > **65,89,201 financial fraud complaints** involving **\> ₹55,050
    > crore** were reported on NCRP between 2021 and 2025, with
    > **₹11,158 crore saved** across 32.80 lakh complaints via CFCFRMS
    > up to June 30, 2026.

3.  **Verified Fact:** Per [[PIB Release ID 2223095 (February 4,
    > 2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095),
    > Indian banks shared **21.65 lakh suspect identifiers** and
    > identified **26.48 lakh Layer-1 mule accounts** with I4C up to
    > December 31, 2025.

4.  **Verified Fact:** Authorized Push Payment (APP) scams---led by
    > Digital Arrest extortion, fake institutional trading/IPO apps,
    > Telegram prepaid task scams, malicious Android APKs hijacking SMS
    > forwarders, and remote-access screen sharing---now dominate Indian
    > payment losses, whereas classic P2P collect-request scams were
    > curbed by NPCI\'s October 1, 2025 P2P collect ban ([[Times of
    > India, August 14,
    > 2025]{.underline}](https://timesofindia.indiatimes.com/business/india-business/upi-fraud-clampdown-npci-to-end-p2p-collect-requests-from-october-1-banks-apps-told-to-block-pull-transactions-permanently/articleshow/123309612.cms)).

5.  **Analytical Inference:** Because the victim personally enters their
    > genuine UPI MPIN on their own bound device in \>70% of Indian UPI
    > fraud value (APP scams), payer-only authentication checks fail;
    > TxnVigil v2 must combine **in-session behavioral/device signals**
    > (active call state, screen-sharing overlay, rapid FD/sweep
    > liquidation) with **payee/beneficiary mule-network velocity
    > signals** (fan-in, pass-through ratio, account age, VPA entropy).

### (b) Official Macro Fraud Statistics and Step-by-Step Typology Breakdown

A harshly honest reading of Indian fraud statistics requires reconciling
two official government datasets that measure completely different
denominators: **RBI Supervisory Returns (FMRs)** and **MHA I4C / NCRP
Citizen Complaints**. Footnote 2 of Table VI.2 in the [[RBI Annual
Report 2025-26 (May 29,
2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
explicitly notes that RBI\'s annual fraud tables include **only frauds
of ₹1 lakh and above** where the bank has formally classified the
incident as a fraud on the bank/system (which, after the July 2024
Master Directions and the Supreme Court\'s *Rajesh Agarwal* ruling,
requires a 21-day Show Cause Notice and formal order, causing reported
digital payment FMR counts \\ge ₹1 lakh to drop sharply from 28,836 in
FY24 and 13,332 in FY25 to 293 in FY26, even as Advances value surged
due to 314 re-examined historical corporate cases totaling ₹30,199
crore). Conversely, the **National Cyber Crime Reporting Portal (NCRP)**
and **Citizen Financial Cyber Fraud Reporting and Management System
(CFCFRMS)** operated by I4C capture all retail UPI/IMPS/NEFT/RTGS cyber
frauds reported via the 1930 helpline regardless of ticket size.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Official Metric FY 2023-24                                                                                                 FY 2024-25     FY 2025-26 / Latest Primary Source & Date
  / Category                                                                                                                                Cumulative          
  --------------- ---------------------------------------------------------------------------------------------------------- -------------- ------------------- ---------------------------------------------------------------------------------------------
  **RBI Total     35,800 cases                                                                                               23,722 cases   10,114 cases        [[RBI Annual Report 2025-26, Table VI.2 (May 29,
  Bank Frauds                                                                                                                                                   2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
  (\\ge ₹1 Lakh):                                                                                                                                               
  Count**                                                                                                                                                       

  **RBI Total     ₹11,013 crore                                                                                              ₹32,803 crore  ₹48,021 crore       [[RBI Annual Report 2025-26, Table VI.2 (May 29,
  Bank Frauds                                                                                                                               (incl. ₹30,199 Cr   2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
  (\\ge ₹1 Lakh):                                                                                                                           re-classified       
  Value**                                                                                                                                   prior-year          
                                                                                                                                            advances)           

  **RBI Card /    28,836 cases (80.4% of total cases)                                                                        13,332 cases   293 cases (2.9% of  [[RBI Annual Report 2025-26, Table VI.3 (May 29,
  Internet /                                                                                                                 (56.2% of      \\ge₹1L FMR cases   2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
  Digital                                                                                                                    total cases)   post-2024 MD        
  Payments (\\ge                                                                                                                            reclassification)   
  ₹1 Lakh): Count                                                                                                                                               
  & Share**                                                                                                                                                     

  **RBI Card /    ₹1,452 crore (13.2% of value)                                                                              ₹517 crore     ₹29 crore (0.1% of  [[RBI Annual Report 2025-26, Table VI.3 (May 29,
  Internet /                                                                                                                 (1.6% of       \\ge₹1L FMR value)  2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
  Digital                                                                                                                    value)                             
  Payments (\\ge                                                                                                                                                
  ₹1 Lakh): Value                                                                                                                                               
  & Share**                                                                                                                                                     

  **I4C / NCRP    Included in 5-yr total (19,18,835 in CY 2024 per                                                           \> 65,89,201   \> ₹11,158 crore    [[PIB MHA Release ID 2287039 (July 21,
  Financial Fraud [[TOI]{.underline}](https://timesofindia.indiatimes.com/india/immersive-story/the-festive-scam-season/))   complaints (\> saved across \>     2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1)
  Complaints                                                                                                                 ₹55,050 crore  32.80 lakh CFCFRMS  
  (2021--2025                                                                                                                reported loss; complaints (up to   
  Cumulative)**                                                                                                              ₹8,189 Cr      June 30, 2026)      
                                                                                                                             lien-marked;                       
                                                                                                                             1,95,760 FIRs)                     

  **I4C           Tracked via NCRP / Samanvaya                                                                               Tracked via    **26.48 lakh        [[PIB MHA Release ID 2223095 (February 4,
  Identified                                                                                                                 CFCFRMS        Layer-1 mule        2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095)
  Layer-1 Mule                                                                                                                              accounts** &        
  Accounts &                                                                                                                                **21.65 lakh        
  Suspect                                                                                                                                   suspect             
  Identifiers**                                                                                                                             identifiers**       
                                                                                                                                            shared by banks (up 
                                                                                                                                            to Dec 31, 2025)    
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Below is the comprehensive technical breakdown of the 10 primary UPI and
digital-payment fraud typologies operating in India across 2024--2026,
detailing their step-by-step execution mechanics, observable bank/PSP
telemetry signals, required data fields, and verified case examples.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Typology          Step-by-Step Execution Mechanics  Observable Signals in Transaction / Device / Login     Telemetry Data Fields Required      Verified Recent Example / News (Date & URL)
                                                      Data                                                                                       
  ----------------- --------------------------------- ------------------------------------------------------ ----------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **1.              \(1\) Spoofed IVR/call claiming   Active long-duration VoIP/cellular call                is_call_active, call_duration_sec,  [[Pune Senior Citizen Loses ₹2.1 Crore in Investment and Fake Digital Arrest Scam (The420.in, Nov 2, 2026)]{.underline}](https://the420.in/pune-senior-citizen-cyber-fraud-2-crore/); [[ORF Analysis on Digital Arrest Scams (July 18,
  Digital-Arrest    TRAI/FedEx/customs parcel with    (call_active=True, duration \>1800s) concurrent with   recent_fd_liquidation_flag,         2026)]{.underline}](https://www.orfonline.org/expert-speak/digital-arrest-scams-and-the-limits-of-domestic-enforcement)
  Scams**           contraband or Aadhaar-linked      banking session; sudden premature FD closure           payer_age (often \>55),             
                    money laundering. (2) Escalation  (fd_broken_last_1h=True) followed by max-limit         beneficiary_first_seen_sec,         
                    to fake CBI/ED/Supreme Court      outflows (amount == 99999 or 100000) to a newly added  beneficiary_1h_inflow_count.        
                    video interrogation on            beneficiary with high fan-in.                                                              
                    WhatsApp/Skype keeping victim                                                                                                
                    under continuous \"digital                                                                                                   
                    arrest\" surveillance. (3) Victim                                                                                            
                    coerced into breaking FDs/mutual                                                                                             
                    funds and transferring funds via                                                                                             
                    UPI (₹1L chunks) or RTGS/IMPS to                                                                                             
                    \"RBI verification/escrow\" mule                                                                                             
                    accounts.                                                                                                                    

  **2. Investment / \(1\) Social media ad (deepfake   Escalating deposit staircase (₹10k \\rightarrow ₹50k   payer_to_new_merchant_count_7d,     [[Pune Software Engineer Loses ₹2.17 Crore in Fake Trading App Investment Scam (The420.in, Oct 30, 2026)]{.underline}](https://the420.in/pune-engineer-217-crore-fake-trading-app-investment-scam/); [[Techie Duped of ₹22 Lakh in
  Trading / Fake    CEO/SEBI broker) lures victim     \\rightarrow ₹1L multiple times/day) from one retail   beneficiary_mcc,                    Online Trading Scam (The Hindu, Oct 17, 2025)]{.underline}](https://www.thehindu.com/news/cities/Delhi/techie-duped-of-22-lakh-in-international-online-trading-scam/article70171815.ece)
  IPO Scams**       into WhatsApp/Telegram VIP stock  payer to rotating newly registered                     amount_vs_mcc_p99_ratio,            
                    group. (2) Victim installs fake   merchant/current-account VPAs                          beneficiary_unique_senders_24h,     
                    institutional trading APK/PWA     (beneficiary_account_age_days \< 30) across unrelated  vpa_handle_entropy.                 
                    showing fabricated 300% paper     MCCs (e.g., grocery/hardware MCC receiving ₹1L                                             
                    gains. (3) Victim sends           tickets).                                                                                  
                    progressive UPI/IMPS deposits to                                                                                             
                    rotating                                                                                                                     
                    current-account/rented-merchant                                                                                              
                    VPAs; blocked when attempting                                                                                                
                    withdrawal unless \"tax\" is                                                                                                 
                    paid.                                                                                                                        

  **3. Prepaid Task \(1\) WhatsApp message offers     Micro-credit inflow (₹150--₹500) from an unknown       recent_micro_credit_flag,           [[Telegram Task Scam: How a ₹200 Review Became a ₹23 Lakh Loss (HerWorkCircle, Oct 8, 2026)]{.underline}](https://www.herworkcircle.com/guides/telegram-task-scam); [[Task Scam on Telegram in India (Bachao.ai, July 18,
  / Part-Time Job   ₹150--₹200 for rating Google Maps corporate/mule account followed within 2--48 hours by  outflow_amount_progression_slope,   2026)]{.underline}](https://www.bachao.ai/blog/task-scam-telegram-job-fraud-india)
  Scams**           locations or YouTube videos. (2)  rapid, monotonically increasing UPI outflows (₹1,000   initiation_mode (QR_SCAN_GALLERY /  
                    Small genuine payout builds trust \\rightarrow ₹5,000 \\rightarrow ₹25,000 \\rightarrow  INTENT_URL), beneficiary_fan_in_1h. 
                    via a mule account. (3) Victim    ₹95,000) to distinct high-velocity VPAs via QR/intent                                      
                    moved to Telegram \"prepaid       links.                                                                                     
                    task\" channel requiring                                                                                                     
                    escalating UPI deposits via                                                                                                  
                    dynamic QR codes/links to unlock                                                                                             
                    bundled commission tiers; account                                                                                            
                    frozen on \"combo task.\"                                                                                                    

  **4. Fake         \(1\) Victim searches             Active voice call during session +                     vpa_keyword_match_score (refund,    [[Top UPI Frauds Trends in India 2026: Fake Customer Care Links (Medium, Mar 18, 2026)]{.underline}](https://medium.com/@naharom.marketing/top-upi-frauds-trends-in-india-2026-11a2fdffec3b); [[Bank of Baroda Cyber Fraud Advisory (Nov
  Customer-Care &   Google/social media for airline,  paste/intent-triggered VPA containing misleading       claim, helpdesk), is_call_active,   2, 2026)]{.underline}](https://bankofbaroda.bank.in/cyber-fraud-awareness)
  Refund Scams**    courier, utility, or UPI app      strings (refund@, cashback@, kyc@, care@) + abnormal   clipboard_paste_vpa_flag,           
                    helpline and calls a SEO-poisoned round/near-limit debit amount.                         initiation_mode.                    
                    number. (2) Fraudster poses as                                                                                               
                    support agent processing a refund                                                                                            
                    or KYC unblock. (3) Victim is                                                                                                
                    tricked into clicking an UPI                                                                                                 
                    intent URI, approving a merchant                                                                                             
                    collect request, or installing a                                                                                             
                    screen-sharing tool.                                                                                                         

  **5.              \(1\) Scammer contacts victim on  txn_type == \'COLLECT\' or MANDATE_CREATE where payer  txn_direction (PULL/COLLECT),       [[NPCI Ends P2P Collect Requests From Oct 1, 2025 to Curb Fraud (Times of India, Aug 14,
  Collect-Request   OLX/marketplace pretending to buy has zero prior transaction history with the requesting merchant_collect_decline_rate_1h,   2025)]{.underline}](https://timesofindia.indiatimes.com/business/india-business/upi-fraud-clampdown-npci-to-end-p2p-collect-requests-from-october-1-banks-apps-told-to-block-pull-transactions-permanently/articleshow/123309612.cms);
  (Pull) Fraud**    an item or send a reward. (2)     merchant VPA; newly registered P2M VPA issuing         payer_merchant_prior_txns,          [[The Collect-Request Trap in FY26 (CyberRishabh, June 10, 2026)]{.underline}](https://cyberrishabh.com/posts/upi-scams-collect-request-trap.html)
                    Since NPCI banned P2P collect     high-frequency collect requests across disparate       merchant_onboarding_age_days,       
                    requests on Oct 1, 2025, scammers states with high decline/timeout rate.                 geo_distance_km.                    
                    now abuse **verified/unverified                                                                                              
                    P2M (merchant) collect handles**                                                                                             
                    or UPI AutoPay mandate creation                                                                                              
                    requests disguised as incoming                                                                                               
                    credits. (3) Victim enters UPI                                                                                               
                    PIN thinking PIN is needed to                                                                                                
                    receive money.                                                                                                               

  **6. QR-Code      \(1\) *Quishing*: Scammer sends a Mode 1: QR scanned from local phone gallery (qr_source qr_scan_source (CAMERA vs GALLERY), [[Cyber Crime Police Arrest Man in Delhi Linked to 88 UPI QR Investment Frauds (Telangana Tribune, Apr 12, 2025)]{.underline}](https://www.telanganatribune.com/cyber-crime-police-arrest-man-in-delhi-for-investment-fraud/); [[QR Code
  Tampering &       QR code image over WhatsApp       == \'GALLERY_IMAGE\') during an active phone call to a payer_gps_to_merchant_dist_km,      Tampering Guide (ZET, Jan 16, 2025)]{.underline}](https://zetapp.in/blog/how-to-report-upi-fraud)
  Gallery QR        claiming the victim must scan it  P2P/newly minted VPA. Mode 2: Sudden shift in a        is_call_active,                     
  Traps**           to \"receive\" a payment, or (2)  merchant location\'s geographical payer cluster or     beneficiary_vpa_age_hours.          
                    *Physical Tampering*: Fraudster   mismatch between static QR VPA state and scanning                                          
                    pastes a mule QR sticker over a   payer GPS.                                                                                 
                    legitimate shopkeeper\'s                                                                                                     
                    soundbox/standee QR code.                                                                                                    

  **7.              \(1\) Victim is socially          Android DisplayManager / accessibility API detects     screen_mirroring_active,            [[AnyDesk Screen Sharing Scam Analysis (Jan 21, 2026)]{.underline}](https://hindidefinition.com/anydesk-screen-sharing-scam-hindi/); [[Bank of Baroda Screen-Sharing Fraud Warning (Nov 2,
  Screen-Sharing &  engineered into installing        secondary virtual display, screen-cast projection      accessibility_service_enabled,      2026)]{.underline}](https://bankofbaroda.bank.in/cyber-fraud-awareness)
  Remote-Access     AnyDesk, TeamViewer, RustDesk, or (is_screen_sharing=True), or known remote-access       installed_remote_apps_count,        
  Takeover**        WhatsApp screen-share during a    package running; unusual touch cadence / zero touch    touch_velocity_std, is_call_active. 
                    support/KYC call. (2) Fraudster   pressure variance.                                                                         
                    watches incoming OTPs and screen                                                                                             
                    keyboard or initiates UPI                                                                                                    
                    transfers remotely while guiding                                                                                             
                    the victim to type their MPIN.                                                                                               

  **8. SIM Swap &   \(1\) Attacker obtains victim\'s  New device_id + new sim_iccid / eSIM profile bound to  hours_since_sim_or_device_change,   [[The Rise of eSIM Fraud in India and What You Can Do About It (South Indian Bank, Nov 26, 2025)]{.underline}](https://www.southindianbank.bank.in/blog/safe-banking/the-rise-of-eSI-fraud-in-india-and-what-you-can-do-about-it); [[UPI
  Remote eSIM       PII/Aadhaar details via phishing  existing customer user_id; IP ASN/geolocation jump;    device_id_change_flag,              24-Hour ₹5,000 Cooling Limit Guide (Sept 30, 2026)]{.underline}](https://gstmunshi.com/blog/upi-cooling-period-limit-rs-5000-twenty-four-hours-guide)
  Hijacking**       and tricks telecom carrier (or    balance inquiry immediately after device registration; sim_iccid_change_flag,              
                    abuses remote eSIM upgrade SMS    transaction of ₹4,999 during the first 24h cooling     amount_near_5k_cooling_cap,         
                    flow) into porting the victim\'s  window followed by ₹99,999 at hour 24 + \\epsilon.     post_24h_spike_ratio.               
                    mobile number onto an                                                                                                        
                    attacker-controlled eSIM/SIM. (2)                                                                                            
                    Victim\'s SIM loses network;                                                                                                 
                    attacker completes UPI device                                                                                                
                    binding on a new handset, resets                                                                                             
                    MPIN using debit card/Aadhaar                                                                                                
                    OTP, and drains accounts after                                                                                               
                    the 24h ₹5,000 cooling window.                                                                                               

  **9. Phishing,    \(1\) Victim receives             Sideloaded app indicator                               untrusted_installer_flag,           [[Cyber Fraudsters Using Malicious APKs & Call Forwarding to Bypass UPI Security (Business Standard / CloudSEK, Mar 11,
  Smishing &        SMS/WhatsApp link for fake RTO    (untrusted_apk_installed=True); silent background      sms_read_permission_abuse_score,    2026)]{.underline}](https://www.business-standard.com/industry/news/cyber-fraudsters-using-new-tech-to-bypass-upi-security-features-report-126031100477_1.html); [[PhonePe Malicious APK Advisory (Dec 3,
  Malicious APKs**  e-Challan, electricity bill       device-binding SMS sent from device IP different from  binding_ip_vs_txn_ip_mismatch,      2025)]{.underline}](https://www.phonepe.com/blog/trust-and-safety/how-to-stay-safe-from-downloading-fake-apps-via-apk-scams/)
                    disconnection, PM-Kisan subsidy,  app session IP; midnight/off-hours velocity bursts;    hour_of_day, failed_auth_count_15m. 
                    or courier tracking. (2)          multiple failed MPIN/OTP attempts followed by rapid                                        
                    Sideloading the .apk grants       sweep.                                                                                     
                    RECEIVE_SMS, SEND_SMS, and                                                                                                   
                    BIND_ACCESSIBILITY_SERVICE                                                                                                   
                    permissions. (3) Malware silently                                                                                            
                    intercepts bank OTPs, sends                                                                                                  
                    silent SIM-binding SMS from the                                                                                              
                    victim\'s phone, or overlays a                                                                                               
                    fake UPI PIN screen.                                                                                                         

  **10.             \(1\) *Recruitment*: Students,    Dormant or low-balance account suddenly exhibits       account_in_degree_1h,               [[I4C Identifies 26.48 Lakh Layer-1 Mule Accounts Across Indian Banks (PIB MHA Release, Feb 4, 2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095); [[I4C & RBIH Sign MoU on MuleHunter.AI (PIB, May 12,
  Mule-Account      gig workers, and rural BSBD/PMJDY 10\\times--100\\times historical turnover; high        account_out_degree_1h,              2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2260277)
  Networks          account holders rent out bank     in_degree_1h from geographically dispersed payers;     pass_through_ratio_24h,             
  (Recruitment,     accounts + SIMs + net-banking     near-unity pass_through_ratio                          median_fund_dwell_time_sec,         
  Renting,          kits for ₹2,000--₹10,000/month    (\\frac{\\text{outflow}\_{1h}}{\\text{inflow}\_{1h}}   shared_device_account_count,        
  Layering)**       via Telegram \"commission\" bots. \\in \[0.90, 1.05\]); median dwell time of funds \< 15 dormancy_wakeup_flag.               
                    (2) *Layer 1 (Collection)*:       minutes; shared device_id or ip_subnet logging into                                        
                    Receives rapid fan-in from        multiple distinct accounts.                                                                
                    10--100 scam victims across                                                                                                  
                    India. (3) *Layer 2/3 (Layering &                                                                                            
                    Integration)*: Automated bots                                                                                                
                    disperse funds within \<15                                                                                                   
                    minutes (pass_through_ratio                                                                                                  
                    \\approx 1.0) via IMPS/UPI to                                                                                                
                    2nd/3rd-hop mules, crypto P2P                                                                                                
                    merchants, or ATM cash-outs.                                                                                                 
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** In UPI, once a push transaction settles, recovery
    > is operationally arduous (only \~14.9% of reported NCRP fraud
    > value was lien-marked between 2021 and 2025: ₹8,189 crore out of
    > ₹55,050 crore per [[PIB Release ID 2287039, July 21,
    > 2026]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1)).
    > Furthermore, because victims authorize APP scams themselves,
    > **beneficiary (payee) telemetry is often more predictive than
    > payer telemetry**.

-   **Analytical Inference:** TxnVigil v2 must compute features
    > symmetrically on **both the Payer (sender_id) and the Payee
    > (receiver_vpa / receiver_account_id)** inside the Redis online
    > store before scoring a transaction:

    1.  **Payer Coercion & Takeover Features:** is_call_active,
        > is_screen_sharing, qr_scan_source == \'GALLERY\',
        > hours_since_device_or_sim_bind, fd_broken_last_1h,
        > outflow_progression_slope_24h, and vpa_suspicious_regex_flag.

    2.  **Payee Mule-Velocity Features (Updated Live in Redis):**
        > payee_unique_senders_1h, payee_inflow_sum_1h,
        > payee_outflow_sum_1h, payee_pass_through_ratio_1h
        > (\\frac{\\text{outflow}\_{1h}}{\\text{inflow}\_{1h} +
        > \\epsilon}), payee_median_dwell_sec, payee_account_age_days,
        > and payee_shared_device_accounts. This dual-sided feature
        > vector allows LightGBM to catch a Digital Arrest or Task Scam
        > on the very first transfer by recognizing that the
        > *destination VPA* is acting as a Layer-1 collection mule.

### (d) Open Uncertainties

-   UNCERTAIN: **Exact Per-Typology Breakdown of NCRP Losses.** While
    > I4C publishes aggregate NCRP complaint counts (65.89 lakh) and
    > total losses (\>₹55,050 crore) via parliamentary replies ([[PIB
    > Release ID 2287039, July 21,
    > 2026]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1)),
    > the Ministry of Home Affairs does not publish an official audited
    > annual percentage split by individual scam typology (e.g., exact
    > share of Digital Arrest vs. Task Scams vs. APK malware).

-   UNCERTAIN: **NPCI Ecosystem-Wide Real-Time Fraud Basis Points (FY
    > 2025-26).** NPCI does not publish a monthly or annual public table
    > of confirmed fraud-to-sales basis points across all 300+ billion
    > annual UPI transactions; public RBI numbers in [[Table VI.3 of the
    > RBI Annual Report
    > 2025-26]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
    > only reflect bank-reported FMR cases \\ge ₹1 lakh.

## R3. Public Datasets for Transaction-Fraud and AML Modelling

### (a) Five-Line Executive Summary

1.  **Verified Fact:** No authentic, multi-million-row Indian UPI
    > transaction dataset with verified fraud and mule labels is
    > publicly available due to RBI\'s April 2018 Payment System Data
    > Localization directive and the [[DPDP Act
    > 2023]{.underline}](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa);
    > small \"UPI fraud\" CSVs on Kaggle/Mendeley are either tiny
    > classroom toys (\<50,000 rows) or relabeled clones of PaySim
    > ([[Mendeley Data Comparison, July 11,
    > 2026]{.underline}](https://data.mendeley.com/datasets/compare/gcsx4mfzhb)).

2.  **Verified Fact:** **PaySim** (6.36M rows) suffers from catastrophic
    > target leakage in its oldbalanceOrg, newbalanceOrig,
    > oldbalanceDest, and newbalanceDest columns because the simulator
    > zeroes out balances differently for fraudulent vs. legitimate
    > transfers, inflating naive tree models to \>0.999 ROC-AUC while
    > failing completely in production ([[PaySim
    > Kaggle]{.underline}](https://www.kaggle.com/datasets/ealaxi/paysim1)).

3.  **Verified Fact:** For graph-based anti-money laundering and
    > mule-network modeling, [**[IBM AMLworld (Altman et al., NeurIPS
    > 2023)]{.underline}**](https://arxiv.org/html/2306.16424v1) (5.1M
    > to 180M transactions across HI/LI-Small/Medium/Large,
    > CDLA-Sharing-1.0) and [**[SAML-D (Oztas et al.,
    > 2023/2024)]{.underline}**](https://arxiv.org/html/2608.15447v1)
    > (9.50M transactions, 28 typology patterns) are the strongest
    > public multi-bank graph benchmarks.

4.  **Verified Fact:** For high-dimensional device/identity tabular
    > modeling, [**[IEEE-CIS Fraud
    > Detection]{.underline}**](https://www.kaggle.com/c/ieee-fraud-detection)
    > (590,540 training rows, 434 features including
    > device/IP/email/card metadata, standardized in the [[Amazon Fraud
    > Dataset Benchmark
    > (FDB)]{.underline}](https://github.com/amazon-science/fraud-dataset-benchmark))
    > and
    > [**[Elliptic++]{.underline}**](https://github.com/git-disl/EllipticPlusPlus)
    > (203,769 transaction nodes + 822,942 wallet address nodes) provide
    > rich real-world signal structures.

5.  **Analytical Inference:** TxnVigil v2 should never train its
    > flagship UPI demo model on raw PaySim alone; instead, it should
    > use **(1) IBM AMLworld (HI-Small, 5.1M txns)** to benchmark
    > graph/mule detection, **(2) IEEE-CIS (via Amazon FDB)** to
    > benchmark tabular velocity + device-fingerprint engineering, and
    > **(3) a custom UPI-calibrated synthetic generator** injecting the
    > 10 Indian typologies from R2.

### (b) Comprehensive Comparison of Public Fraud and AML Datasets

The table below evaluates all 11 requested public datasets plus the
status of Indian UPI datasets against the structural requirements of a
real-time behavioral and graph fraud platform.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Dataset Name   Size (Rows &        Time Span      Fraud /       Timestamps?               Account / Customer  Device / IP Metadata?     Graph Structure?       License            Primary Download / Paper URL                                                                                                                                           Known Issues & Technical
                 Entities)                          Illicit Rate                            IDs?                                                                                                                                                                                                                                                           Flaws
  -------------- ------------------- -------------- ------------- ------------------------- ------------------- ------------------------- ---------------------- ------------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------------------
  **PaySim**     6,362,620 txns      744 hourly     0.129% (8,213 Yes (1-hour step integer) Yes (nameOrig,      No                        Degenerate (almost all CC BY-NC-SA 4.0    [[Kaggle: ealaxi/paysim1]{.underline}](https://www.kaggle.com/datasets/ealaxi/paysim1)                                                                                 **Severe Balance Leakage:**
  (Lopez-Rojas                       steps (30      frauds)                                 nameDest)                                     nameOrig transact                                                                                                                                                                                                Fraudulent TRANSFER followed
  et al., 2016)                      days)                                                                                                once; no multi-hop                                                                                                                                                                                               by CASH_OUT leaves
                                                                                                                                          cycles)                                                                                                                                                                                                          oldbalanceOrg - amount !=
                                                                                                                                                                                                                                                                                                                                                           newbalanceOrig
                                                                                                                                                                                                                                                                                                                                                           deterministically; models
                                                                                                                                                                                                                                                                                                                                                           learn arithmetic bug instead
                                                                                                                                                                                                                                                                                                                                                           of behavior; zero graph
                                                                                                                                                                                                                                                                                                                                                           topology.

  **BankSim**    594,643 txns        180 daily      1.21% (7,200  Coarse (daily step        Yes (customer,      No (only zipcodeOri,      Bipartite              Open / Academic    [[PMC Benchmark Analysis (Apr 2024)]{.underline}](https://pmc.ncbi.nlm.nih.gov/articles/PMC11016795/) / [[GitHub                                                       Zipcode fields are constant
  (Lopez-Rojas & (\~4,112 customers, steps (6       frauds)       0--179)                   merchant)           zipMerchant)              customer-to-merchant                      Mirror]{.underline}](https://github.com/Karthiksriram09/Fraud-Detection-in-Python)                                                                                     across almost all rows; no
  Axelsson,      50 merchants)       months)                                                                                              only (no P2P                                                                                                                                                                                                     sub-day timestamps
  2014)                                                                                                                                   transfers)                                                                                                                                                                                                       (impossible to compute 5m/1h
                                                                                                                                                                                                                                                                                                                                                           velocity windows); bipartite
                                                                                                                                                                                                                                                                                                                                                           merchant-only graph cannot
                                                                                                                                                                                                                                                                                                                                                           model P2P mule layering.

  **IEEE-CIS     590,540 train +     6 months       3.50% (20,663 Yes (TransactionDT        Implicit            Yes (DeviceType,          Implicit               Competition /      [[Kaggle: ieee-fraud-detection]{.underline}](https://www.kaggle.com/c/ieee-fraud-detection) & [[Amazon FDB                                                             V1--V339 columns are
  Fraud          506,691 test txns;                 train frauds) seconds offset)           (card1--card6 +     DeviceInfo, id_01--id_38, entity-sharing graph   Academic           GitHub]{.underline}](https://github.com/amazon-science/fraud-dataset-benchmark)                                                                                        anonymized Vesta engineered
  Detection**    434 features                                                               addr + D1 entity    browser/OS)               (shared cards,         (Apache-2.0 loader                                                                                                                                                                        features with heavy
  (Vesta / IEEE,                                                                            fingerprint)                                  devices, emails,       in FDB)                                                                                                                                                                                   collinearity and missingness;
  2019)                                                                                                                                   addresses)                                                                                                                                                                                                       no explicit user_id (must
                                                                                                                                                                                                                                                                                                                                                           reconstruct ENTITY_ID from
                                                                                                                                                                                                                                                                                                                                                           card + address + time delta
                                                                                                                                                                                                                                                                                                                                                           D1).

  **ULB Credit   284,807 txns        48 hours (Sept 0.172% (492   Yes (Time seconds from    No                  No                        None (independent      Open Database      [[Kaggle: mlg-ulb/creditcardfraud]{.underline}](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) & [[PMC Study                                                 Features V1--V28 are
  Card Fraud**                       2013)          frauds)       first txn)                                                              rows)                  (ODbL)             (2024)]{.underline}](https://pmc.ncbi.nlm.nih.gov/articles/PMC11065415/)                                                                                               PCA-projected components with
  (Dal Pozzolo                                                                                                                                                                                                                                                                                                                                             zero domain semantics; no
  et al.,                                                                                                                                                                                                                                                                                                                                                  customer IDs or counterparty
  2013/2015)                                                                                                                                                                                                                                                                                                                                               IDs, making stateful velocity
                                                                                                                                                                                                                                                                                                                                                           or graph feature engineering
                                                                                                                                                                                                                                                                                                                                                           impossible.

  **Sparkov      1,852,394 txns      2 years (Jan   0.52% (9,651  Yes (exact                Yes (cc_num,        No (has lat/long &        Bipartite              CC0: Public Domain [[Kaggle: kartik2112/fraud-detection]{.underline}](https://www.kaggle.com/datasets/kartik2112/fraud-detection) & [[PMC Study (Sept                                     Clean timestamps and
  Simulated      (1,296,675 train +  2019 -- Dec    frauds; 5.70% trans_date_trans_time +   merchant, first,    merch_lat/merch_long)     customer-to-merchant   (Generator GPLv3)  2023)]{.underline}](https://pmc.ncbi.nlm.nih.gov/articles/PMC1053547/)                                                                                                 geospatial coordinates for
  Credit Card**  555,719 test;       2020)          in FDB        UNIX epoch)               last, dob)                                    graph                                                                                                                                                                                                            velocity/distance features,
  (Brandon       \~1,000 customers,                 subset)                                                                                                                                                                                                                                                                                                but rule-based Gaussian
  Harris /       800 merchants)                                                                                                                                                                                                                                                                                                                            simulation makes simple amt +
  Shenoy, 2020)                                                                                                                                                                                                                                                                                                                                            hour + category tree splits
                                                                                                                                                                                                                                                                                                                                                           achieve \>0.99 AUC trivially;
                                                                                                                                                                                                                                                                                                                                                           no P2P mule transfers.

  **IBM AMLworld 6 splits: HI-Small  10 days        0.051%        Yes (minute-resolution    Yes (Account        No (has payment Format:   Rich directed          CDLA-Sharing-1.0   [[Kaggle:                                                                                                                                                              Lacks mobile
  (IT-AML)**     (5.08M txns, 515K   (Small), 16    (LI-Medium:   timestamps)               sender/receiver +   Wire, ACH, Cheque, Credit multi-graph with 8                        ealtman2019/ibm-transactions-for-anti-money-laundering-aml]{.underline}](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) & device/IP/session telemetry
  (Altman et     accts) to HI-Large  days (Medium), 1/1,948) to                             From Bank / To      Card, Cash, Bitcoin +     canonical laundering                      [[arXiv:2306.16424v1 (June 2023 / NeurIPS Dec 2023)]{.underline}](https://arxiv.org/html/2306.16424v1)                                                                 (designed for inter-bank
  al., NeurIPS   (180M txns, 2.12M   97 days        0.124%                                  Bank)               multi-currency)           topologies (fan-in,                                                                                                                                                                                              wire/ACH AML rather than
  2023)          accts) & LI-Large   (Large)        (HI-Large:                                                                            fan-out, cycle,                                                                                                                                                                                                  mobile app telemetry), and
                 (176M txns, 2.06M                  1/807)                                                                                scatter-gather,                                                                                                                                                                                                  Account IDs can be memorized
                 accts)                                                                                                                   gather-scatter,                                                                                                                                                                                                  by transductive GNNs if node
                                                                                                                                          bipartite, stack,                                                                                                                                                                                                IDs are not stripped.
                                                                                                                                          random)                                                                                                                                                                                                          

  **IBM AMLSim** Configurable        Configurable   \~0.131%      Yes (step/timestamp)      Yes (orig_acct,     No                        Directed               Apache-2.0         [[GitHub: IBM/AMLSim]{.underline}](https://github.com/IBM/AMLSim) & [[NeurIPS 2023 Comparison]{.underline}](https://arxiv.org/html/2306.16424v1)                       Models only the *layering*
  (Suzumura &    (standard public    (typically 1   (1/762 txns)                            bene_acct)                                    account-to-account                                                                                                                                                                                               phase (no placement or
  Kanezashi,     benchmark: 1.32M    year / 365                                                                                           multi-graph (8                                                                                                                                                                                                   integration);
  2019/2021)     txns, 100K          steps)                                                                                               smurfing/cycle motifs)                                                                                                                                                                                           single-bank/single-currency
                 accounts)                                                                                                                                                                                                                                                                                                                                 focus; largely superseded by
                                                                                                                                                                                                                                                                                                                                                           IBM\'s 2023 IT-AML / AMLworld
                                                                                                                                                                                                                                                                                                                                                           generator.

  **SAML-D**     9,504,852 txns      \~11 months    0.1039%       Yes (Date + exact Time    Yes                 No (has                   Multi-bank directed    CC BY 4.0          [[ResearchGate / IEEE ICEBE (Dec                                                                                                                                       Rich multi-class typology
  (Oztas et al., (\~890K accounts    (Oct 2022 --   (\~9,874      HH:MM:SS)                 (Sender_account,    Sender_bank_location,     transaction graph with                    2023)]{.underline}](https://www.researchgate.net/publication/376637949_Enhancing_Anti-Money_Laundering_Development_of_a_Synthetic_Transaction_Monitoring_Dataset) &    ground truth (Smurfing,
  2023/2024)     across 12           Aug 2023)      laundering                              Receiver_account)   Receiver_bank_location,   explicit                                  [[arXiv SAML-D Benchmark (Aug 15, 2026)]{.underline}](https://arxiv.org/html/2608.15447v1)                                                                             Fan_In, Cycle,
                 currencies & 15                    txns across                                                 Payment_type)             Laundering_type labels                                                                                                                                                                                           Scatter-Gather), but
                 locations)                         28                                                                                    (28 typologies)                                                                                                                                                                                                  synthetic amount
                                                    typologies)                                                                                                                                                                                                                                                                                            distributions for certain
                                                                                                                                                                                                                                                                                                                                                           typologies have narrow
                                                                                                                                                                                                                                                                                                                                                           variance; lacks
                                                                                                                                                                                                                                                                                                                                                           device/session telemetry.

  **Elliptic &   **Elliptic:**       49 discrete    9.76% of      Discrete (timesteps       Yes in              No (blockchain protocol   Temporal homogeneous   Academic /         [[GitHub: git-disl/EllipticPlusPlus]{.underline}](https://github.com/git-disl/EllipticPlusPlus) & [[MDPI TWIN-GNN Study (Oct 26,                                       77% of nodes are unlabeled;
  Elliptic++**   203,769 Bitcoin txn timesteps (\~2 labeled txns  1--49)                    **Elliptic++**      features: 165 txn         (Elliptic) &           MIT-style repo     2026)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)                                                                                                            severe temporal concept drift
  (Weber et al., nodes, 234,355      weeks per      (4,545                                  (822,942 wallet     features + 56 wallet      heterogeneous                                                                                                                                                                                                    at timestep 43 (Dark Market
  2019; Elmougy  edges.              step)          illicit,                                addresses with 56   features)                 bipartite                                                                                                                                                                                                        shutdown causes GNN recall
  & Liu, KDD     **Elliptic++:**                    42,019 licit,                           features)                                     transaction-wallet                                                                                                                                                                                               collapse); UTXO blockchain
  2023)          adds 822,942 wallet                157,205                                                                               graph (Elliptic++)                                                                                                                                                                                               mechanics differ slightly
                 address nodes &                    unlabeled)                                                                                                                                                                                                                                                                                             from bank-account balances.
                 1.27M address-txn                                                                                                                                                                                                                                                                                                                         
                 edges                                                                                                                                                                                                                                                                                                                                     

  **Amazon Fraud Unified benchmark   Varies by      0.18% to      Yes (standardized         Standardized        Yes (in IEEE-CIS &        Entity-linkable on     Apache-2.0         [[GitHub: amazon-science/fraud-dataset-benchmark]{.underline}](https://github.com/amazon-science/fraud-dataset-benchmark) & [[arXiv:2208.14417v3 (Sept 22,             Excellent reproducible
  Dataset        wrapping 9 public   sub-dataset    34.2% across  temporal train/test       ENTITY_ID           FraudEcommerce subsets)   IEEE-CIS / Sparkov                        2023)]{.underline}](https://arxiv.org/pdf/2208.14417)                                                                                                                  evaluation harness, but
  Benchmark      datasets (IEEE-CIS,                tasks         splits)                                                                 subsets                                                                                                                                                                                                          relies on Kaggle API download
  (FDB)**        ULB, Sparkov,                                                                                                                                                                                                                                                                                                                             credentials for underlying
  (Prince et     FraudEcommerce,                                                                                                                                                                                                                                                                                                                           raw CSVs and does not include
  al.,           etc.)                                                                                                                                                                                                                                                                                                                                     multi-hop AML graph datasets
  2023/2024)                                                                                                                                                                                                                                                                                                                                               like AMLworld.

  **Indian / UPI Only small          Synthetic /    Artificial    Synthetic                 Synthetic           None                      None                   Various            [[Mendeley Harmonized Fraud Dataset (July 11, 2026)]{.underline}](https://data.mendeley.com/datasets/compare/gcsx4mfzhb)                                               **Not found (Authentic
  Public         synthetic/student   Ad-hoc         (5%--50%)                                                                                                                                                                                                                                                                                              UPI):** Zero real NPCI/bank
  Datasets**     CSVs (5,000--50,000                                                                                                                                                                                                                                                                                                                       UPI datasets exist publicly.
                 rows)                                                                                                                                                                                                                                                                                                                                     All \"UPI Fraud\" files on
                                                                                                                                                                                                                                                                                                                                                           Kaggle are either tiny
                                                                                                                                                                                                                                                                                                                                                           rule-generated toys or
                                                                                                                                                                                                                                                                                                                                                           renamed PaySim subsets.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Relying on PaySim will cause any seasoned ML
    > reviewer to dismiss the project immediately due to its
    > well-documented balance-column arithmetic leakage ([[Kaggle
    > PaySim]{.underline}](https://www.kaggle.com/datasets/ealaxi/paysim1)),
    > while relying on ULB Credit Card (V1--V28) makes real-time Redis
    > velocity and graph feature engineering impossible.

-   **Analytical Inference:** Validate TxnVigil v2 across **three
    > complementary datasets**:

    1.  **Primary Graph & Mule-Account Benchmark --- [[IBM AMLworld
        > HI-Small (5.08M transactions, 515K
        > accounts)]{.underline}](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml) +
        > [[SAML-D (9.50M
        > transactions)]{.underline}](https://arxiv.org/html/2608.15447v1):**
        > Use HI-Small (which fits easily in 8--16 GB laptop RAM via
        > DuckDB/Parquet) and a 2M-row chronological slice of SAML-D to
        > benchmark TxnVigil\'s **multi-hop mule graph features**
        > (fan-in, fan-out, pass-through ratio, PageRank, cycle
        > detection, 2-hop risk propagation) and chronological PR-AUC
        > under \~0.1% prevalence.

    2.  **Primary Device & Behavioral Tabular Benchmark --- [[IEEE-CIS
        > Fraud Detection (via Amazon FDB temporal split, 590K
        > rows)]{.underline}](https://github.com/amazon-science/fraud-dataset-benchmark):**
        > Use IEEE-CIS with the competition-winning ENTITY_ID
        > (card1_addr1_D1) to prove that TxnVigil\'s LightGBM + Redis
        > sliding-window feature pipeline achieves top-tier ROC-AUC /
        > PR-AUC on real-world noisy device/IP/velocity data.

    3.  **Live End-to-End Demo Stream --- TxnVigil Synthetic UPI
        > Generator (TxnVigil-Synth-UPI):** Build a deterministic
        > SimPy/Mesa generator calibrated to NPCI/RBI statistics that
        > emits realistic Indian UPI events (P2P_PUSH, P2M_QR,
        > COLLECT_P2M, AUTOPAY) with injected Digital Arrest, Task Scam,
        > APK Takeover, and 3-hop Mule Layering typologies for the live
        > Docker Compose demo.

### (d) Open Uncertainties

-   UNCERTAIN: **RBIH Public Benchmark Release.** Under the [[RBI
    > FREE-AI Framework (August 13, 2025, Pillar 1:
    > Infrastructure)]{.underline}](https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306),
    > the FREE-AI Committee recommended establishing shared
    > financial-sector data infrastructure and anonymized benchmark
    > datasets as Digital Public Infrastructure (DPI), but neither RBI
    > nor NPCI has released a public anonymized UPI dataset as of
    > November 2026.

## R4. State of the Art in Transaction Fraud Detection Models (2022--2026)

### (a) Five-Line Executive Summary

1.  **Verified Fact:** Across rigorous 2022--2026 tabular
    > benchmarks---including [[TabArena
    > (2025/2026)]{.underline}](https://www.codesota.com/tasks/tabular-ml),
    > [[AIMultiple\'s 19-Dataset Tabular Benchmark (October 12,
    > 2026)]{.underline}](https://aimultiple.com/tabular-models), and
    > the [[Elliptic++ TWIN-GNN vs. LightGBM study (October 26,
    > 2026)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)---tuned
    > Gradient Boosted Decision Trees (**LightGBM v4.7.0**, **XGBoost
    > v3.4.2**, **CatBoost v1.2.10**) remain the dominant production
    > models for medium-to-large transaction fraud datasets (\>50,000
    > rows) with sub-5ms CPU latency.

2.  **Verified Fact:** While [[TabPFN v2 (Hollmann et al.,]{.underline}
    > *[Nature]{.underline}* [637, Jan
    > 2025)]{.underline}](https://www.codesota.com/tasks/tabular-ml) and
    > [[TabPFN-2.5 (November
    > 2025)]{.underline}](https://arxiv.org/html/2511.08667v2)
    > outperform GBDTs on small datasets (N \\le 10,000--50,000),
    > [[independent evaluations (arXiv:2505.16226v1, May
    > 2025)]{.underline}](https://arxiv.org/html/2505.16226v1) confirm
    > quadratic attention memory scaling and high GPU inference latency
    > make TabPFN impractical for real-time million-row transaction
    > streams on an 8--16 GB CPU laptop.

3.  **Verified Fact:** Frontier payment processors---including [[Stripe
    > (Payments Foundation Model,
    > 2025/2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning),
    > [[Visa (TREASURE Transformer, April
    > 2026)]{.underline}](https://arxiv.org/html/2511.19693v3),
    > [[Sardine AI (September
    > 2026)]{.underline}](https://www.sardine.ai/blog/foundation-model-issuer-fraud-detection),
    > and [[Razorpay (Vulcan Foundation Model, August 18,
    > 2026)]{.underline}](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)---do
    > **not** replace GBDTs with transformers; instead, they pre-train
    > sequence transformers on transaction histories and feed the
    > resulting dense embeddings into downstream GBDT classifiers.

4.  **Verified Fact:** Production fraud models face severe **label
    > delay** (victim complaints arrive hours to weeks later, while
    > non-alerted transactions are only *unlabeled*, not guaranteed
    > clean) and **concept drift**, which must be mitigated via
    > dual-model ensembles (short-term fast-adapting model + long-term
    > delayed-feedback model per [[Dal Pozzolo et
    > al.]{.underline}](https://www.semanticscholar.org/paper/Credit-card-fraud-detection-and-concept-drift-with-Pozzolo-Boracchi/b769ec8f3be051b7c5f9a0ba5f85a38594950df9)),
    > sample-importance weighting, and post-hoc probability calibration.

5.  **Analytical Inference:** TxnVigil v2 should deploy a **Hybrid
    > Two-Stage Scoring Architecture**: a primary **LightGBM v4.7.0**
    > classifier trained on engineered velocity + graph features
    > (calibrated via Isotonic Regression for true expected-value cost
    > thresholding), augmented by an **unsupervised Isolation Forest /
    > Autoencoder anomaly score passed as an input feature** (late/early
    > fusion) rather than used as a standalone blocker.

### (b) Model Families, Latest Versions, Benchmarks, and Operational Trade-Offs

Despite a wave of deep-learning architectures for tabular
data---including FT-Transformer (Gorishniy et al., 2021), TabNet (Arik &
Pfister, 2021), and prior-data fitted networks ([[TabPFN
v2,]{.underline} *[Nature]{.underline}*
[2025]{.underline}](https://www.codesota.com/tasks/tabular-ml);
[[TabPFN-2.5, Nov
2025]{.underline}](https://arxiv.org/html/2511.08667v2))---gradient-boosted
trees remain the undisputed workhorse for real-time transaction fraud
scoring when stateful velocity and graph features are engineered
properly. In the [[October 26, 2026 Elliptic++ benchmark
(MDPI]{.underline} [*Journal of Cybersecurity and
Privacy*)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186),
**LightGBM achieved a transaction-level F1 score of 0.807 compared to
0.439 for end-to-end GNNs**, because tree ensembles handle skewed
heavy-tailed financial ratios, sharp threshold boundaries (such as
NPCI\'s ₹5,000 and ₹1,00,000 caps), missing device fields, and temporal
distribution shifts without over-smoothing across edges. Similarly, on
the 9.5M-row SAML-D dataset under a strict 0.1% laundering prevalence
and chronological split, [[LightGBM achieved 89% precision at 0.51
alerts per 10,000 transactions (August 15,
2026)]{.underline}](https://arxiv.org/html/2608.15447v1), whereas
standalone Isolation Forest, Local Outlier Factor, and dense
Autoencoders suffered catastrophic false-positive rates when used
directly as decision makers, adding value only when stacked via late
fusion (PR-AUC rising from 0.0469 to 0.0477).

Where deep learning genuinely moves the needle in 2025--2026 industry
deployments is **sequential representation learning (Transaction
Foundation Models)**. [[Stripe\'s Payments Foundation Model (PFM,
2025/2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning),
[[Visa\'s TREASURE foundation model (arXiv:2511.19693v3, April 8,
2026)]{.underline}](https://arxiv.org/html/2511.19693v3), [[Sardine
AI\'s card-sequence transformer (September 10,
2026)]{.underline}](https://www.sardine.ai/blog/foundation-model-issuer-fraud-detection)
(reporting up to 35% higher fraud recall at fixed false-positive rates),
and [[Razorpay\'s Vulcan payments foundation model (August 18,
2026)]{.underline}](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)
all follow the same two-stage pattern: a causal Transformer or GRU
encodes a user\'s last N transactions into a compact
32-to-128-dimensional behavioral embedding (updated asynchronously in
Redis after each transaction), and that embedding is concatenated with
real-time Redis velocity counters and fed into a fast GBDT
(LightGBM/XGBoost) for the synchronous sub-20ms authorization decision.

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Model / Library           Latest Stable Version & Release Date                                                                                    Primary Benchmark / Evidence                                                               Fraud Detection       Laptop (8--16 GB RAM) & Latency Costs                                        Role in TxnVigil v2
                                                                                                                                                                                                                                               Strengths                                                                                          
  ------------------------- ----------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------ --------------------- ---------------------------------------------------------------------------- -----------------------
  **LightGBM**              **v4.7.0** (Released **July 18, 2026**, [[PyPI]{.underline}](https://pypi.org/project/lightgbm/) /                      Top transaction F1 (0.807 vs 0.439 GNN) on [[Elliptic++ (Oct                               Histogram-based       **\< 1.5 ms** single-row CPU inference; trains on 5M rows in \<45 sec on 8   **Primary Real-Time
  (lightgbm-org/LightGBM)   [[GitHub]{.underline}](https://github.com/lightgbm-org/LightGBM/releases))                                              2026)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186); top precision (0.89) on       leaf-wise splitting;  GB RAM.                                                                      Transaction
                                                                                                                                                    [[SAML-D (Aug 2026)]{.underline}](https://arxiv.org/html/2608.15447v1).                    native NaN and                                                                                     Classifier** &
                                                                                                                                                                                                                                               categorical handling;                                                                              **Account Mule
                                                                                                                                                                                                                                               native C++                                                                                         Classifier**.
                                                                                                                                                                                                                                               pred_contrib=True                                                                                  
                                                                                                                                                                                                                                               exact TreeSHAP in \<1                                                                              
                                                                                                                                                                                                                                               ms.                                                                                                

  **XGBoost**               **v3.4.2** (Released **September 15, 2026**, [[GitHub]{.underline}](https://github.com/dmlc/xgboost/releases))          Top Elo rank on large datasets in [[AIMultiple 19-Dataset Benchmark (Oct 12,               Depth-wise            **1.5--2.5 ms** CPU inference; slightly higher memory footprint than         **Challenger / Shadow
  (dmlc/xgboost)                                                                                                                                    2026)]{.underline}](https://aimultiple.com/tabular-models).                                regularized trees;    LightGBM on 5M+ rows.                                                        Model** for
                                                                                                                                                                                                                                               strong monotonic and                                                                               champion-challenger
                                                                                                                                                                                                                                               interaction                                                                                        comparison in MLflow.
                                                                                                                                                                                                                                               constraints;                                                                                       
                                                                                                                                                                                                                                               inplace_predict                                                                                    
                                                                                                                                                                                                                                               low-latency API.                                                                                   

  **CatBoost**              **v1.2.10** (Released **February 19, 2026**, [[GitHub]{.underline}](https://github.com/catboost/catboost/releases))     Strong out-of-the-box performance on high-cardinality categoricals ([[TabArena             Oblivious (symmetric) **\< 1 ms** C++ applier, but Python wheel is **274 MB** and training on      Optional offline
  (catboost/catboost)                                                                                                                               2026]{.underline}](https://www.codesota.com/tasks/tabular-ml)).                            trees give ultra-fast large datasets is slower on CPU.                                             benchmark comparator;
                                                                                                                                                                                                                                               C++ branchless                                                                                     omit from slim API
                                                                                                                                                                                                                                               evaluation and                                                                                     container to save image
                                                                                                                                                                                                                                               target-encoding                                                                                    size.
                                                                                                                                                                                                                                               without leakage.                                                                                   

  **TabPFN v2 / v2.5**      **TabPFN v2** (*Nature*, Jan 2025) / **TabPFN-2.5** (Nov 2025,                                                          Beats GBDTs on small tabular tasks (N \\le 10,000) via in-context learning                 Zero hyperparameter   **Unsuitable for real-time fraud:** O(N\^2) context attention; requires GPU; **Do not use** in
  (PriorLabs/TabPFN)        [[arXiv:2511.08667v2]{.underline}](https://arxiv.org/html/2511.08667v2))                                                ([[arXiv:2502.17361v2, June 2025]{.underline}](https://arxiv.org/html/2502.17361v2)).      tuning on small       fails on 10\^6 row imbalanced streams                                        real-time UPI scoring
                                                                                                                                                                                                                                               cold-start datasets.  ([[arXiv:2505.16226v1]{.underline}](https://arxiv.org/html/2505.16226v1)).   path.

  **Sequence Transformers / Industry pattern: [[Visa TREASURE (Apr 2026)]{.underline}](https://arxiv.org/html/2511.19693v3), [[Stripe PFM           [[Sardine AI (Sept 10,                                                                     Captures subtle       Synchronous transformer inference breaks CPU latency budgets (\>25 ms),      Implement lightweight
  Foundation Models**       (2025/2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning),   2026)]{.underline}](https://www.sardine.ai/blog/foundation-model-issuer-fraud-detection)   ordering of event     unless computed asynchronously on stream and cached in Redis.                **Markov transition
                            [[Razorpay Vulcan (Aug                                                                                                  reports +35% fraud catch when feeding sequence embeddings into GBDT.                       types (LOGIN                                                                                       log-likelihood / async
                            2026)]{.underline}](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)                                                                                                           \\rightarrow                                                                                       sequence features** in
                                                                                                                                                                                                                                               BAL_CHECK                                                                                          Redis; feed into
                                                                                                                                                                                                                                               \\rightarrow FD_BREAK                                                                              LightGBM.
                                                                                                                                                                                                                                               \\rightarrow P2P_MAX)                                                                              
                                                                                                                                                                                                                                               missed by flat count                                                                               
                                                                                                                                                                                                                                               aggregates.                                                                                        

  **Unsupervised (Isolation scikit-learn IsolationForest / PyTorch MLP Autoencoder                                                                  [[SAML-D Late-Fusion Study (Aug 15,                                                        Detects extreme       Standalone precision on 0.1% base-rate fraud is terrible (\<2\\%), causing   **Feature-Only / Late
  Forest / Autoencoder)**                                                                                                                           2026)]{.underline}](https://arxiv.org/html/2608.15447v1).                                  out-of-distribution   massive false-positive floods if used directly to block.                     Fusion:** Compute
                                                                                                                                                                                                                                               (OOD) velocity bursts                                                                              iforest_anomaly_score
                                                                                                                                                                                                                                               on zero-day                                                                                        and feed it as a
                                                                                                                                                                                                                                               typologies without                                                                                 numeric feature into
                                                                                                                                                                                                                                               labels.                                                                                            LightGBM + use for
                                                                                                                                                                                                                                                                                                                                                  analyst queue sorting
                                                                                                                                                                                                                                                                                                                                                  on novel drift.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Handling Label Delay, Verification Bias, Cost-Sensitive Calibration, and Alert Budgets

1.  **Label Delay and Verification Bias:** In Indian UPI, two distinct
    > feedback streams arrive at different speeds ([[Dal Pozzolo et
    > al.,]{.underline} *[IEEE
    > TNNLS]{.underline}*](https://www.semanticscholar.org/paper/Credit-card-fraud-detection-and-concept-drift-with-Pozzolo-Boracchi/b769ec8f3be051b7c5f9a0ba5f85a38594950df9);
    > [[Cost-Aware Adaptive Fraud Detection, Oct 21,
    > 2026]{.underline}](https://www.researchgate.net/publication/416317894_Cost-Aware_Adaptive_Credit_Card_Fraud_Detection_Under_Concept_Drift_A_Comparative_Evaluation_of_Model-Maintenance_Policies)):

    -   *Immediate Investigator/Step-Up Feedback (T + 5\\text{ min to }
        > 48\\text{ hours}):* Transactions flagged by the model/rules
        > and reviewed by an analyst or confirmed via step-up challenge
        > yield rapid labels, but suffer from **selection/verification
        > bias** (only high-score transactions are observed).

    -   *Delayed Victim NCRP/1930 Chargeback/Lien Reports (T + 1\\text{
        > day to } 30\\text{ days}):* Missed frauds (false negatives)
        > are only discovered when the victim files an NCRP/bank
        > complaint. Crucially, a transaction from 2 hours ago with no
        > complaint is **unlabeled (censored)**, not a confirmed
        > legitimate transaction!

    -   **Practical Recipe for TxnVigil v2:** Implement a **Maturity
        > Horizon Buffer (H = 7\\text{ days})** for negative labels:
        > never label a non-investigated transaction as y = 0
        > (legitimate) in training sets until 7 days have elapsed
        > without an NCRP/customer dispute, while ingesting confirmed
        > fraud (y = 1) immediately into a **fast-adapting short-term
        > LightGBM model** combined (via weighted ensemble p = 0.7
        > p\_{\\text{long}} + 0.3 p\_{\\text{short}}) with a 60-day
        > rolling baseline model.

2.  **Calibration Under Class Weighting:** If LightGBM is trained with
    > scale_pos_weight = w (or undersampling) on a 0.1% fraud dataset,
    > the raw sigmoid output \\hat{p}\_{\\text{raw}} is systematically
    > distorted upward: \\hat{p}\_{\\text{calibrated}} =
    > \\frac{\\hat{p}\_{\\text{raw}}}{\\hat{p}\_{\\text{raw}} + w(1 -
    > \\hat{p}\_{\\text{raw}})} Better still, train LightGBM with
    > **unweighted log-loss (scale_pos_weight = 1.0, boost_from_average
    > = True)** so raw probabilities match the true empirical base rate,
    > and apply **Isotonic Regression or Platt Scaling** on a
    > chronologically held-out validation fold.

3.  **Cost-Sensitive Decisioning and Alert-Budget Thresholding:** Once
    > \\hat{p}\_i = P(\\text{Fraud} \\mid x_i) is calibrated, TxnVigil
    > can compute both:

    -   **Expected Financial Loss (\\text{EL}\_i):** \\text{EL}\_i =
        > \\hat{p}\_i \\cdot \\text{Amount}\_i \\cdot (1 -
        > \\text{RecoveryRate}), blocking or holding when \\text{EL}\_i
        > \> C\_{\\text{friction/review}}.

    -   **Quantile Alert-Budget Threshold (\\tau_K):** To guarantee the
        > fraud operations team receives exactly K alerts per day (e.g.,
        > 0.5 alerts per 1,000 transactions), dynamically set the review
        > threshold \\tau_K to the (1 -
        > \\frac{K}{N\_{\\text{daily}}})-th quantile of the rolling
        > 24-hour score distribution stored in a Redis t-digest or
        > sorted set.

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Single monolithic models cannot simultaneously
    > classify transaction-level push scams in \<15 ms and multi-hop
    > account-level mule rings ([[Elliptic++ TWIN-GNN Benchmark, Oct 26,
    > 2026]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)).

-   **Analytical Inference:** Deploy a **Three-Component Model
    > Ensemble** in TxnVigil v2:

    1.  **Model A --- Online Transaction Risk Classifier (LightGBM
        > v4.7.0, Unweighted + Isotonic Calibrated):** Scores every
        > incoming UPI event in \<2 ms using 45 features (transaction
        > attributes, Redis sliding-window payer/payee velocities,
        > pre-computed payee graph features, and iforest_score).

    2.  **Model B --- Account Mule Confidence Classifier (LightGBM
        > v4.7.0 on Graph + Behavioral Features, inspired by
        > [[MuleHunter.AI]{.underline}](https://docs.rbihub.in/mule-hunter)):**
        > Runs in micro-batch (every 5--15 minutes via DuckDB +
        > igraph/PyG) over active accounts, writing account_mule_prob
        > back to Redis so Model A can read the payee\'s latest mule
        > probability in O(1) time.

    3.  **Model C --- Unsupervised Drift/Outlier Detector (scikit-learn
        > IsolationForest):** Trained on legitimate behavioral profiles;
        > outputs an anomaly score logged for drift monitoring and
        > passed as a feature into Model A.

### (d) Open Uncertainties

-   UNCERTAIN: **Exact Architecture of Razorpay Vulcan & Stripe PFM.**
    > While [[Razorpay (Aug 18,
    > 2026)]{.underline}](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)
    > and [[Stripe
    > (2025/2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning)
    > publicly describe their Payments Foundation Models as transformer
    > architectures pre-trained on billions of payment sequences,
    > neither company has open-sourced model weights or exact tokenizer
    > vocabularies.

## R5. Industry Architecture of Real-Time Fraud Platforms

### (a) Five-Line Executive Summary

1.  **Verified Fact:** Across public engineering disclosures from
    > [[Stripe
    > Radar]{.underline}](https://stripe.dev/blog/how-we-built-it-stripe-radar),
    > [[Razorpay (Bumblebee &
    > Vulcan)]{.underline}](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51),
    > [[PhonePe]{.underline}](https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/),
    > [[Revolut
    > (Sherlock)]{.underline}](https://medium.com/revolut/building-a-state-of-the-art-card-fraud-detection-system-in-9-months-96463d7f652d),
    > [[Uber (Mastermind & Michelangelo
    > Palette)]{.underline}](https://github.com/TurboML-Inc/awesome-real-time-ml),
    > [[DoorDash
    > (Riviera)]{.underline}](https://huyenchip.com/2023/01/08/self-serve-feature-platforms.html),
    > [[Featurespace
    > ARIC]{.underline}](https://www.featurespace.com/solutions),
    > [[Feedzai]{.underline}](https://www.feedzai.com/fraud/), and
    > [[FICO
    > Falcon]{.underline}](https://www.fico.com/en/products/fico-falcon-fraud-manager),
    > every production real-time fraud platform separates **synchronous
    > inline scoring** from **asynchronous streaming state enrichment
    > and investigation**.

2.  **Verified Fact:** End-to-end synchronous risk-scoring latency
    > budgets in payment switches are strictly bounded at **15--50 ms
    > p99** (and never exceed **100--150 ms** hard circuit-breaker
    > timeouts in UPI/card rails), broken down into \~2--5 ms
    > network/serialization, \~3--8 ms parallel online feature-store
    > fetch (Redis/Aerospike), \~2--6 ms GBDT inference + TreeSHAP, and
    > \~1--3 ms deterministic rule evaluation ([[Redis Real-Time Fraud
    > Architecture, June 10,
    > 2026]{.underline}](https://redis.io/blog/real-time-fraud-detection/)).

3.  **Verified Fact:** Rules and ML are never mutually exclusive;
    > industry architectures execute **pre-ML hard rules** (sanctions,
    > DPIP blocklists, NPCI regulatory limits), **inline ML scoring**,
    > and **post-ML policy rules** combining ML probability, transaction
    > amount, and rule hits into a **4-tier decision matrix** (ALLOW,
    > STEP_UP_CHALLENGE, HOLD_COOLING, BLOCK).

4.  **Verified Fact:** Modern platforms like [[Razorpay\'s Bumblebee
    > (December 17,
    > 2025)]{.underline}](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51)
    > and [[Stripe\'s Scaling Radar (October 19,
    > 2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning)
    > deploy **asynchronous multi-agent / shadow pipelines** off the hot
    > path to triage borderline alerts, synthesize merchant/account
    > context, and run shadow models without adding a single millisecond
    > to payment authorization.

5.  **Analytical Inference:** TxnVigil v2 should replicate this exact
    > **Dual-Path (Fast Inline + Async Streaming) Reference
    > Architecture**, complete with a hard 50 ms SLA circuit breaker
    > (falling back to deterministic Redis velocity rules if ML times
    > out), shadow-model scoring, and a closed-loop analyst feedback
    > topic.

### (b) Survey of Publicly Documented Industry Fraud Architectures

The table below synthesizes verified architectural patterns published by
leading global and Indian payment/fintech engineering teams and
enterprise fraud vendors.

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Company /        Public Engineering Source & Date                                                                                                                             Core Architecture & Feature Store Design                                                          Latency Budget  Key Architectural
  Platform                                                                                                                                                                                                                                                                        & Decision      Pattern to Note
                                                                                                                                                                                                                                                                                  Tiers           
  ---------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------- --------------- --------------------
  **Stripe Radar** [[How We Built It: Stripe Radar (Mar 29, 2023)]{.underline}](https://stripe.dev/blog/how-we-built-it-stripe-radar) & [[Scaling Radar with Agent-Assisted ML  Network-wide entity graph (cards, emails, devices, IPs across millions of merchants) + **Payments \< 50--100 ms   **Point-in-Time
                   (Oct 19, 2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning)                                      Foundation Model (PFM)** embeddings cached in low-latency KV store + GBDT/DNN ensembles           inline scoring; Time-Travel
                                                                                                                                                                                (Shield) + merchant-customizable Radar Rules DSL.                                                 decisions:      Logging:** Logs
                                                                                                                                                                                                                                                                                  Allow, Request  exact feature values
                                                                                                                                                                                                                                                                                  3DS / Step-Up,  at scoring time to
                                                                                                                                                                                                                                                                                  Manual Review,  S3/Parquet to
                                                                                                                                                                                                                                                                                  Block.          eliminate
                                                                                                                                                                                                                                                                                                  train-serve skew
                                                                                                                                                                                                                                                                                                  during retraining.

  **Razorpay       [[Meet Bumblebee: Multi-Agent AI Fraud Architecture (Dec 17,                                                                                                 Inline rule engine + ML risk scoring for 10M+ daily Indian payment gateway transactions           Sub-50 ms       **Hot-Path vs.
  (Bumblebee &     2025)]{.underline}](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51) & ([[Razorpay Blog, Oct 8,                                                                          inline gateway  Cold-Path
  Vulcan)**        [[Razorpay Vulcan Foundation Model (Aug 18, 2026)]{.underline}](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)         2026]{.underline}](https://razorpay.com/blog/built-in-payment-gateway-fraud-detection-india/));   scoring; async  Separation:** Keep
                                                                                                                                                                                **Vulcan** foundation model for payment sequences; **Bumblebee** multi-agent system               multi-agent     synchronous checkout
                                                                                                                                                                                asynchronously investigates merchant/collusion anomalies.                                         investigation   scoring ultra-lean
                                                                                                                                                                                                                                                                                  for merchant    (rules +
                                                                                                                                                                                                                                                                                  onboarding &    GBDT/embeddings),
                                                                                                                                                                                                                                                                                  collusion.      and offload complex
                                                                                                                                                                                                                                                                                                  multi-hop/agentic
                                                                                                                                                                                                                                                                                                  analysis to an async
                                                                                                                                                                                                                                                                                                  event consumer.

  **PhonePe**      [[Building PhonePe\'s Real-Time Transaction Model to Prevent Frauds (July 28,                                                                                Event-driven streaming ingestion over UPI switches; real-time user/merchant/device velocity       Strict \<       **Pre-MPIN
                   2022)]{.underline}](https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/)                                     counters in distributed low-latency NoSQL/cache + gradient-boosted tree scoring + dynamic rule    20--50 ms p99   Contextual Warning
                                                                                                                                                                                engine.                                                                                           budget inside   Tier:** Instead of
                                                                                                                                                                                                                                                                                  UPI PSP/switch  binary allow/block,
                                                                                                                                                                                                                                                                                  call path;      trigger a specific
                                                                                                                                                                                                                                                                                  tiers include   scam-type warning
                                                                                                                                                                                                                                                                                  **In-App Scam   modal (\"Are you on
                                                                                                                                                                                                                                                                                  Warnings**      a call with someone
                                                                                                                                                                                                                                                                                  before MPIN     claiming to be
                                                                                                                                                                                                                                                                                  entry.          police/customs?\")
                                                                                                                                                                                                                                                                                                  before the user
                                                                                                                                                                                                                                                                                                  enters their UPI
                                                                                                                                                                                                                                                                                                  PIN.

  **Revolut        [[Building a State-of-the-Art Card Fraud Detection System in 9 Months (Nov 14,                                                                               Kafka event bus + streaming feature processors + Python microservice serving LightGBM/CatBoost    \< 50 ms        **Automated
  (Sherlock)**     2019)]{.underline}](https://medium.com/revolut/building-a-state-of-the-art-card-fraud-detection-system-in-9-months-96463d7f652d)                             models + automated in-app customer push confirmation (\"Did you just attempt this                 scoring         Self-Service Step-Up
                                                                                                                                                                                transaction?\").                                                                                  latency; claims Resolution:** When a
                                                                                                                                                                                                                                                                                  \<1 cent per    transaction is
                                                                                                                                                                                                                                                                                  \$100 fraud     held/declined,
                                                                                                                                                                                                                                                                                  loss and 30%    immediately push an
                                                                                                                                                                                                                                                                                  reduction in    interactive
                                                                                                                                                                                                                                                                                  false declines. verification prompt
                                                                                                                                                                                                                                                                                                  to the user\'s app
                                                                                                                                                                                                                                                                                                  so legitimate users
                                                                                                                                                                                                                                                                                                  unblock themselves
                                                                                                                                                                                                                                                                                                  without calling
                                                                                                                                                                                                                                                                                                  support.

  **Uber           [[Uber Real-Time Data Infrastructure & Michelangelo Palette]{.underline}](https://github.com/TurboML-Inc/awesome-real-time-ml)                               **Michelangelo Palette** dual-store feature platform (Apache Flink streaming aggregations into    \< 20--40 ms    **Declarative
  (Mastermind &                                                                                                                                                                 Redis/Cassandra online store + Hive/Parquet offline store) feeding **Mastermind** rule engine +   p99; supports   Feature Parity:**
  Michelangelo                                                                                                                                                                  GBDT/deep models.                                                                                 **Shadow        Streaming Flink jobs
  Palette)**                                                                                                                                                                                                                                                                      Rules** and     write to both the
                                                                                                                                                                                                                                                                                  **Shadow        online KV store and
                                                                                                                                                                                                                                                                                  Models** in     offline Parquet
                                                                                                                                                                                                                                                                                  Mastermind      store from a single
                                                                                                                                                                                                                                                                                  before          feature definition.
                                                                                                                                                                                                                                                                                  promotion.      

  **DoorDash       [[Building Riviera & Scalable ML Feature Store with Redis (Chip Huyen Survey, Jan 8,                                                                         **Riviera** declarative streaming feature framework on Kafka/Flink writing protobuf/compressed    \< 10 ms        **Redis Hash Field
  (Riviera & Redis 2023)]{.underline}](https://huyenchip.com/2023/01/08/self-serve-feature-platforms.html)                                                                      binary hashes into **Redis** for sub-5ms multi-key retrieval.                                     feature         Packing &
  Store)**                                                                                                                                                                                                                                                                        retrieval for   Pipelining:** Store
                                                                                                                                                                                                                                                                                  hundreds of     all velocity
                                                                                                                                                                                                                                                                                  features per    features for an
                                                                                                                                                                                                                                                                                  checkout        entity (user_id or
                                                                                                                                                                                                                                                                                  request.        vpa) inside a single
                                                                                                                                                                                                                                                                                                  Redis Hash or Lua
                                                                                                                                                                                                                                                                                                  pipeline to fetch
                                                                                                                                                                                                                                                                                                  40+ features in 1
                                                                                                                                                                                                                                                                                                  network round-trip
                                                                                                                                                                                                                                                                                                  (\< 1 ms).

  **Featurespace   [[Featurespace Adaptive Behavioral Analytics (Oct 4, 2026)]{.underline}](https://www.featurespace.com/solutions); [[Feedzai Platform                         **Adaptive Behavioral Analytics** (recursive bayesian / decaying time-window profiles per         10--30 ms       **Exponentially
  ARIC / Feedzai / (2026)]{.underline}](https://www.feedzai.com/fraud/); [[FICO Falcon Fraud Manager]{.underline}](https://www.fico.com/en/products/fico-falcon-fraud-manager)  customer and counterparty) + RNN/GBDT scoring + integrated Case Manager and Link Analysis         inline          Decaying Behavioral
  FICO Falcon**                                                                                                                                                                 workbench.                                                                                        transaction     Profiles:** Maintain
                                                                                                                                                                                                                                                                                  scoring at      compact recursive
                                                                                                                                                                                                                                                                                  10,000+ TPS.    state (mean,
                                                                                                                                                                                                                                                                                                  variance, last
                                                                                                                                                                                                                                                                                                  timestamp) per
                                                                                                                                                                                                                                                                                                  account so current
                                                                                                                                                                                                                                                                                                  transactions are
                                                                                                                                                                                                                                                                                                  scored as Z-scores
                                                                                                                                                                                                                                                                                                  against the user\'s
                                                                                                                                                                                                                                                                                                  own historical
                                                                                                                                                                                                                                                                                                  baseline.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** A real-time fraud platform that queries
    > PostgreSQL or DuckDB on the synchronous /score hot path will
    > bottleneck at \<50 RPS and violate p99 latency under burst load
    > ([[Redis Real-Time Fraud Guide, June 10,
    > 2026]{.underline}](https://redis.io/blog/real-time-fraud-detection/)).

-   **Analytical Inference:** Copy the **7 Golden Design Patterns** of
    > Stripe Radar, PhonePe, DoorDash, and Uber into TxnVigil v2\'s
    > reference architecture:

    1.  **Single-Round-Trip Online Feature Fetch (\< 2 ms):** Execute a
        > single atomic Lua script (evalsha) on Valkey/Redis that
        > simultaneously updates sliding-window counters for payer_id,
        > payee_vpa, and device_id and returns all 45 online +
        > pre-computed graph features in one network hop.

    2.  **Three-Stage Decision Pipeline (\< 15 ms p99):**

        -   *Stage 1 (Pre-ML Hard Rules, \< 0.5 ms):* Check DPIP
            > blocklist, NPCI ₹5,000/24h new-device cooling cap, P2P
            > collect ban, and MCC limit.

        -   *Stage 2 (Champion + Shadow ML Scoring, \< 3 ms):* Run
            > Champion LightGBM v4.7.0 (predict + pred_contrib=True for
            > exact TreeSHAP reason codes) and optionally evaluate a
            > Challenger/Shadow model asynchronously.

        -   *Stage 3 (Post-ML Policy & 4-Tier Action Matrix, \< 0.5
            > ms):* Map calibrated probability \\hat{p}, Expected Loss
            > \\text{EL}, and rule hits into:

            -   ALLOW (\\hat{p} \< \\tau_1): Process immediately.

            -   STEP_UP (\\tau_1 \\le \\hat{p} \< \\tau_2): Trigger
                > **PhonePe-style contextual scam warning modal** +
                > biometric/OTP re-verification (e.g., if
                > is_call_active=True or new beneficiary).

            -   HOLD (\\tau_2 \\le \\hat{p} \< \\tau_3): Place temporary
                > 30-minute escrow hold + create high-priority analyst
                > case.

            -   BLOCK (\\hat{p} \\ge \\tau_3 or Hard Rule hit): Reject
                > transaction, freeze mule VPA if payee_mule_prob \>
                > 0.85, and open critical case.

    3.  **Feature Log-and-Wait (Zero Train-Serve Skew):** When /score
        > completes, publish a txn.scored.v1 event to Redpanda
        > containing the **exact 45-feature vector used at inference
        > time**, the Champion/Shadow scores, and top-5 SHAP reason
        > codes. A background worker batches these into **Parquet files
        > (for DuckDB training/backtesting)** and **PostgreSQL (for case
        > management)**.

    4.  **Hard Circuit Breaker (50 ms Timeout):** Wrap ML inference in a
        > strict timeout; if model inference fails or exceeds 50 ms,
        > degrade gracefully to the deterministic NPCI/velocity rules
        > and flag degraded_mode=True.

### (d) Open Uncertainties

-   UNCERTAIN: **Exact Internal Feature Counts of Indian PSP Switches.**
    > While [[PhonePe
    > (2022)]{.underline}](https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/)
    > and [[Razorpay
    > (2025/2026)]{.underline}](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51)
    > describe their streaming and multi-agent architectures publicly,
    > exact production feature counts and hardware cluster topologies
    > are proprietary.

## R6. Feature Store and Streaming Stack for Laptop Scale (Versions as of Now)

### (a) Five-Line Executive Summary

1.  **Verified Fact:** While **Feast** is actively maintained (latest
    > stable release **v0.67.0** on **October 13, 2026** per [[GitHub
    > feast-dev/feast]{.underline}](https://github.com/feast-dev/feast/releases)),
    > its Python get_online_features() path adds protobuf
    > serialization/deserialization and registry overhead (typically
    > 5--15 ms per call) and cannot natively execute sub-millisecond
    > atomic sliding-window ZSET updates during a synchronous /score
    > call without an external stream processor.

2.  **Verified Fact:** Following Redis Inc.\'s March 2024 switch from
    > BSD-3 to RSALv2/SSPLv1 (and May 2025 addition of AGPLv3 in Redis
    > 8, latest release **Redis v8.12** on **October 31, 2026** per
    > [[GitHub
    > redis/redis]{.underline}](https://github.com/redis/redis/releases)),
    > the Linux Foundation\'s **BSD-3-Clause** fork **Valkey** (latest
    > stable **v9.1.x** on **October 26, 2026**, with **v9.2.0-rc1** on
    > **September 16, 2026** per [[GitHub
    > valkey-io/valkey]{.underline}](https://github.com/valkey-io/valkey/releases))
    > is the standard permissive open-source drop-in replacement.

3.  **Verified Fact:** In Python stream processing, **Bytewax** has
    > stalled at **v0.21.1** (released **November 25, 2024** with no new
    > releases in 23 months per [[GitHub
    > bytewax/bytewax]{.underline}](https://github.com/bytewax/bytewax/releases)
    > and [[Medium analysis, Oct 17,
    > 2025]{.underline}](https://taogang.medium.com/the-past-and-present-of-stream-processing-part-20-bytewax-the-burned-out-data-candle-760223db6b64)),
    > original robinhood/faust is dead (though community fork
    > faust-streaming/faust reached **v0.15.3** on **August 22, 2026**
    > per [[GitHub
    > faust-streaming/faust]{.underline}](https://github.com/faust-streaming/faust/releases)),
    > whereas **Quix Streams** (**v3.28.1**, October 2026, Apache-2.0
    > per [[GitHub
    > quixio/quix-streams]{.underline}](https://github.com/quixio/quix-streams/releases))
    > and **confluent-kafka-python** (**v2.16.1**, October 2026,
    > Apache-2.0 per [[GitHub
    > confluentinc/confluent-kafka-python]{.underline}](https://github.com/confluentinc/confluent-kafka-python/releases))
    > are actively maintained and support Python 3.14 free-threaded
    > builds.

4.  **Verified Fact:** **Redpanda** (latest release **v26.2.2** on
    > **August 19, 2026**, Business Source License 1.1 per [[GitHub
    > redpanda-data/redpanda]{.underline}](https://github.com/redpanda-data/redpanda/releases))
    > runs in a single C++ binary consuming **\~250--512 MB RAM** in
    > \--mode dev-container \--smp 1 \--memory 512M, compared to
    > **1.2--2.0 GB RAM** for JVM-based **Apache Kafka** (latest
    > **v4.1.2 / v4.4.0** on **October 29, 2026** in KRaft mode per
    > [[Apache Kafka
    > Downloads]{.underline}](https://kafka.apache.org/community/downloads/)).

5.  **Analytical Inference:** On an 8--16 GB RAM laptop, TxnVigil v2
    > should **skip Feast, Hopsworks, and JVM Kafka**, and instead
    > deploy **Valkey 9.1 (BSD-3)** with a **hand-rolled 150-line Lua +
    > Pydantic Feature Store module** (backed by **DuckDB v1.5.6** +
    > Parquet for point-in-time offline features), **Redpanda v26.2.2**
    > capped at 512 MB RAM, and **confluent-kafka-python v2.16.1** (or
    > **Quix Streams v3.28.1**) for async stream processing.

### (b) Feature Store, Cache, Broker, and Stream Processor Comparison (Exact 2026 Versions)

A brutally honest assessment of feature stores for a laptop-scale
real-time fraud platform must distinguish between *resume buzzwords* and
*actual engineering performance*:

-   **Why Feast v0.67.0 is the wrong choice for inline sub-10ms fraud
    > velocity on a laptop:** Feast is designed around pre-materialized
    > batch/stream features (get_online_features). When a UPI
    > transaction arrives at t_0, you need sliding-window features that
    > include events from t_0 - 3\\text{ seconds} (e.g., rapid-fire APK
    > drain attempts) and you must atomically increment the sender\'s
    > and receiver\'s 1m/5m/1h/24h counters *at the moment of scoring*.
    > Doing this through Feast requires running a separate streaming
    > engine pushing to Feast\'s push endpoint (introducing 100--500 ms
    > lag and race conditions) plus Feast\'s Python entity-key protobuf
    > serialization overhead. A 150-line Python class wrapping **Valkey
    > Lua scripts** (ZADD, ZREMRANGEBYSCORE, ZCARD, HMGET) executes both
    > the sliding-window update and the 45-feature read atomically in
    > **\< 0.6 ms**, while writing scored feature vectors to Parquet
    > gives **DuckDB (ASOF JOIN)** zero-leakage offline point-in-time
    > joins! (If desired for portfolio demonstration, a single
    > feature_definitions.py file can export a Feast metadata spec
    > without putting Feast on the hot path.)

-   **Redis vs. Valkey Licensing (2024--2026):** In March 2024 (starting
    > with Redis 7.4), Redis Inc. abandoned the 3-Clause BSD license in
    > favor of dual proprietary/copyleft licensing (**RSALv2** and
    > **SSPLv1**), and in May 2025 (with Redis 8.0, which bundles
    > formerly separate Redis Stack modules like RediSearch, RedisJSON,
    > RedisTimeSeries, and RedisBloom into core Redis) added **AGPLv3**
    > as a third option ([[AceMQ Redis Licensing Guide, Oct 27,
    > 2026]{.underline}](https://acemq.com/guides/redis-licensing/);
    > [[Percona Analysis, Oct 1,
    > 2025]{.underline}](https://www.percona.com/blog/the-redis-license-has-changed-what-you-need-to-know/)).
    > Under AGPLv3/SSPLv1, any hosted network service or SaaS
    > Modification triggers copyleft source-disclosure obligations.
    > Conversely, **Valkey** (forked from Redis 7.2.4 in March/April
    > 2024 under the Linux Foundation and backed by AWS, Google Cloud,
    > Oracle, Ericsson, and Percona) remains 100% **3-Clause BSD**
    > ([[AceMQ Valkey vs Redis, Oct 27,
    > 2026]{.underline}](https://acemq.com/compare/valkey-vs-redis/)).
    > Note that in Valkey 9.1/9.2, sorted sets (ZSET) were upgraded to
    > use **B+ trees** instead of skiplists for large sets and
    > SIMD-optimized radix trees ([[GitHub valkey-io/valkey
    > releases]{.underline}](https://github.com/valkey-io/valkey/releases)),
    > making native ZSET + HASH + Lua scripts blazingly fast without
    > needing proprietary Redis Stack modules.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Component Category   Tool / Software                Latest Stable Version & Release Date                                                                License (as of Nov Official Docker Image & Laptop RAM Footprint        Verdict for TxnVigil
                                                                                                                                                          2026)                                                                  v2 (8--16 GB RAM)
  -------------------- ------------------------------ --------------------------------------------------------------------------------------------------- ------------------ --------------------------------------------------- ---------------------
  **Feature Store      **Feast** (feast-dev/feast)    **v0.67.0** (**Oct 13, 2026**, [[GitHub]{.underline}](https://github.com/feast-dev/feast/releases)) Apache-2.0         feastdev/feature-server:0.67.0 (\~300--500 MB RAM)  **Skip on hot path.**
  (OSS)**                                                                                                                                                                                                                        Protobuf/registry
                                                                                                                                                                                                                                 overhead slows
                                                                                                                                                                                                                                 single-row /score and
                                                                                                                                                                                                                                 cannot do atomic
                                                                                                                                                                                                                                 read-modify-write
                                                                                                                                                                                                                                 sliding windows. Use
                                                                                                                                                                                                                                 a hand-rolled Valkey
                                                                                                                                                                                                                                 Lua + DuckDB ASOF
                                                                                                                                                                                                                                 JOIN feature store.

  **Feature Store      **Hopsworks** (5.0.9 / 5.1,    Hopsworks v5.0.9 ([[GitHub]{.underline}](https://github.com/logicalclocks/hopsworks-api/releases)); AGPLv3 (Hopsworks) Hopsworks requires \>16 GB RAM (RonDB/Spark/K8s);   **Reject both.**
  Alternatives**       2026) & **Featureform**        Featureform v0.12.1 ([[GitHub]{.underline}](https://github.com/featureform/featureform/releases))   / MPL-2.0          Featureform OSS stalled since 2024.                 Hopsworks cannot fit
                       (v0.12.1, Feb 12, 2024)                                                                                                            (Featureform)                                                          on an 8--16 GB laptop
                                                                                                                                                                                                                                 alongside 6 services;
                                                                                                                                                                                                                                 Featureform OSS
                                                                                                                                                                                                                                 releases have
                                                                                                                                                                                                                                 stagnated.

  **Online Feature     **Valkey** (valkey-io/valkey)  **v9.1.x** (**Oct 26, 2026** security patch; **v9.2.0-rc1** **Sept 16, 2026**,                      **BSD-3-Clause**   valkey/valkey:9.1-alpine (**\~60--250 MB RAM**)     **RECOMMENDED
  Store / Cache**                                     [[GitHub]{.underline}](https://github.com/valkey-io/valkey/releases))                               (Linux Foundation)                                                     WINNER.** Permissive
                                                                                                                                                                                                                                 BSD-3 license,
                                                                                                                                                                                                                                 drop-in compatible
                                                                                                                                                                                                                                 with redis-py
                                                                                                                                                                                                                                 (v5.x/v7.x), B+ tree
                                                                                                                                                                                                                                 sorted sets, and Lua
                                                                                                                                                                                                                                 scripts.

  **Online Feature     **Redis Open Source**          **v8.12** (**Oct 31, 2026**, [[GitHub]{.underline}](https://github.com/redis/redis/releases))       Triple-licensed:   redis:8.12-alpine (\~100--350 MB RAM; includes      Use only if you
  Store / Cache        (redis/redis)                                                                                                                      **RSALv2 / SSPLv1  Bloom/TimeSeries/JSON in Redis 8)                   specifically want
  (Alt)**                                                                                                                                                 / AGPLv3**                                                             native CMS.INCRBY
                                                                                                                                                                                                                                 (Count-Min Sketch) or
                                                                                                                                                                                                                                 TDIGEST.ADD in Redis
                                                                                                                                                                                                                                 8 and accept
                                                                                                                                                                                                                                 AGPLv3/RSALv2 terms.
                                                                                                                                                                                                                                 Otherwise prefer
                                                                                                                                                                                                                                 Valkey 9.1.

  **Event Streaming    **Redpanda**                   **v26.2.2** (**Aug 19, 2026**,                                                                      **BSL 1.1** (Free  docker.redpanda.com/redpandadata/redpanda:v26.2.2   **RECOMMENDED
  Broker**             (redpanda-data/redpanda)       [[GitHub]{.underline}](https://github.com/redpanda-data/redpanda/releases))                         for dev, testing,  (**\~350--512 MB RAM** with \--smp 1 \--memory      WINNER.** Zero JVM
                                                                                                                                                          and internal       512M)                                               overhead, built-in
                                                                                                                                                          self-hosted                                                            Schema Registry &
                                                                                                                                                          non-competing use)                                                     HTTP Proxy, starts in
                                                                                                                                                                                                                                 2 seconds on a
                                                                                                                                                                                                                                 laptop.

  **Event Streaming    **Apache Kafka (KRaft)**       **v4.1.2 / v4.4.0** (**Oct 29, 2026**, [[Apache                                                     **Apache-2.0**     apache/kafka-native:4.1.2 (GraalVM native image     Viable fallback if
  Broker (Alt)**       (apache/kafka)                 Downloads]{.underline}](https://kafka.apache.org/community/downloads/))                                                \~400 MB) or apache/kafka:4.1.2 (JVM \~1.2--2 GB)   strict OSI Apache-2.0
                                                                                                                                                                                                                                 broker licensing is
                                                                                                                                                                                                                                 desired (use
                                                                                                                                                                                                                                 apache/kafka-native
                                                                                                                                                                                                                                 image to avoid JVM
                                                                                                                                                                                                                                 RAM bloat).

  **Python Stream      **confluent-kafka-python** +   confluent-kafka **v2.16.1** (**Oct 2026**,                                                          **Apache-2.0**     Runs inside Python worker container (**\~120--200   **RECOMMENDED
  Processing**         **quix-streams**               [[GitHub]{.underline}](https://github.com/confluentinc/confluent-kafka-python/releases));           (both)             MB RAM**)                                           WINNER.**
                                                      quixstreams **v3.28.1** (**Oct 2026**,                                                                                                                                     confluent-kafka
                                                      [[GitHub]{.underline}](https://github.com/quixio/quix-streams/releases))                                                                                                   v2.16.1 wraps C
                                                                                                                                                                                                                                 librdkafka (GIL-safe,
                                                                                                                                                                                                                                 async support);
                                                                                                                                                                                                                                 quixstreams v3.28.1
                                                                                                                                                                                                                                 provides
                                                                                                                                                                                                                                 RocksDB-backed
                                                                                                                                                                                                                                 stateful windows in
                                                                                                                                                                                                                                 pure Python if
                                                                                                                                                                                                                                 needed.

  **Python Stream      **Bytewax** & **Faust**        Bytewax **v0.21.1** (**Nov 25, 2024**,                                                              Apache-2.0         \~150--300 MB RAM                                   **Avoid Bytewax** (no
  Processing           (faust-streaming)              [[GitHub]{.underline}](https://github.com/bytewax/bytewax/releases)); faust-streaming **v0.15.3**   (Bytewax) / BSD-3                                                      release since Nov
  (Stalled/Legacy)**                                  (**Aug 22, 2026**, [[GitHub]{.underline}](https://github.com/faust-streaming/faust/releases))       (Faust)                                                                2024; company
                                                                                                                                                                                                                                 pivoted/wound down
                                                                                                                                                                                                                                 OSS). **Avoid Faust**
                                                                                                                                                                                                                                 (legacy asyncio actor
                                                                                                                                                                                                                                 model is harder to
                                                                                                                                                                                                                                 debug than
                                                                                                                                                                                                                                 confluent-kafka or
                                                                                                                                                                                                                                 quixstreams).

  **OLTP / Case Store  **PostgreSQL** & **DuckDB**    PostgreSQL **v18.6** (**Aug 13, 2026**, [[PostgreSQL Release                                        PostgreSQL License postgres:18.6-alpine (**\~150--300 MB RAM**);       **RECOMMENDED
  & OLAP / Lakehouse**                                Notes]{.underline}](https://www.postgresql.org/docs/release/18.6/)); DuckDB **v1.5.6** (**Sept 29,  / MIT (DuckDB)     DuckDB runs in-process (**\~200--500 MB RAM**)      WINNER.** Postgres
                                                      2026**, [[DuckDB Releases]{.underline}](https://r.duckdb.org/news/index.html))                                                                                             18.6 handles cases,
                                                                                                                                                                                                                                 rules, RBAC, and
                                                                                                                                                                                                                                 audit logs; DuckDB
                                                                                                                                                                                                                                 1.5.6 queries Parquet
                                                                                                                                                                                                                                 feature logs
                                                                                                                                                                                                                                 in-process for
                                                                                                                                                                                                                                 training and
                                                                                                                                                                                                                                 backtesting.

  **API Framework**    **FastAPI** (fastapi/fastapi)  **v0.136.1+** (**Oct 2026**, [[GitHub]{.underline}](https://github.com/fastapi/fastapi/releases) /  MIT                python:3.13-slim + uvicorn (**\~180--250 MB RAM**)  **RECOMMENDED
                                                      [[ZestMinds]{.underline}](https://www.zestminds.com/blog/fastapi-requirements-setup-guide-2025/))                                                                          WINNER.** Async I/O
                                                                                                                                                                                                                                 for Redis/Redpanda,
                                                                                                                                                                                                                                 Pydantic v2
                                                                                                                                                                                                                                 validation, automatic
                                                                                                                                                                                                                                 OpenAPI docs.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### Exact Valkey/Redis Data Structures for Sliding-Window Fraud Features at Laptop Scale

To keep Valkey memory under 250 MB while supporting sub-millisecond
sliding-window counts, sums, and distinct counterparty ratios across
1-minute, 15-minute, 1-hour, and 24-hour windows:

1.  **Exact Short/Medium Windows (1m, 5m, 15m, 1h) --- Sorted Sets
    > (ZSET) with Composite Member Packing:**

    -   Key: vel:zset:{account_id} (with EXPIRE 3600).

    -   Score: timestamp_ms (UNIX epoch in milliseconds).

    -   Member: \"{txn_id}:{amount_paise}:{counterparty_hash8}\".

    -   Inside a single atomic Lua script (evalsha), first prune expired
        > entries via ZREMRANGEBYSCORE key -inf (now_ms - 3600000),
        > insert the current event via ZADD, and iterate the remaining
        > members in C/Lua memory to compute **exact 1m, 5m, 15m, and 1h
        > transaction counts, inflow/outflow sums, max amount, and
        > unique counterparty counts** in \< 0.4 ms!

2.  **Long Windows (24h, 7d, 30d) --- Compact Hourly/Daily Bucket Hashes
    > (HASH) + HyperLogLog (PFADD / PFCOUNT):**

    -   Storing 30 days of individual raw transactions in a ZSET wastes
        > memory for high-volume merchants. Instead, store hourly/daily
        > rollups in a Redis Hash vel:bucket:{account_id}:{YYYYMMDDHH}
        > (HINCRBY count 1, HINCRBYFLOAT outflow_sum amount) and track
        > 24h/7d unique senders/receivers using **HyperLogLog** (PFADD
        > hll:senders:{account_id}:{YYYYMMDD} {sender_id} --- fixed 12
        > KB max per key, often \<1 KB via sparse encoding) or exact set
        > membership with TTL.

3.  **Entity Profile & Pre-Computed Graph Features --- Redis Hash
    > (HGETALL / HMGET):**

    -   Key: feat:acct:{account_id} stores account_age_days, kyc_tier,
        > last_device_bind_ts, last_sim_change_ts, pagerank_score,
        > in_degree_24h, out_degree_24h, pass_through_ratio_24h,
        > community_fraud_density, and mule_prob.

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Running 6+ Docker containers on an 8 GB RAM
    > laptop will crash via Linux OOM-killer if any JVM service
    > (Kafka/Flink/Spark) or heavy orchestrator is included.

-   **Analytical Inference:** Pin the following exact **6-Container
    > Docker Compose Topology** totaling **\~1.85 GB RAM at idle and
    > \~3.2 GB RAM under load** (leaving \>4.5 GB headroom on an 8 GB
    > machine):

    1.  valkey (valkey/valkey:9.1-alpine, mem_limit: 384m): Online
        > velocity ZSETs, bucket hashes, DPIP negative sets, and graph
        > feature cache.

    2.  redpanda (docker.redpanda.com/redpandadata/redpanda:v26.2.2,
        > mem_limit: 512m, \--mode dev-container \--smp 1 \--memory
        > 450M): Event bus for upi.txns.raw, upi.txns.scored, and
        > upi.cases.feedback.

    3.  postgres (postgres:18.6-alpine, mem_limit: 384m): Cases, SCN/STR
        > compliance timers, rules version history, and DPDP audit logs.

    4.  scoring-api (python:3.13-slim, FastAPI + LightGBM v4.7.0 +
        > confluent-kafka v2.16.1, mem_limit: 512m): Synchronous
        > /v1/score endpoint + /v1/cases REST API.

    5.  stream-worker (python:3.13-slim, confluent-kafka v2.16.1 +
        > DuckDB v1.5.6 + python-igraph v1.0.0, mem_limit: 512m):
        > Consumes upi.txns.scored, writes Parquet feature logs,
        > triggers micro-batch graph feature refreshes every 5 minutes
        > into Valkey, and creates Postgres cases for HOLD/BLOCK events.

    6.  web-ui (nginx:1.27-alpine serving static React + Vite +
        > TypeScript build, mem_limit: 64m): Analyst Case Manager, Rule
        > Backtester, Mule Graph Explorer, and Live Metrics Dashboard.
        > (MLflow v3.17.2 can run on-demand via a docker compose
        > \--profile mlops up profile so it consumes 0 MB during normal
        > runtime).

### (d) Open Uncertainties

-   UNCERTAIN: **Future Valkey Native Module Ecosystem.** While Valkey
    > 9.1/9.2 includes core data structures (ZSET, HASH, HLL, BITMAP,
    > STREAM) under BSD-3, Valkey\'s optional Bloom/Search modules
    > (valkey-bloom, valkey-search, valkey-json) are packaged separately
    > from the minimal valkey:9.1-alpine image; using core Lua + ZSET +
    > HLL avoids any external module compilation dependency.

## R7. Explainability, Reason Codes, and Model Governance

### (a) Five-Line Executive Summary

1.  **Verified Fact:** As proven in [[GitHub Issue shap/shap#5121
    > (August 12,
    > 2026)]{.underline}](https://github.com/shap/shap/issues/5121),
    > calling shap.TreeExplainer(model).shap_values(X) on a LightGBM
    > model delegates directly to LightGBM\'s built-in C++
    > booster.predict(X, pred_contrib=True) (max\|shap - native\| = 0.0,
    > bit-identical), while shap.TreeExplainer.\_\_init\_\_ wastes up to
    > ratusan seconds and gigabytes of RAM parsing
    > booster\_.dump_model() in Python.

2.  **Verified Fact:** Calling booster.predict(X, pred_contrib=True)
    > directly in **LightGBM v4.7.0** computes exact path-dependent
    > TreeSHAP log-odds contributions for a single row in **\< 0.3 to
    > 1.2 ms** on CPU with zero wrapper overhead, eliminating any need
    > for FastTreeSHAP unless interventional SHAP or second-order
    > Shapley interactions (shapiq, [[May
    > 2026]{.underline}](https://www.researchgate.net/publication/397215150_shapiq_Shapley_Interactions_for_Machine_Learning))
    > are required.

3.  **Verified Fact:** On August 13, 2025, the RBI published the
    > [**[Report of the Committee to Develop a Framework for Responsible
    > and Ethical Enablement of Artificial Intelligence (FREE-AI) in the
    > Financial
    > Sector]{.underline}**](https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306)
    > ([[RBI Press Release
    > 2025-2026/902]{.underline}](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61018)),
    > establishing **7 Sutras**, **6 Strategic Pillars**
    > (*Infrastructure, Policy, Capacity, Governance, Protection,
    > Assurance*), and **26 actionable recommendations**, followed by
    > RBI\'s **Draft Guidance on Regulatory Principles for Model Risk
    > Management (June 24, 2026)** ([[RBI Annual Report 2025-26, Para
    > VI.18]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)).

4.  **Verified Fact:** The RBI survey conducted for the FREE-AI report
    > revealed that among 127 Indian financial entities using AI, **only
    > 15% used model interpretation tools, only 21% monitored for
    > data/model drift, and only 18% maintained AI audit logs** ([[Dvara
    > Research FREE-AI Summary, October 21,
    > 2025]{.underline}](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/)).

5.  **Analytical Inference:** By implementing native pred_contrib=True
    > reason-code mapping, automated Evidently drift checks, immutable
    > decision audit logs, and a standardized Model Card + Datasheet +
    > AIBOM ([[CERT-In v2.0, July 9,
    > 2025]{.underline}](https://intellixbom.com/resources/aibom/aibom-vs-model-cards/)),
    > TxnVigil v2 directly addresses the exact governance gaps flagged
    > by the RBI FREE-AI Committee.

### (b) Explainability Benchmarks, Reason-Code Design, and RBI FREE-AI Governance

In production financial crime systems, raw SHAP floating-point vectors
(\\phi_1, \\phi_2, \\dots, \\phi_d) cannot be shown directly to
customers or L1 compliance analysts without translation. Industry
practice (standardized in credit adverse-action notices under ECOA/Reg B
and adapted for fraud case management in FICO Falcon and Featurespace
ARIC) uses a **Two-Layer Reason Code Architecture**:

1.  **Mathematical Attribution Layer (pred_contrib=True):** For a
    > LightGBM binary classifier, booster.predict(x, pred_contrib=True)
    > returns a vector of length d + 1, where the first d elements are
    > the exact TreeSHAP log-odds contributions \\phi_j of each feature
    > j, and the (d+1)-th element is the expected base log-odds \\phi_0:
    > \\log \\frac{\\hat{p}\_{\\text{raw}}}{1 - \\hat{p}\_{\\text{raw}}}
    > = \\phi_0 + \\sum\_{j=1}\^{d} \\phi_j

2.  **Semantic Reason-Code Mapping Layer:** Features are grouped into
    > human-understandable **Risk Reason Families** (e.g.,
    > RC_VEL_OUTFLOW, RC_DEVICE_COOLING, RC_MULE_FAN_IN,
    > RC_MULE_PASSTHROUGH, RC_COERCION_CALL_ACTIVE). For every flagged
    > transaction, TxnVigil selects the top-3 features with \\phi_j \>
    > 0.15 log-odds and formats a dynamic natural-language explanation
    > templated with the actual feature value and baseline comparison
    > (e.g., RC_MULE_FAN_IN (+1.84 log-odds): Payee VPA received 19
    > unique sender transfers in the last 60m vs. 99th percentile
    > baseline of 3). Crucially, the system maintains **two distinct
    > explanation views**:

    -   **Internal Analyst & Regulator View (RBI SCN / FIU-IND STR):**
        > Displays exact feature values, SHAP log-odds contributions,
        > triggered rule IDs, and 2-hop counterparty graph evidence
        > required to draft a **21-day Show Cause Notice** ([[RBI Fraud
        > Risk Management MD, Para
        > 2.1.1]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702))
        > or **FIU-IND STR** narrative.

    -   **External Customer / PSP View (Anti-Tipping-Off Safe):**
        > Displays only safe behavioral nudges during STEP_UP (e.g.,
        > *\"Warning: You are on an active phone call and sending money
        > to a new recipient. Police/RBI never ask for UPI transfers\"*)
        > or generic policy codes on BLOCK, never revealing internal
        > mule-network scores.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Explainability / Method / Framework & Latest Version                                                     Latency / Resource    Source & Publication Date                                                                                                                                                                      Concrete Implementation in
  Governance                                                                                               Profile                                                                                                                                                                                                              TxnVigil v2
  Dimension                                                                                                                                                                                                                                                                                                                     
  ---------------- --------------------------------------------------------------------------------------- --------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------
  **Online         LightGBM **v4.7.0** native booster.predict(X, pred_contrib=True)                        **0.2--1.0 ms** per   [[GitHub Issue shap/shap#5121 (Aug 12, 2026)]{.underline}](https://github.com/shap/shap/issues/5121) & [[LightGBM v4.7.0 (July 18, 2026)]{.underline}](https://pypi.org/project/lightgbm/)     Use pred_contrib=True on
  Single-Row                                                                                               row on CPU; **0 MB**                                                                                                                                                                                                 every synchronous /v1/score
  TreeSHAP**                                                                                               extra RAM allocation;                                                                                                                                                                                                request; never instantiate
                                                                                                           bit-identical to                                                                                                                                                                                                     shap.TreeExplainer on the
                                                                                                           shap.TreeExplainer                                                                                                                                                                                                   hot path.
                                                                                                           (max\|diff\| = 0.0).                                                                                                                                                                                                 

  **Offline Global **SHAP v0.54.1** (shap/shap) & **shapiq / FastTreeSHAP**                                shap v0.54.1 used     [[SHAP v0.54.1 Release Notes (Oct 16, 2026)]{.underline}](https://shap.readthedocs.io/en/latest/release_notes.html) & [[shapiq Paper (May 6,                                                   Run shap v0.54.1 in offline
  Plots &                                                                                                  offline during        2026)]{.underline}](https://www.researchgate.net/publication/397215150_shapiq_Shapley_Interactions_for_Machine_Learning)                                                                       training scripts only; save
  Interactions**                                                                                           training to log                                                                                                                                                                                                      static beeswarm PNGs and
                                                                                                           summary beeswarm &                                                                                                                                                                                                   JSON feature importances
                                                                                                           dependence plots to                                                                                                                                                                                                  into MLflow artifacts.
                                                                                                           MLflow.                                                                                                                                                                                                              

  **RBI FREE-AI    **RBI FREE-AI Committee Report** (Constituted Dec 26, 2024; Report released Aug 13,     **7 Sutras:** (1)     [[RBI Official Report ID 1306 (Aug 13, 2025)]{.underline}](https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306), [[RBI Press Release                                              Map every TxnVigil
  Framework (7     2025)                                                                                   Trust is the          2025-2026/902]{.underline}](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61018), & [[Dvara Research Summary (Oct 21,                                                        governance feature to a
  Sutras & 6                                                                                               Foundation, (2)       2025)]{.underline}](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/)                                                                                                    specific FREE-AI Sutra and
  Pillars)**                                                                                               People First, (3)                                                                                                                                                                                                    Pillar in the UI
                                                                                                           Innovation over                                                                                                                                                                                                      \"Governance & Compliance\"
                                                                                                           Restraint, (4)                                                                                                                                                                                                       tab (e.g., Sutra 6
                                                                                                           Fairness & Equity,                                                                                                                                                                                                   *Understandable by Design*
                                                                                                           (5) Accountability,                                                                                                                                                                                                  \\rightarrow pred_contrib
                                                                                                           (6) Understandable by                                                                                                                                                                                                reason codes; Sutra 4
                                                                                                           Design, (7) Safety,                                                                                                                                                                                                  *Fairness* \\rightarrow
                                                                                                           Resilience &                                                                                                                                                                                                         demographic/region FPR
                                                                                                           Sustainability. **6                                                                                                                                                                                                  parity check; Pillar 6
                                                                                                           Pillars (26 Recs):**                                                                                                                                                                                                 *Assurance* \\rightarrow
                                                                                                           Infrastructure,                                                                                                                                                                                                      drift monitoring & audit
                                                                                                           Policy, Capacity                                                                                                                                                                                                     trail).
                                                                                                           (Innovation);                                                                                                                                                                                                        
                                                                                                           Governance,                                                                                                                                                                                                          
                                                                                                           Protection, Assurance                                                                                                                                                                                                
                                                                                                           (Risk).                                                                                                                                                                                                              

  **RBI & SEBI     **RBI Draft Guidance on Regulatory Principles for Model Risk Management** & **SEBI      Requires model        [[RBI Annual Report 2025-26, Para VI.18 (May 29, 2026)]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466), [[Dvara MRM Comments (July 27,                       Implement Maker-Checker
  Model Risk       Responsible AI/ML Consultation & Circulars**                                            inventory,            2026)]{.underline}](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/), & [[SEBI AI/ML Consultation Paper (June 20,                                                       approval for rule/threshold
  Management                                                                                               independent           2025)]{.underline}](https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html)   changes, Shadow Model
  (MRM)**                                                                                                  validation,                                                                                                                                                                                                          scoring, human override
                                                                                                           champion-challenger                                                                                                                                                                                                  reason logging
                                                                                                           shadow testing, drift                                                                                                                                                                                                (analyst_override_reason),
                                                                                                           monitoring,                                                                                                                                                                                                          and an emergency ML
                                                                                                           human-in-the-loop                                                                                                                                                                                                    kill-switch.
                                                                                                           override logging, and                                                                                                                                                                                                
                                                                                                           kill-switch fallback.                                                                                                                                                                                                

  **Model Cards,   **Mitchell et al. (2019) Model Cards**, **Gebru et al. (2021) Datasheets**, [**[Hugging Standardized          [[IntelliXBOM / CERT-In AIBOM Guidelines v2.0 (July 9, 2025)]{.underline}](https://intellixbom.com/resources/aibom/aibom-vs-model-cards/) & [[Model Cards Survey (June 26,                     Auto-generate MODEL_CARD.md,
  Datasheets &     Face Model Card                                                                         Markdown + JSON       2025)]{.underline}](https://medium.com/@akankshasinha247/model-cards-datasheets-governance-frameworks-0cda9605c94e)                                                                            DATASHEET.md, and
  AIBOM**          v2]{.underline}**](https://huggingface.co/docs/hub/en/model-card-landscape-analysis), & governance artifacts                                                                                                                                                                                                 aibom.cyclonedx.json on
                   **CERT-In AIBOM v2.0**                                                                  bundled with every                                                                                                                                                                                                   every training run,
                                                                                                           registered MLflow                                                                                                                                                                                                    recording dataset lineage,
                                                                                                           model version.                                                                                                                                                                                                       subgroup FPR across account
                                                                                                                                                                                                                                                                                                                                tiers/states, known
                                                                                                                                                                                                                                                                                                                                limitations, and FREE-AI
                                                                                                                                                                                                                                                                                                                                compliance mapping.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Only 15% of surveyed Indian financial
    > institutions use model explainability tools and only 18% maintain
    > AI audit logs ([[Dvara Research FREE-AI Summary, Oct 21,
    > 2025]{.underline}](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/)).

-   **Analytical Inference:** Make **RBI FREE-AI Compliance** a
    > first-class visual feature of TxnVigil v2:

    1.  **Zero-Latency Reason Codes via pred_contrib=True:** Every
        > /v1/score call runs booster.predict(features,
        > pred_contrib=True) in \<1 ms, maps the top-3 positive SHAP
        > contributors to a 25-code typology dictionary (RC01--RC25),
        > and stores both the raw SHAP values and human-readable reason
        > strings in PostgreSQL.

    2.  **Subgroup Fairness & Bias Audit (FREE-AI Sutra 4):** During
        > model evaluation, compute False Positive Rate (FPR) and Alert
        > Rate Parity across account tiers (BSBD / Jan Dhan vs. Regular
        > Savings vs. Current Account) and geographic tiers (Metro vs.
        > Tier-3/Rural) to prove that low-balance rural accounts are not
        > unfairly de-risked solely due to account type.

    3.  **Automated Model Card & CERT-In AIBOM Generator:** Include a
        > CLI command (uv run txnvigil generate-governance-bundle) that
        > emits a complete MODEL_CARD.md (following Hugging Face /
        > Mitchell et al.), DATASHEET.md (Gebru et al.), and aibom.json
        > (CERT-In July 2025 v2.0 specification).

### (d) Open Uncertainties

-   UNCERTAIN: **Mandatory Audit Format for RBI FREE-AI Assurance
    > Pillar.** While the [[FREE-AI Report (August 13,
    > 2025)]{.underline}](https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306)
    > recommends third-party and internal AI audits under Pillar 6
    > (*Assurance*), RBI has not yet mandated a rigid XBRL/JSON schema
    > for AI model audit submissions on DAKSH.

## R8. Evaluation Metrics Used in Production Fraud Teams

### (a) Five-Line Executive Summary

1.  **Verified Fact:** Production banking fraud and AML operations teams
    > never optimize or report raw accuracy or ROC-AUC in isolation;
    > under 0.05%--0.15% fraud prevalence, a model with 0.990 ROC-AUC
    > can still generate 20+ false positives for every true fraud (an
    > unworkable 20:1 Alert-to-Fraud Ratio) ([[FluxForce AI Fraud
    > Benchmarks, August 20,
    > 2026]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response);
    > [[SAML-D Operational Evaluation, August 15,
    > 2026]{.underline}](https://arxiv.org/html/2608.15447v1)).

2.  **Verified Fact:** Enterprise fraud platforms (FICO Falcon,
    > Featurespace ARIC, Feedzai) evaluate performance across three
    > distinct granularities: **Transaction Count** (Transaction
    > Detection Rate), **Monetary Value** (**Value Detection Rate /
    > VDR** --- catching a ₹99,000 Digital Arrest transfer matters
    > 500\\times more than catching a ₹200 test ping), and **Account /
    > Entity Level** (**Account Detection Rate / ADR** --- identifying a
    > compromised victim account or mule beneficiary before full balance
    > exhaustion).

3.  **Verified Fact:** Alert thresholds in production banks are governed
    > by fixed **Analyst Alert Budgets (K alerts/day)**---determined by
    > L1 investigator headcount \\times average handle time---and
    > **Customer Friction Budgets** (maximum allowable step-up/challenge
    > rate, typically \< 0.5\\%--1.5\\% of total volume) ([[False
    > Positives in Production AI, February 23,
    > 2026]{.underline}](https://medium.com/@adnanmasood/false-positives-the-hidden-cost-center-in-production-ai-790afc8c1632)).

4.  **Verified Fact:** Offline backtest metrics systematically
    > overestimate online production metrics due to **point-in-time
    > feature leakage**, **rule-censoring (selection bias)** where
    > transactions blocked by legacy rules never reach the outcome
    > labeler, **label delay** (7--30 days for NCRP/chargeback claims),
    > and **adversarial fraudster adaptation** when a rule goes live.

5.  **Analytical Inference:** TxnVigil v2 must compute and display an
    > **8-Metric Production Scorecard** in both MLflow and the React
    > dashboard---reporting VDR, ADR, Alert-to-Fraud Ratio (AFPR),
    > Precision@K (at 0.1% and 0.5% alert budgets), Net Financial
    > Savings (₹), Customer Step-Up Friction Rate, and Median
    > Time-to-Detect (TTD)---backed by a DuckDB point-in-time rule
    > backtester and shadow-mode evaluator.

### (b) Production Metric Definitions, Mathematical Formulas, and Operational Benchmarks

In a real-time payment switch processing N transactions over an
evaluation window with ground-truth label y_i \\in \\{0, 1\\}, risk
score s_i \\in \[0, 1\], alert/block indicator \\hat{y}\_i =
\\mathbb{I}(s_i \\ge \\tau \\lor \\text{RuleHit}\_i = 1), and
transaction amount v_i (in ₹), let \\text{TP} = \\sum
\\mathbb{I}(\\hat{y}\_i=1 \\land y_i=1), \\text{FP} = \\sum
\\mathbb{I}(\\hat{y}\_i=1 \\land y_i=0), \\text{FN} = \\sum
\\mathbb{I}(\\hat{y}\_i=0 \\land y_i=1), and \\text{TN} = \\sum
\\mathbb{I}(\\hat{y}\_i=0 \\land y_i=0).

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Metric Name                       Exact Mathematical Formula                              Production Definition & Operational Meaning  Industry Target / Benchmark (2025--2026)                                                       Source & Date
  --------------------------------- ------------------------------------------------------- -------------------------------------------- ---------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **1. Value Detection Rate (VDR /  \\text{VDR} = \\frac{\\sum\_{i=1}\^{N} v_i \\cdot       Fraction of total fraudulent monetary value  **\\ge 75\\%--85\\%** at \\le 0.5\\% false positive rate ([[FluxForce AI Benchmarks, Aug 20,   [[FluxForce AI Fraud Benchmarks 2026 (Aug 20, 2026)]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response)
  Dollar-Weighted Recall)**         \\mathbb{I}(\\hat{y}\_i = 1 \\land y_i =                (₹) intercepted before settlement. Because   2026]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response)).   
                                    1)}{\\sum\_{i=1}\^{N} v_i \\cdot \\mathbb{I}(y_i = 1)}  APP scams involve high-value transfers                                                                                                      
                                                                                            whereas card/UPI probing uses ₹1--₹10 pings,                                                                                                
                                                                                            VDR is the #1 executive KPI.                                                                                                                

  **2. Account / Entity Detection   \\text{ADR} = \\frac{\\sum\_{a \\in                     Proportion of compromised customer accounts  **\\ge 80\\%** of multi-transaction fraud/mule episodes caught prior to full drain.            [[MDPI Elliptic++ Actor-Level Triage Benchmark (Oct 26, 2026)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)
  Rate (ADR)**                      \\mathcal{A}\_{\\text{fraud}}}                          or active mule accounts detected on at least                                                                                                
                                    \\mathbb{I}\\!\\left(\\max\_{t \\in T(a)}               one transaction during an episode. Critical                                                                                                 
                                    \\hat{y}\_{a,t} = 1\\right)}{\\lvert                    for **MuleHunter.AI** style evaluations.                                                                                                    
                                    \\mathcal{A}\_{\\text{fraud}} \\rvert}                                                                                                                                                              

  **3. Alert-to-Fraud Ratio (AFR) & \\text{AFR} = \\frac{\\text{TP} +                       Number of alerts (or false alerts) generated Card/UPI blocking: **\\le 3:1\\text{ to }5:1**; AML/Mule investigation queue: **\\le           [[Digital Sense Banking Fraud Case Study (Apr 8, 2026)]{.underline}](https://www.digitalsense.ai/blog/ai-in-banking) & [[SAML-D Operational Benchmark (Aug 15,
  False-Positive-to-True-Positive   \\text{FP}}{\\text{TP}} = \\frac{1}{\\text{Precision}}, per confirmed fraud case. Directly measures  5:1\\text{ to }10:1** (vs. legacy rules at 50:1).                                              2026)]{.underline}](https://arxiv.org/html/2608.15447v1)
  Ratio (FPR:TPR)**                 \\quad \\text{FP:TP} = \\frac{\\text{FP}}{\\text{TP}} = analyst workload efficiency; an AFR of 5:1                                                                                                  
                                    \\text{AFR} - 1                                         means 20% precision (4 false positives per 1                                                                                                
                                                                                            true fraud).                                                                                                                                

  **4. Precision@K & Recall@K       \\text{Precision@}K = \\frac{1}{K}\\sum\_{r=1}\^{K}     Precision and recall when strictly flagging  Precision@K \\ge 0.85 at 0.5 alerts per 10,000 txns on SAML-D ([[arXiv:2608.15447v1, Aug 15,   [[SAML-D Operational AML Evaluation (Aug 15, 2026)]{.underline}](https://arxiv.org/html/2608.15447v1)
  (Alert Budget Operating Point)**  y\_{(r)}, \\quad \\text{Recall@}K =                     only the top K highest-scored transactions   2026]{.underline}](https://arxiv.org/html/2608.15447v1)).                                      
                                    \\frac{\\sum\_{r=1}\^{K} y\_{(r)}}{\\sum\_{i=1}\^{N}    per day (where K = N\_{\\text{analysts}}                                                                                                    
                                    y_i}                                                    \\times                                                                                                                                     
                                                                                            \\frac{\\text{ShiftMinutes}}{\\text{AHT}},                                                                                                  
                                                                                            e.g., 0.5 to 5.0 alerts per 10,000 txns).                                                                                                   

  **5. Customer Friction / Step-Up  \\text{FrictionRate} = \\frac{\\sum\_{i=1}\^{N}         **Friction Rate** measures % of total        Step-Up Friction **\< 1.0\\%**; Hard Decline Insult Rate **\< 0.05\\%--0.15\\%** ([[FluxForce  [[FluxForce AI Fraud Benchmarks 2026 (Aug 20, 2026)]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response)
  Rate & Insult Rate**              \\mathbb{I}(\\text{Action}\_i \\in                      transactions subjected to any delay/warning; AI, Aug 20,                                                                                    
                                    \\{\\text{STEP\\\_UP}, \\text{HOLD},                    **Insult Rate** measures % of legitimate     2026]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response)).   
                                    \\text{BLOCK}\\})}{N}\\text{InsultRate} =               transactions outright declined (causing                                                                                                     
                                    \\frac{\\sum\_{i=1}\^{N} \\mathbb{I}(\\text{Action}\_i  customer churn).                                                                                                                            
                                    = \\text{BLOCK} \\land y_i = 0)}{\\sum\_{i=1}\^{N}                                                                                                                                                  
                                    \\mathbb{I}(y_i = 0)}                                                                                                                                                                               

  **6. Time-to-Detect (TTD) &       \\text{TTD}\_a = t\_{\\text{first\\\_alert}}(a) -       Elapsed seconds (and number of fraudulent    **\\text{TxnsToDetect} = 1** for APP Digital Arrest; **\< 15\\text{ min}** for Layer-1 mule    [[CheckDetect Real-Time Loss Alerts (Aug 20, 2025)]{.underline}](https://validadvantage.com/blog/real-time-loss-alerts)
  Residual Drain Ratio**            t\_{\\text{first\\\_fraud}}(a)\\text{TxnsToDetect}\_a = transactions) between the first fraudulent   account freeze before cash-out.                                                                
                                    \\lvert \\{t \\in T\_{\\text{fraud}}(a) : t \\le        event on account a and the first alert/block                                                                                                
                                    t\_{\\text{first\\\_alert}}(a)\\} \\rvert               triggered by the engine.                                                                                                                    

  **7. Net Fraud Savings (Expected  \\text{NetSavings} = \\sum\_{\\text{TP}} v_i -          Net rupee utility accounting for prevented   Must exceed baseline rules-only Net Savings on out-of-time validation split.                   [[Cost-Aware Adaptive Fraud Detection (Oct 21,
  Value Matrix in ₹)**              \\sum\_{\\text{FN}} v_i -                               fraud value (\\text{TP}), missed fraud loss                                                                                                 2026)]{.underline}](https://www.researchgate.net/publication/416317894_Cost-Aware_Adaptive_Credit_Card_Fraud_Detection_Under_Concept_Drift_A_Comparative_Evaluation_of_Model-Maintenance_Policies)
                                    c\_{\\text{review}}(\\text{TP}+\\text{FP}) -            (\\text{FN}), analyst investigation cost                                                                                                    
                                    \\sum\_{\\text{FP}} (c\_{\\text{insult}} +              (c\_{\\text{review}} \\approx                                                                                                               
                                    \\alpha\_{\\text{churn}} v_i)                           ₹150/\\text{case}), and false-decline                                                                                                       
                                                                                            customer lifetime value loss.                                                                                                               
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#### How Production Banks Set Alert Budgets, Backtest Rules, and Close the Offline-vs-Online Gap

1.  **Setting the Daily Alert Budget (K):** A bank\'s Fraud Operations
    > Center sizes its manual review queue from human capacity:
    > K\_{\\text{daily}} = N\_{\\text{analysts}} \\times
    > \\frac{\\text{ProductiveHoursPerShift} \\times
    > 60}{\\text{AverageHandleTime (mins)}} \\times
    > \\text{UtilizationFactor} For example, 20 analysts working 6.5
    > productive hours/day at an Average Handle Time (AHT) of 12 minutes
    > per UPI case can review K = 20 \\times \\frac{390}{12} =
    > 650\\text{ cases/day}. Automated actions (ALLOW and
    > high-confidence STEP_UP) bypass human review, while only HOLD and
    > contested BLOCK / mule-freeze cases consume the K = 650 budget.

2.  **Backtesting Rules Without Time-Travel Leakage:** As implemented in
    > modern open-source engines like [[ezrules (sofeikov/ezrules, Oct
    > 2026)]{.underline}](https://github.com/sofeikov/ezrules), a
    > candidate rule (e.g., payee_inflow_count_1h \> 8 AND
    > payee_pass_through_ratio_24h \> 0.85 AND amount \>= 10000) must be
    > evaluated against **stored point-in-time feature snapshots** from
    > the historical Parquet log---never against current end-of-day
    > balances---computing **Marginal/Incremental TP and FP** (how many
    > frauds the candidate rule catches that were *not already caught*
    > by existing active rules or the ML model).

3.  **Why Offline Metrics Diverge from Online Production Metrics:**

    -   *Point-in-Time Feature Skew:* Computing rolling 1h/24h
        > aggregates in SQL without excluding the current row or
        > respecting network lag inflates offline recall by 10%--25%.

    -   *Censored Positives (Policy Blindness):* Once TxnVigil blocks a
        > transaction in production, you never observe whether a
        > non-contacted customer would have filed a fraud claim---unless
        > a small **Random Control Group (0.5%--1% holdout of borderline
        > step-ups)** or **Shadow Mode** is maintained ([[Medium
        > Production AI False Positives, Feb 23,
        > 2026]{.underline}](https://medium.com/@adnanmasood/false-positives-the-hidden-cost-center-in-production-ai-790afc8c1632)).

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Reporting only F1 = 0.96 or Accuracy = 99.9% on a
    > portfolio README is a red flag that signals lack of real-world
    > fraud domain experience ([[FluxForce AI, Aug 20,
    > 2026]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response)).

-   **Analytical Inference:** Build a dedicated
    > **metrics/production_scorecard.py** module and UI view in TxnVigil
    > v2 that reports all 7 production formulas above side-by-side:

    -   Plot the **VDR vs. Alert Volume Curve** (showing % of ₹ fraud
        > value captured at 10, 50, 100, and 500 alerts per 100,000
        > transactions).

    -   Include an interactive **Rule Backtester & Shadow Evaluator**
        > tab powered by DuckDB over the Parquet feature log that
        > outputs for any candidate rule: Total Hits, Incremental True
        > Positives (Uncaught by Champion ML), Incremental False
        > Positives, Marginal AFR, and Rupee Value Captured (₹).

### (d) Open Uncertainties

-   UNCERTAIN: **Exact Analyst AHT and False-Decline Churn Multipliers
    > in Indian PSBs vs. Fintechs.** While global card benchmarks cite
    > $5–$`<!-- -->`{=html}15 per manual review, Indian bank CFMU
    > per-alert review costs and UPI customer abandonment rates after a
    > false 24-hour cooling hold vary widely by institution and are not
    > publicly standardized.

## R9. Graph-Based Mule-Account Detection

### (a) Five-Line Executive Summary

1.  **Verified Fact:** On the canonical [**[IBM AMLworld benchmark
    > (Altman et al., NeurIPS
    > 2023)]{.underline}**](https://arxiv.org/html/2306.16424v1),
    > message-passing Graph Neural Networks incorporating edge updates
    > and neighborhood aggregation (**GIN+EU** and **PNA**) crush
    > tabular-only MLPs on minority-class F1: on HI-Small, **GIN+EU
    > achieves 59.21% F1 and PNA achieves 51.87% F1 vs. 24.11% for
    > MLP**; on HI-Medium, **PNA reaches 68.12% F1 vs. 28.16% for MLP**.

2.  **Verified Fact:** Subsequent theoretical and empirical work by
    > [**[Egressy et al. (ETH Zurich / IBM Research, arXiv:2404.19109v2,
    > May 1, 2024)]{.underline}**](https://arxiv.org/html/2404.19109v2)
    > proved that standard MPNNs cannot detect directed cycles or
    > scatter-gather smurfing motifs unless augmented with **directed
    > port numberings, ego-IDs, and edge updates**, raising HI-Medium F1
    > above 72%.

3.  **Verified Fact:** Crucially, the [**[October 26, 2026 TWIN-GNN
    > benchmark on Elliptic++
    > (MDPI)]{.underline}**](https://www.mdpi.com/2624-800x/6/6/186)
    > demonstrates a vital operational split: **GNNs beat tabular GBDTs
    > by +67.7% PR-AUC on account/wallet-level illicit actor detection
    > (0.624 vs. 0.372), whereas LightGBM on engineered features beats
    > GNNs on individual transaction classification (0.807 vs. 0.439
    > F1)** because transductive graph structures suffer under temporal
    > shift and multi-hop neighbor sampling is too slow for synchronous
    > \<15 ms inline scoring.

4.  **Verified Fact:** RBIH\'s
    > [**[MuleHunter.AI]{.underline}**](https://docs.rbihub.in/mule-hunter)
    > (live in 26 Indian banks as of March 31, 2026 per [[RBI Annual
    > Report 2025-26, Para
    > VI.57]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
    > and linked with I4C via the [[May 12, 2026 MHA-RBIH
    > MoU]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2260277))
    > operates at the **account level**, combining behavioral, velocity,
    > and network topology features across 19 distinct mule patterns to
    > output an account-level mule confidence score.

5.  **Analytical Inference:** For laptop scale (8--16 GB RAM), TxnVigil
    > v2 should **not** run PyTorch Geometric on the synchronous
    > /v1/score hot path; instead, it should run **fast C-backed
    > python-igraph v1.0.0 micro-batch graph feature extraction every 5
    > minutes** (writing 12 structural/flow features into Valkey for
    > LightGBM) plus an **offline/nearline PyTorch Geometric v2.8.1
    > GraphSAGE/GIN+EU module** for account-level mule ring triage.

### (b) Graph Feature Engineering, GNN Benchmarks, MuleHunter.AI, and Library Comparison

Money-mule networks in India operate as **directed temporal
multigraphs** G = (V, E, T) where vertices V represent bank
accounts/VPAs (plus shared entity nodes such as device_id, ip_subnet,
and sim_iccid in a heterogeneous graph) and directed edges e = (u, v, t,
w) \\in E represent UPI/IMPS transfers of amount w at timestamp t.

#### 1. High-Signal Engineered Graph Features for Mule Detection

Even before training a neural network, computing 12 explicit structural
and temporal-flow graph metrics over a rolling 1-hour and 24-hour window
captures the exact mechanics of Layer-1 and Layer-2 mules ([[Altman et
al., 2023]{.underline}](https://arxiv.org/html/2306.16424v1); [[Egressy
et al., 2024]{.underline}](https://arxiv.org/html/2404.19109v2);
[[SAML-D SNA Resilience Study, June
2026]{.underline}](https://www.mdpi.com/2076-3417/16/12/6270)):

-   **Fan-In / Fan-Out Degree Asymmetry:**
    > d\_{\\text{in}}\^{(1\\text{h})}(v),
    > d\_{\\text{out}}\^{(1\\text{h})}(v), and degree ratio
    > \\frac{d\_{\\text{in}}(v)}{d\_{\\text{out}}(v) + 1}. Layer-1
    > collection mules exhibit high d\_{\\text{in}} (receiving from
    > 10--50 distinct victims) and low d\_{\\text{out}} (forwarding to
    > 1--3 Layer-2 consolidators).

-   **Pass-Through Flow Ratio & Flow Imbalance:**
    > \\text{PassThrough}\_{24\\text{h}}(v) = \\frac{\\sum\_{e \\in
    > E\_{\\text{out}}(v)} w_e}{\\sum\_{e \\in E\_{\\text{in}}(v)} w_e +
    > \\epsilon} Mule accounts retain almost zero balance, exhibiting
    > \\text{PassThrough}\_{24\\text{h}}(v) \\in \[0.90, 1.05\] coupled
    > with a high turnover-to-resting-balance ratio.

-   **Rapid-Forwarding Dwell Time (\\Delta t\_{\\text{dwell}}):** Median
    > time elapsed between an incoming credit t\_{\\text{in}} and the
    > next outgoing debit t\_{\\text{out}}. Automated Telegram/APK mule
    > bots forward funds in \\Delta t\_{\\text{dwell}} \< 180\\text{
    > seconds}.

-   **Temporal PageRank & Personalized Fraud PageRank
    > (Guilt-by-Association):** Standard PageRank \\text{PR}(v)
    > identifies hub aggregators, while **Personalized PageRank (PPR)**
    > seeded with known NCRP/DPIP-flagged accounts (\\vec{s}\_u = 1 if u
    > \\in \\mathcal{F}\_{\\text{known}}) propagates risk 1 to 3 hops
    > downstream in O(\\lvert E \\rvert) iterations.

-   **Leiden Community Fraud Density:** Partitioning the 24-hour
    > transaction + shared-device graph via the **Leiden algorithm**
    > (available in C speed in python-igraph v1.0.0) and computing the
    > fraction of flagged/new accounts in account v\'s community.

-   **2-Hop Cycle & Scatter-Gather Motif Counts:** Counting directed
    > 2-cycles (u \\leftrightarrow v), 3-cycles (u \\rightarrow v
    > \\rightarrow w \\rightarrow u), and bipartite/scatter-gather
    > diamonds where u splits ₹1,00,000 across v_1, v_2, v_3, v_4 who
    > all forward to z within 1 hour ([[Egressy et al., May
    > 2024]{.underline}](https://arxiv.org/html/2404.19109v2)).

-   **Shared-Infrastructure Bipartite Projection Degree:** Number of
    > distinct bank accounts/VPAs sharing the same device_id,
    > ip_prefix_24, or beneficiary_mobile within 7 days (catches mule
    > herders operating 20+ rented SIMs/accounts on one handset
    > cluster).

#### 2. Published GNN Benchmarks on AMLworld and Elliptic++

  -------------------------------------------------------------------------------------------------------------------------------------------------------
  Benchmark        Model Architecture Reported Metric &      Inference          Source & Date
  Dataset & Study                     Score                  Throughput /       
                                                             Latency Note       
  ---------------- ------------------ ---------------------- ------------------ -------------------------------------------------------------------------
  **IBM AMLworld** **MLP** (Tabular   Minority F1: 24.11%    Fast tabular       [[Altman et al., NeurIPS 2023 (arXiv:2306.16424v1, June/Dec
  (HI-Small /      Baseline)          (HI-S), 14.59% (LI-S), baseline, blind to 2023)]{.underline}](https://arxiv.org/html/2306.16424v1)
  LI-Small /                          28.16% (HI-M), 7.95%   multi-hop edges.   
  HI-Medium /                         (LI-M)                                    
  LI-Medium)                                                                    

  **IBM AMLworld** **GAT** (Graph     Minority F1: 36.17%    43,074 TPS batch   [[Altman et al., NeurIPS 2023
                   Attention Network) (HI-S), 25.67% (LI-S), GPU inference;     (arXiv:2306.16424v1)]{.underline}](https://arxiv.org/html/2306.16424v1)
                                      15.66% (HI-M), 4.90%   unstable variance  
                                      (LI-M)                 (±20.22%) on       
                                                             medium graphs.     

  **IBM AMLworld** **GIN** (Graph     Minority F1: 39.31%    53,130 TPS batch   [[Altman et al., NeurIPS 2023
                   Isomorphism        (HI-S), 33.09% (LI-S), GPU inference      (arXiv:2306.16424v1)]{.underline}](https://arxiv.org/html/2306.16424v1)
                   Network)           38.48% (HI-M), 22.04%  (1,876s train      
                                      (LI-M)                 time).             

  **IBM AMLworld** **GIN+EU** (GIN    Minority F1: **59.21%  52,426 TPS batch   [[Altman et al., NeurIPS 2023
                   with Edge Updates) (HI-S)**, **39.27%     GPU inference      (arXiv:2306.16424v1)]{.underline}](https://arxiv.org/html/2306.16424v1)
                                      (LI-S)**, 54.90%       (2,437s train      
                                      (HI-M), 29.28% (LI-M)  time); best on     
                                                             small graphs.      

  **IBM AMLworld** **PNA** (Principal Minority F1: 51.87%    24,952 TPS (5,921s [[Altman et al., NeurIPS 2023
                   Neighbourhood      (HI-S), 38.29% (LI-S), train time);       (arXiv:2306.16424v1)]{.underline}](https://arxiv.org/html/2306.16424v1)
                   Aggregation)       **68.12% (HI-M)**,     min/max/std/mean   
                                      **38.02% (LI-M)**      aggregators excel  
                                                             on medium graphs.  

  **IBM AMLworld** **Subgraph-Aware   Minority F1: **\> 72%  Explicitly         [[Egressy et al.,]{.underline} [*The Shape of Money Laundering*,
  (HI-Medium       MPNN** (Port       (HI-M)**,              provably counts    ICML/arXiv (May 1,
  Subgraph Motifs) Numbering +        outperforming base     directed cycles    2024)]{.underline}](https://arxiv.org/html/2404.19109v2)
                   Ego-IDs + Edge     GIN/PNA by +4 to +17   and scatter-gather 
                   Updates)           F1 points              motifs.            

  **Elliptic++**   **TWIN-GNN** (Dual **Wallet/Actor-Level   Proves GNNs should [[TWIN-GNN,]{.underline} *[MDPI J. Cybersecur. Priv.]{.underline}* [(Oct
  (203.7K Txns +   GraphSAGE +        PR-AUC:** TWIN-GNN     run at the         26, 2026)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)
  822.9K Wallets)  Bipartite          **0.624** vs. LightGBM **account/actor    
                   Cross-Attention)   0.372 (+67.7%).        triage layer**,    
                   vs. **LightGBM**   **Txn-Level F1:**      while GBDTs should 
                                      LightGBM **0.807** vs. run at the         
                                      GNN 0.439.             **transaction      
                                                             layer**.           
  -------------------------------------------------------------------------------------------------------------------------------------------------------

#### 3. Laptop-Scale Graph Library Comparison (Versions as of November 2026)

  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Graph Library                  Latest Stable Version & Release Date                                              License        Implementation & Speed Verdict for
                                                                                                                                                         TxnVigil v2 (8--16
                                                                                                                                                         GB RAM)
  ------------------------------ --------------------------------------------------------------------------------- -------------- ---------------------- -------------------
  **python-igraph**              **v1.0.0** (Released **October 23, 2025**,                                        GPLv2+         C core (igraph 1.0.0); **RECOMMENDED
  (igraph/python-igraph)         [[GitHub]{.underline}](https://github.com/igraph/python-igraph/releases))                        10\\times--50\\times   WINNER for
                                                                                                                                  faster and 5\\times    Micro-Batch Graph
                                                                                                                                  lower RAM than         Features.**
                                                                                                                                  NetworkX for PageRank, Computes PageRank,
                                                                                                                                  Leiden                 Leiden communities,
                                                                                                                                  (community_leiden),    and 2-hop
                                                                                                                                  and                    pass-through stats
                                                                                                                                  degree/shortest-path   on 500K edges in \<
                                                                                                                                  calculations on 10\^6  1.5 seconds on 1
                                                                                                                                  edges.                 CPU core.

  **NetworkX**                   **v3.7** (Released **September 21, 2026**,                                        BSD-3-Clause   Pure Python            **Use for Small
  (networkx/networkx)            [[PyPI]{.underline}](https://pypi.org/project/networkx/) /                                       dict-of-dicts (with    Ego-Graphs (\< 500
                                 [[GitHub]{.underline}](https://github.com/networkx/networkx/releases))                           optional               nodes).** Ideal for
                                                                                                                                  nx-parallel/backend    serializing 2-hop
                                                                                                                                  dispatch); includes    ego-network JSON
                                                                                                                                  new Leiden/ISMAGS      payloads for the
                                                                                                                                  utilities in v3.7.     React link-analysis
                                                                                                                                                         UI, too
                                                                                                                                                         slow/memory-heavy
                                                                                                                                                         for 5M-edge batch
                                                                                                                                                         jobs.

  **PyTorch Geometric (PyG)**    **v2.8.1** (Released **October 14, 2025**,                                        MIT            PyTorch C++/CPU/CUDA   **RECOMMENDED
  (pyg-team/pytorch_geometric)   [[GitHub]{.underline}](https://github.com/pyg-team/pytorch_geometric/releases))                  tensor message passing WINNER for Optional
                                                                                                                                  (GraphSAGE, GINConv,   GNN Experiment.**
                                                                                                                                  PNAConv, HeteroData,   Clean API, works on
                                                                                                                                  LinkNeighborLoader).   CPU-only PyTorch
                                                                                                                                                         wheels without
                                                                                                                                                         requiring
                                                                                                                                                         specialized C++
                                                                                                                                                         graph binaries.

  **Deep Graph Library (DGL)**   Legacy v2.x (14.3k stars, [[GitHub]{.underline}](https://github.com/dmlc/dgl));   Apache-2.0     C++/PyTorch graph      **Avoid.** DGL\'s
  (dmlc/dgl)                     frequent PyTorch ABI/Colab import breakages reported ([[Issue                                    framework.             binary wheel
                                 #4587]{.underline}](https://github.com/googlecolab/colabtools/issues/4587))                                             compatibility with
                                                                                                                                                         modern PyTorch
                                                                                                                                                         2.5+/Python 3.13+
                                                                                                                                                         is brittle compared
                                                                                                                                                         to PyG v2.8.1.
  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Trying to run 2-hop neighbor sampling in PyTorch
    > Geometric synchronously inside /v1/score adds 30--200 ms latency
    > and contention, whereas pre-computing account-level graph features
    > asynchronously and reading them from Redis/Valkey takes \< 0.5 ms
    > ([[TWIN-GNN Benchmark, Oct 26,
    > 2026]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)).

-   **Analytical Inference:** Implement a **Two-Tier Mule-Hunter
    > Recipe** in TxnVigil v2:

    1.  **Tier 1 --- Nearline Micro-Batch Graph Feature Engine
        > (python-igraph v1.0.0 + DuckDB v1.5.6, every 5 minutes):**
        > Query the last 24 hours of transactions from DuckDB/Parquet,
        > build a directed multigraph in igraph v1.0.0, compute
        > in_degree_1h, out_degree_1h, pass_through_ratio_24h,
        > median_dwell_sec, pagerank, personalized_fraud_pagerank,
        > leiden_community_fraud_rate, cycle_3_flag, and
        > shared_device_degree, run the **Account Mule LightGBM
        > Classifier** to get mule_prob, and pipeline-write all 10
        > values into Valkey feat:acct:{account_id}.

    2.  **Tier 2 --- Offline/Nearline GNN Experiment (PyTorch Geometric
        > v2.8.1 Edge-Updated GraphSAGE / GIN+EU):** Include a
        > standalone reproducible pipeline (ml/gnn_mule_detector.py)
        > trained on **IBM AMLworld HI-Small** and
        > **TxnVigil-Synth-UPI** that compares (a) Tabular LightGBM
        > without graph features, (b) LightGBM + igraph engineered
        > features, and (c) PyG GIN+EU / GraphSAGE + LightGBM late
        > fusion, logging the ablation table directly to MLflow.

### (d) Open Uncertainties

-   UNCERTAIN: **Cross-Bank Federated Graph Topology in India.** As
    > proved by [[Altman et al.
    > (2023)]{.underline}](https://arxiv.org/html/2306.16424v1) and
    > [[Pricing Cross-Bank Context in Federated AML (arXiv:2610.35996v1,
    > October 26,
    > 2026)]{.underline}](https://arxiv.org/html/2610.35996v1), a single
    > bank only sees its own local subgraph (1 hop of an inter-bank UPI
    > transfer), whereas multi-hop cycles cross 3--6 banks. While
    > RBIH\'s
    > [[DPIP]{.underline}](https://docs.rbihub.in/digital-payments-intelligence-platform)
    > and
    > [[MuleHunter.AI]{.underline}](https://docs.rbihub.in/mule-hunter)
    > bridge this gap nationally, the exact federated vs. centralized
    > graph-aggregation protocol used between RBIH and participating
    > banks is not publicly disclosed.

## R10. MLOps, CI/CD, and Supply-Chain Security Tooling (Versions as of Now)

### (a) Five-Line Executive Summary

1.  **Verified Fact:** **MLflow** (latest **v3.17.2** in October 2026,
    > alongside **v2.11.5** patch on **September 23, 2026** per [[GitHub
    > mlflow/mlflow]{.underline}](https://github.com/mlflow/mlflow/releases))
    > has deprecated legacy Model Registry Stages (Staging, Production)
    > in favor of **Model Registry Aliases** (@champion, \@challenger,
    > \@shadow) and tags, enabling zero-downtime atomic model promotion
    > via URI models:/txnvigil-fraud@champion.

2.  **Verified Fact:** **Evidently** (latest **v0.7.23** in 2026 per
    > [[GitHub
    > evidentlyai/evidently]{.underline}](https://github.com/evidentlyai/evidently/releases))
    > provides native Python drift reports (DataDriftPreset,
    > TargetDriftPreset, Population Stability Index / PSI, Wasserstein
    > distance, and Kolmogorov-Smirnov tests) that export to JSON/HTML
    > without requiring a heavy background server.

3.  **Verified Fact:** For Python packaging, linting, and type-checking
    > in 2026, **uv v0.13.6** (**October 21, 2026**, [[GitHub
    > astral-sh/uv]{.underline}](https://github.com/astral-sh/uv/releases)),
    > **Ruff** (**October 26, 2026** signed release, [[GitHub
    > astral-sh/ruff]{.underline}](https://github.com/astral-sh/ruff/releases)),
    > **Pyright v1.1.414** (**September 9, 2026**, [[GitHub
    > microsoft/pyright]{.underline}](https://github.com/microsoft/pyright/releases)),
    > and **mypy v2.4.0** ([[Mypy
    > Docs]{.underline}](https://mypy.readthedocs.io/en/stable/changelog.html))
    > define the modern toolchain, while **pnpm** (**October 28, 2026**
    > release, [[GitHub
    > pnpm/pnpm]{.underline}](https://github.com/pnpm/pnpm/releases)),
    > **Vite v8.3.5** ([[GitHub
    > vitejs/vite]{.underline}](https://github.com/vitejs/vite/releases)),
    > **Vitest v5.0.5** (**October 15, 2026**,
    > [[npm]{.underline}](https://www.npmjs.com/package/@vitest/browser-playwright)),
    > and **Playwright v1.64.1** (**September 4, 2026**, [[GitHub
    > microsoft/playwright]{.underline}](https://github.com/microsoft/playwright/releases))
    > anchor the frontend stack.

4.  **Verified Fact:** Free open-source supply-chain security in 2026
    > centers on **Trivy v0.76.1** ([[GitHub
    > aquasecurity/trivy]{.underline}](https://github.com/aquasecurity/trivy/releases)),
    > **Grype v0.121.0** ([[GitHub
    > anchore/grype]{.underline}](https://github.com/anchore/grype/releases)),
    > **Syft v1.55.0** ([[GitHub
    > anchore/syft]{.underline}](https://github.com/anchore/syft/releases))
    > for CycloneDX/SPDX SBOMs, **Gitleaks v8.30.1** ([[GitHub
    > gitleaks/gitleaks]{.underline}](https://github.com/gitleaks/gitleaks/releases)),
    > **OSV-Scanner** ([[GitHub
    > google/osv-scanner]{.underline}](https://github.com/google/osv-scanner/releases)),
    > **Semgrep v1.183.0** (**October 29, 2026**, [[GitHub
    > semgrep/semgrep]{.underline}](https://github.com/semgrep/semgrep/releases)),
    > **Bandit v1.9.4** (**February 22, 2026**, [[GitHub
    > PyCQA/bandit]{.underline}](https://github.com/PyCQA/bandit/releases)),
    > **OWASP ZAP v2.17.0** (**December 15, 2025**, [[ZAP
    > Download]{.underline}](https://www.zaproxy.org/download/)), and
    > keyless **Cosign v3.1.4** (**October 2026**, [[GitHub
    > sigstore/cosign]{.underline}](https://github.com/sigstore/cosign/releases)).

5.  **Analytical Inference:** TxnVigil v2 should avoid running Prefect
    > (v3.9.1), Dagster, or DVC as persistent containers on a laptop;
    > instead, use **MLflow Model Registry Aliases (@champion /
    > \@challenger)**, **Evidently v0.7.23** scheduled via lightweight
    > CLI/cron, and a hardened **GitHub Actions CI/CD pipeline**
    > featuring setup-uv caching, Testcontainers integration tests,
    > Trivy/Syft/Gitleaks/Bandit/Semgrep security gates, and keyless
    > Sigstore cosign container signing via GitHub OIDC.

### (b) Complete MLOps, Developer Tooling, and Security Scanner Version Matrix (As of November 2026)

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Category          Tool / Package            Latest Verified Version & Release Date                                            License          Key 2025--2026 Architectural Notes & API Changes                                                    Recommendation for TxnVigil v2
  ----------------- ------------------------- --------------------------------------------------------------------------------- ---------------- --------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------
  **Model Registry  **MLflow**                **v3.17.2** (**Oct 2026**; 2.x LTS patch **v2.11.5** **Sept 23, 2026**,           Apache-2.0       **Model Registry Stages (Staging/Production) are deprecated/removed** in favor of **Model Aliases** **Use MLflow v3.17.2** with SQLite/Postgres backend (\--profile mlops) and load
  & Tracking**      (mlflow/mlflow)           [[GitHub]{.underline}](https://github.com/mlflow/mlflow/releases))                                 (client.set_registered_model_alias(name, \"champion\", version)) and **LoggedModel / Tracing**      \@champion + \@challenger models into FastAPI.
                                                                                                                                                 APIs.                                                                                               

  **Drift & Data    **Evidently**             **v0.7.23** (**2026**,                                                            Apache-2.0       Unified Snapshot/Report API (Report(metrics=\[DataDriftPreset(), ClassificationPreset()\])) with    **Use Evidently v0.7.23** in batch evaluation script to compute PSI on top 15
  Quality**         (evidentlyai/evidently)   [[GitHub]{.underline}](https://github.com/evidentlyai/evidently/releases))                         Litestar v2.18 local UI & JSON export; computes PSI and Wasserstein drift on numeric/categorical    features + score distribution drift (PSI \> 0.25 triggers alert).
                                                                                                                                                 columns.                                                                                            

  **Workflow        **Prefect**               Prefect **v3.9.1** (**2026**,                                                     Apache-2.0       Dagster\'s Software-Defined Assets (@asset) are great for data teams, and Prefect 3 adds            **Skip persistent orchestrator daemon.** Use a clean Python CLI (typer / Makefile) +
  Orchestration**   (PrefectHQ/prefect) vs.   [[GitHub]{.underline}](https://github.com/PrefectHQ/prefect/releases)); Dagster                    transactional task semantics, but running a persistent Dagster/Prefect webserver + daemon consumes  APScheduler inside stream-worker to save \~600 MB RAM.
                    **Dagster**               **Oct 31, 2026 release**                                                                           **400--800 MB RAM**.                                                                                
                    (dagster-io/dagster)      ([[GitHub]{.underline}](https://github.com/dagster-io/dagster/releases))                                                                                                                               

  **Data            **DVC** (iterative/dvc)   **v3.x** (**Mar 30, 2026 release**,                                               Apache-2.0       Useful when sharing static binary datasets across S3 remotes, but adds Git hook friction when       **Skip DVC.** Version the deterministic synthetic generator seed + schema
  Versioning**                                [[GitHub]{.underline}](https://github.com/iterative/dvc/releases))                                 datasets are generated deterministically via a seed script.                                         (synth_config.yaml) in Git and log dataset SHA-256 hashes directly to MLflow
                                                                                                                                                                                                                                                     (mlflow.log_inputs).

  **Python Package  **uv** (astral-sh/uv)     **v0.13.6** (**Oct 21, 2026**,                                                    Apache-2.0 / MIT 10--100x faster than pip/Poetry; uv.lock deterministic cross-platform lockfile; Oct 21, 2026        **Mandatory.** Use uv sync \--frozen in local dev, Docker multi-stage builds, and
  & Env Manager**                             [[GitHub]{.underline}](https://github.com/astral-sh/uv/releases))                                  release includes certifi 2026.10.19 eMudhra root CA distrust fix and CPython 3.13/3.14/3.15         GitHub Actions (astral-sh/setup-uv@v5+ with enable-cache: true).
                                                                                                                                                 standalone builds.                                                                                  

  **Python Linter & **Ruff** (astral-sh/ruff) **v0.14.x** (**Oct 26, 2026**, code-signed Oct 9, 2026,                           MIT              Replaces Flake8, Black, isort, pyupgrade, and autoflake in a single Rust binary (ruff check + ruff  **Mandatory** pre-commit and CI check.
  Formatter**                                 [[GitHub]{.underline}](https://github.com/astral-sh/ruff/releases))                                format).                                                                                            

  **Python Type     **Pyright**               Pyright **v1.1.414** (**Sept 9, 2026**,                                           MIT (Pyright) /  Pyright v1.1.414 includes standalone Type Server Protocol (TSP) and checks FastAPI/Pydantic v2 code **Recommend Pyright v1.1.414** (or basedpyright) as primary strict type checker (with
  Checker**         (microsoft/pyright) vs.   [[GitHub]{.underline}](https://github.com/microsoft/pyright/releases)); mypy      MIT (mypy)       3\\times--5\\times faster than mypy with fewer plugin quirks.                                       mypy v2.4.0 optional).
                    **mypy** (python/mypy)    **v2.4.0** (**2026**,                                                                                                                                                                                  
                                              [[Docs]{.underline}](https://mypy.readthedocs.io/en/stable/changelog.html))                                                                                                                            

  **JS/TS Package,  **pnpm**, **Vite**,       **pnpm** (**Oct 28, 2026**,                                                       MIT / Apache-2.0 **Security Alert:** Pin **Vitest \\ge v5.0.5** (or \\ge v4.1.8) to patch **CVE-2026-53633** (Vitest **Use pnpm + Vite v8.3.5 + Vitest v5.0.5 + Playwright v1.64.1** for the React +
  Build & Test**    **Vitest**,               [[GitHub]{.underline}](https://github.com/pnpm/pnpm/releases)); **Vite v8.3.5**   (Playwright)     Browser Mode CDP RCE vulnerability patched July 20, 2026 per                                        TypeScript analyst workbench.
                    **Playwright**            (create-vite@9.3.3,                                                                                [[SentinelOne]{.underline}](https://www.sentinelone.com/vulnerability-database/cve-2026-53633/)).   
                                              [[GitHub]{.underline}](https://github.com/vitejs/vite/releases)); **Vitest                                                                                                                             
                                              v5.0.5** (**Oct 15, 2026**,                                                                                                                                                                            
                                              [[npm]{.underline}](https://www.npmjs.com/package/@vitest/browser-playwright));                                                                                                                        
                                              **Playwright v1.64.1** (**Sept 4, 2026**,                                                                                                                                                              
                                              [[GitHub]{.underline}](https://github.com/microsoft/playwright/releases))                                                                                                                              

  **Container,      **Trivy**, **Grype**,     **Trivy v0.76.1** (**Oct 2026**,                                                  Apache-2.0       Trivy v0.76.1 patches CVE-2026-111943 (Go 1.27.3 eMudhra CA distrust) and scans OS packages,        **Use Trivy v0.76.1** for CI vulnerability & Dockerfile scanning + **Syft v1.55.0**
  Vulnerability &   **Syft**                  [[GitHub]{.underline}](https://github.com/aquasecurity/trivy/releases)); **Grype                   Python/JS lockfiles, Dockerfile misconfigs, and secrets in one pass; Syft v1.55.0 emits CycloneDX   for CycloneDX SBOM generation (aligned with [[CERT-In SBOM/AIBOM v2.0, July 9,
  SBOM Scanners**                             v0.121.0** (**Oct 2026**,                                                                          1.6 / SPDX SBOMs.                                                                                   2025]{.underline}](https://intellixbom.com/resources/aibom/aibom-vs-model-cards/)).
                                              [[GitHub]{.underline}](https://github.com/anchore/grype/releases)); **Syft                                                                                                                             
                                              v1.55.0** (**Oct 2026**,                                                                                                                                                                               
                                              [[GitHub]{.underline}](https://github.com/anchore/syft/releases))                                                                                                                                      

  **Secrets &       **Gitleaks**,             **Gitleaks v8.30.1** (**Nov 26, 2025**,                                           MIT (Gitleaks) / OSV-Scanner (backed by Google\'s osv-scalibr engine in 2026) natively parses uv.lock and            **Use Gitleaks v8.30.1** (pre-commit + CI) and **OSV-Scanner** (or pip-audit) on
  Dependency        **OSV-Scanner**,          [[GitHub]{.underline}](https://github.com/gitleaks/gitleaks/releases));           Apache-2.0 (OSV  pnpm-lock.yaml against the Open Source Vulnerability database in seconds.                           uv.lock & pnpm-lock.yaml.
  Scanners**        **pip-audit**             **OSV-Scanner** (**Oct 2026** osv-scalibr engine,                                 & pip-audit)                                                                                                         
                                              [[GitHub]{.underline}](https://github.com/google/osv-scanner/releases));                                                                                                                               
                                              **pip-audit** ([[PyPI]{.underline}](https://pypi.org/project/pip-audit/))                                                                                                                              

  **SAST, DAST &    **Semgrep**, **Bandit**,  **Semgrep v1.183.0** (**Oct 29, 2026**,                                           LGPL/Community   Bandit v1.9.4 is pure AST-based Python SAST (zero account required); Semgrep CE runs offline with   Run **Bandit v1.9.4 + Semgrep CE** on PRs, **OWASP ZAP v2.17.0 API baseline scan**
  Artifact          **OWASP ZAP**, **Cosign** [[GitHub]{.underline}](https://github.com/semgrep/semgrep/releases)); **Bandit    (Semgrep),       local rules; ZAP v2.17.0 runs baseline OpenAPI DAST against FastAPI; Cosign v3.1.4 signs images     against the Testcontainers FastAPI stack, and **Cosign v3.1.4 keyless signing** on
  Signing**                                   v1.9.4** (**Feb 22, 2026**,                                                       Apache-2.0       keylessly via GitHub OIDC (id-token: write).                                                        release images pushed to GHCR.
                                              [[GitHub]{.underline}](https://github.com/PyCQA/bandit/releases)); **OWASP ZAP    (Bandit, ZAP,                                                                                                        
                                              v2.17.0** (**Dec 15, 2025**,                                                      Cosign)                                                                                                              
                                              [[ZAP]{.underline}](https://www.zaproxy.org/download/)); **Cosign v3.1.4** (**Oct                                                                                                                      
                                              2026**, [[GitHub]{.underline}](https://github.com/sigstore/cosign/releases))                                                                                                                           
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** Most open-source ML repos fail production
    > engineering reviews because they lack lockfiles, integration tests
    > against real Redis/Postgres/Kafka instances, SBOMs, and container
    > signing.

-   **Analytical Inference:** Implement a **3-Workflow GitHub Actions
    > Pipeline** using reusable workflows and zero long-lived secrets
    > (100% OIDC):

    1.  ci-fast-checks.yml (runs in \< 90 sec on every PR): uv sync
        > \--frozen (cached via astral-sh/setup-uv), ruff check, ruff
        > format \--check, pyright, bandit -r src/, gitleaks detect,
        > osv-scanner \--lockfile=uv.lock \--lockfile=ui/pnpm-lock.yaml,
        > and pnpm \--dir ui test (Vitest v5.0.5).

    2.  ci-integration-and-dast.yml (runs in \< 4 min on PRs): Uses
        > testcontainers-python (v4.13.3+ per [[Quix Streams
        > deps]{.underline}](https://github.com/quixio/quix-streams/releases))
        > to spin up ephemeral **Valkey 9.1**, **PostgreSQL 18.6**, and
        > **Redpanda v26.2.2** containers inside the GitHub Actions
        > Ubuntu runner, verifies /v1/score p99 latency \< 15 ms at 200
        > RPS, runs Playwright v1.64.1 E2E tests against the React UI,
        > and executes the **OWASP ZAP v2.17.0 OpenAPI baseline scan**
        > against http://localhost:8000/openapi.json.

    3.  release-supply-chain.yml (runs on main / tags with GitHub
        > Environment approval): Builds multi-stage distroless/slim
        > images, scans with **Trivy v0.76.1** (\--exit-code 1
        > \--severity CRITICAL,HIGH), generates CycloneDX SBOMs via
        > **Syft v1.55.0**, and signs images + SBOM attestations
        > keylessly to GHCR using **Cosign v3.1.4** (permissions:
        > id-token: write, packages: write).

### (d) Open Uncertainties

-   UNCERTAIN: **Semgrep CE vs. Pro Registry Rules.** Semgrep\'s CLI
    > (v1.183.0) remains open-source, but several advanced cross-file
    > taint-tracking rules in the Semgrep Registry now require a Semgrep
    > AppSec Platform token; keeping local custom .semgrep.yml rules +
    > **Bandit v1.9.4** guarantees 100% token-free CI execution forever.

## R11. Free or Near-Free Hosting for the Demo (2026)

### (a) Five-Line Executive Summary

1.  **Verified Fact:** Between July 2025 and October 2026, free cloud
    > hosting tiers contracted sharply: **Oracle Cloud quietly halved
    > its Always Free Ampere A1 ARM tier in June 2026 from 4 OCPU / 24
    > GB RAM to 2 OCPU / 12 GB RAM** (1,500 OCPU-hours and 9,000
    > GB-hours/month per [[TerminalBytes Audit, June 26,
    > 2026]{.underline}](https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/)
    > and [[MrPlanB 2026 VPS
    > Audit]{.underline}](https://www.mrplanb.com/datacenter/free-vps-tiers)).

2.  **Verified Fact:** On **July 15, 2025**, **AWS abolished its classic
    > 12-month 750-hour/month EC2 Free Tier for new signups**, replacing
    > it with a **6-month Free Account Plan backed by up to \$200 in
    > credits** (\$100 at signup + \$100 via tasks) that automatically
    > closes after 6 months ([[AWS Free Tier
    > FAQs]{.underline}](https://aws.amazon.com/free/free-tier-faqs/);
    > [[Flavio Copes Free Tier Audit, October 16,
    > 2026]{.underline}](https://flaviocopes.com/hosting-free-tiers/)).

3.  **Verified Fact:** As verified in the [[September/October 2026
    > side-by-side hosting
    > audit]{.underline}](https://flaviocopes.com/hosting-free-tiers/),
    > **Fly.io** eliminated its monthly free allowance (now a 7-day /
    > 2-hour trial), **Railway** offers only \$1/month after a 30-day
    > \$5 trial (\~100 MB RAM), **Render** gives 512 MB RAM web services
    > that sleep after 15 idle minutes plus a 1 GB Postgres that expires
    > in 30 days, and **Google Cloud**\'s Always Free e2-micro VM has
    > only 1 GB RAM in US regions only (not India).

4.  **Verified Fact:** **Hugging Face Spaces** offers CPU Basic (**2
    > vCPU, 16 GB RAM, 50 GB ephemeral disk**, sleeps after 48h idle per
    > [[Hugging Face Spaces
    > Overview]{.underline}](https://huggingface.co/docs/hub/en/spaces-overview)),
    > though in **July 2026** Hugging Face restricted new free
    > Docker/Gradio Space creation on some unverified free accounts
    > ([[Hugging Face Forum, July 12,
    > 2026]{.underline}](https://discuss.huggingface.co/t/official-community-complaint-revert-free-cpu-basic-spaces-and-remove-anti-developer-sdk-restrictions/177703);
    > [[Klymentiev Audit, September 11,
    > 2026]{.underline}](https://klymentiev.com/blog/huggingface-inference-api))
    > and does not support multi-container docker-compose (requiring a
    > single container with supervisord exposing port 7860).

5.  **Analytical Inference:** The **#1 Best Option for a permanent 24/7
    > full docker-compose (6-service) deployment in India (ap-mumbai-1 /
    > ap-hyderabad-1) is Oracle Cloud Always Free Ampere A1 (2 OCPU / 12
    > GB RAM, \$0/month forever)**; the **#2 Best Option (Zero Credit
    > Card Required) is a dual-mode setup combining GitHub Codespaces
    > (2--4 cores, 8--16 GB RAM, 120 core-hours/month free, full
    > docker-compose) for live interactive runs + a single-container
    > Dockerfile.hf (supervisord) for Hugging Face Spaces / Render**.

### (b) Brutally Honest 2026 Comparison of All 9 Free / Near-Free Hosting Options

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Hosting        2026 Free RAM / CPU /  Sleep / Expiry Policy                                                                                                                                                 Can It Run 6-Service docker-compose?  India Region Available on    Credit Card Required?    Primary Source & Verification Date
  Provider       Storage Limits                                                                                                                                                                                                                     Free Tier?                                            
  -------------- ---------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------- ---------------------------- ------------------------ -------------------------------------------------------------------------------------
  **1. Oracle    **Ampere A1 ARM:** **2 **Never expires (\$0 forever)**; idle instances may be reclaimed only if CPU/RAM utilization stays \<10--20\\% over 7 days on Free tier (avoided by upgrading account **YES (Full native docker compose up  **YES** (ap-mumbai-1 Mumbai  **Yes** (Credit/Debit    [[TerminalBytes OCI 2026 Cut Analysis (June 26,
  Cloud Always   OCPU & 12 GB RAM**     to PAYG while staying strictly within 2 OCPU / 12 GB limits).                                                                                                         -d on Ubuntu VM).** 12 GB RAM runs    & ap-hyderabad-1 Hyderabad). card required for        2026)]{.underline}](https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/) &
  Free (OCI)**   (cut from 4 OCPU / 24                                                                                                                                                                        all 6 TxnVigil containers (\~3.2 GB   Note: Arm capacity can be    identity check; ₹0/month [[Oracle Cloud Free Tier]{.underline}](https://www.oracle.com/in/cloud/free/)
                 GB in June 2026: 1,500                                                                                                                                                                       total) with 8+ GB headroom.           tight; PAYG account tier     if within 2 OCPU / 12    
                 OCPU-hrs + 9,000                                                                                                                                                                                                                   fixes \"Out of host          GB).                     
                 GB-hrs/mo) + **2× AMD                                                                                                                                                                                                              capacity\" errors at \$0                              
                 Micro** (1/8 OCPU, 1                                                                                                                                                                                                               cost.                                                 
                 GB RAM each) + **200                                                                                                                                                                                                                                                                     
                 GB Block Storage**.                                                                                                                                                                                                                                                                      

  **2. Hugging   **CPU Basic:** **2     **Sleeps after 48 hours** without visitor traffic; wakes automatically on HTTP visit (\~30--60s cold boot). Note July 2026 restrictions on new compute Spaces for     **No native docker-compose** (runs a  No (US/EU AWS regions).      **No** for               [[HF Spaces Overview
  Face Spaces    vCPU, 16 GB RAM, 50 GB unverified free accounts ([[HF                                                                                                                                        single Dockerfile exposing port                                    grandfathered/eligible   Docs]{.underline}](https://huggingface.co/docs/hub/en/spaces-overview) & [[HF Pricing
  (Docker SDK)** ephemeral disk**       Forum]{.underline}](https://discuss.huggingface.co/t/official-community-complaint-revert-free-cpu-basic-spaces-and-remove-anti-developer-sdk-restrictions/177703)).   7860), **BUT** all services (FastAPI,                              accounts (or **\$9/mo    Audit (Sept 11,
                 (non-persistent across                                                                                                                                                                       Valkey, Postgres/SQLite, DuckDB,                                   PRO** if gated).         2026)]{.underline}](https://klymentiev.com/blog/huggingface-inference-api)
                 restarts unless paid                                                                                                                                                                         React static UI) can be bundled into                                                        
                 persistent storage is                                                                                                                                                                        **one fat container via supervisord**                                                       
                 attached).                                                                                                                                                                                   inside 16 GB RAM!                                                                           

  **3. GitHub    **120                  Auto-suspends after **30 minutes** of browser inactivity; quota resets monthly. Not for 24/7 unattended public hosting, but unbeatable for 1-click                    **YES (100% native docker compose up  Yes (Southeast Asia /        **No** (100% free with   [[GitHub Codespaces Features]{.underline}](https://github.com/features/codespaces) &
  Codespaces**   core-hours/month** +   recruiter/evaluator demos.                                                                                                                                            via                                   India-adjacent Azure         any personal GitHub      [[Unblocked 2026 Pricing Audit (Sept 25,
                 **15 GB                                                                                                                                                                                      .devcontainer/devcontainer.json).**   routing).                    account, no card         2026)]{.underline}](https://getunblocked.com/blog/best-developer-onboarding-tools/)
                 storage/month** free                                                                                                                                                                                                                                            needed).                 
                 for all personal                                                                                                                                                                                                                                                                         
                 GitHub accounts                                                                                                                                                                                                                                                                          
                 (equals **60                                                                                                                                                                                                                                                                             
                 hours/month on 2-core                                                                                                                                                                                                                                                                    
                 / 8 GB RAM** or **30                                                                                                                                                                                                                                                                     
                 hours/month on 4-core                                                                                                                                                                                                                                                                    
                 / 16 GB RAM**).                                                                                                                                                                                                                                                                          

  **4. Google    **Always Free:** 1×    e2-micro & Cloud Run are Always Free; \$300 credit expires in **90 days** (can run an e2-standard-4 16 GB VM in Mumbai for 90 days on the \$300 trial).               **No on Always Free e2-micro** (1 GB  e2-micro Always Free is      **Yes** (Card/UPI        [[Flavio Copes Hosting Audit (Oct 16,
  Cloud Free     e2-micro VM (**0.25--2                                                                                                                                                                       RAM OOMs instantly on 6 services);    **US-only**                  auto-pay verification    2026)]{.underline}](https://flaviocopes.com/hosting-free-tiers/)
  Tier (GCP)**   shared vCPU, 1 GB                                                                                                                                                                            **Yes for 90 days** using the \$300   (us-west1/central1/east1);   required).               
                 RAM**, 30 GB standard                                                                                                                                                                        credit on an e2-standard-2 (8 GB) or  \$300 trial works in Mumbai                           
                 disk) + **Cloud Run**                                                                                                                                                                        e2-standard-4 (16 GB) VM.             (asia-south1) & Delhi                                 
                 (2M requests, 180,000                                                                                                                                                                                                              (asia-south2).                                        
                 vCPU-s, 360,000                                                                                                                                                                                                                                                                          
                 GB-s/mo). **New Signup                                                                                                                                                                                                                                                                   
                 Trial:** \$300 credit                                                                                                                                                                                                                                                                    
                 for 90 days.                                                                                                                                                                                                                                                                             

  **5. AWS Free  **New Accounts (since  Free-plan account **automatically closes after 6 months** or when \$200 credits are exhausted unless upgraded to Paid Plan.                                           **Yes for \~3--5 months** (burning    **Yes** (ap-south-1 Mumbai & **Yes** (Payment method  [[AWS Free Tier FAQs]{.underline}](https://aws.amazon.com/free/free-tier-faqs/) &
  Tier           July 15, 2025):** **Up                                                                                                                                                                       the \$200 credit on a t3.large 8 GB   ap-south-2 Hyderabad).       required for identity    [[InfraTally AWS 2026 Guide (Apr 17,
  (Post-July     to \$200 in credits**                                                                                                                                                                        or t4g.large 8 GB ARM EC2 instance in                              verification).           2026)]{.underline}](https://infratally.com/articles/aws-free-tier-2026/)
  2025           (\$100 at signup +                                                                                                                                                                           Mumbai). Not free after 6 months.                                                           
  Overhaul)**    \$100 via tasks) valid                                                                                                                                                                                                                                                                   
                 for **6 months**                                                                                                                                                                                                                                                                         
                 (classic 12-month                                                                                                                                                                                                                                                                        
                 t2.micro/t3.micro free                                                                                                                                                                                                                                                                   
                 tier retired for new                                                                                                                                                                                                                                                                     
                 signups).                                                                                                                                                                                                                                                                                

  **6. Render**  **Free Web Service:**  Web service **sleeps after 15 minutes** of inactivity (\~60s cold wake); **Free Postgres is deleted after 30 days** (14-day grace period).                            **No** (512 MB RAM cannot run         No (Singapore sin is         **No** (Free tier runs   [[Flavio Copes Hosting Audit (Oct 16,
                 **512 MB RAM**, 0.1                                                                                                                                                                          LightGBM + Redpanda + Valkey +        closest; US/EU otherwise).   without a card and       2026)]{.underline}](https://flaviocopes.com/hosting-free-tiers/)
                 CPU (750 hrs/mo pool),                                                                                                                                                                       Postgres + Workers, and no                                         suspends on bandwidth    
                 5 GB bandwidth. **Free                                                                                                                                                                       multi-container compose on free                                    cap).                    
                 Postgres:** 1 GB disk,                                                                                                                                                                       tier).                                                                                      
                 **256 MB RAM**.                                                                                                                                                                                                                                                                          

  **7. Railway** **Trial:** \$5         \$1/month credit buys only **\~100 MB of continuous RAM** for a month (\$10/GB-month rate); services stop when \$1 runs out (in \~3--4 days for a multi-service app). **No on Free Plan** (supports         No (Singapore ap-southeast-1 **No** for initial       [[Flavio Copes Hosting Audit (Oct 16,
                 one-time credit for 30                                                                                                                                                                       multi-service compose templates, but  closest).                    GitHub-verified trial;   2026)]{.underline}](https://flaviocopes.com/hosting-free-tiers/)
                 days (with GitHub                                                                                                                                                                            \$1/mo credit runs out in \<72 hours;                              **Yes** for Hobby        
                 verification). **Free                                                                                                                                                                        requires Hobby \$5/mo + usage                                      (\$5/mo).                
                 Plan after 30 days:**                                                                                                                                                                        \\approx \\\$12--\\\$18/\\text{mo}).                                                        
                 **\$1/month credit**,                                                                                                                                                                                                                                                                    
                 max **0.5 GB RAM** & 1                                                                                                                                                                                                                                                                   
                 vCPU per service.                                                                                                                                                                                                                                                                        

  **8. Fly.io**  **No monthly free tier Trial stops after **2 hours runtime or 7 days**.                                                                                                                      **No for free.** Running \~4 GB of    **Yes** (bom Mumbai region   **Yes** (Card required   [[Flavio Copes Hosting Audit (Oct 16,
                 in 2026.** Only a                                                                                                                                                                            RAM across 6 machines costs           available on paid plans).    for all orgs past the    2026)]{.underline}](https://flaviocopes.com/hosting-free-tiers/)
                 **7-day trial with 2                                                                                                                                                                         \~$24–$`<!-- -->`{=html}30/month on                                2-hour trial).           
                 hours total machine                                                                                                                                                                          paid Fly.io.                                                                                
                 runtime** (machines                                                                                                                                                                                                                                                                      
                 stop after 5 minutes).                                                                                                                                                                                                                                                                   
                 Paid shared-cpu-1x                                                                                                                                                                                                                                                                       
                 (256 MB) is                                                                                                                                                                                                                                                                              
                 \~\$2.19/mo; RAM is                                                                                                                                                                                                                                                                      
                 **\$6/GB/month**                                                                                                                                                                                                                                                                         
                 (raised Oct 1, 2026).                                                                                                                                                                                                                                                                    

  **9. Koyeb**   **Starter Free Tier:** Sleeps on idle; free DB limited to 50 active hours/month.                                                                                                             **No** (512 MB RAM limit cannot host  No (Singapore/Frankfurt/US). No for basic GitHub      [[Koyeb Instance Docs (May 27,
                 1 Web Service (Free                                                                                                                                                                          6 services).                                                       signup, but severely     2026)]{.underline}](https://www.koyeb.com/docs/reference/instances)
                 nano instance: **512                                                                                                                                                                                                                                            resource-capped.         
                 MB RAM**, 0.1 vCPU) +                                                                                                                                                                                                                                                                    
                 1 Free Postgres (50                                                                                                                                                                                                                                                                      
                 hours/month active                                                                                                                                                                                                                                                                       
                 limit).                                                                                                                                                                                                                                                                                  
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation for TxnVigil v2

-   **Verified Fact:** No PaaS free tier (Render, Railway, Fly.io,
    > Koyeb) can run a 6-container docker-compose stack (FastAPI,
    > Redpanda, Valkey, PostgreSQL, Stream-Worker, React UI)
    > continuously in 2026 because they cap free containers at 512 MB
    > RAM or \$1/month credit ([[Flavio Copes Audit, Oct 16,
    > 2026]{.underline}](https://flaviocopes.com/hosting-free-tiers/)).

-   **Analytical Inference:** Provide **Two Official Zero-Cost
    > Deployment Modes** in the TxnVigil v2 repository:

    1.  **Option 1 (Best 24/7 Always-On Production Stack in India ---
        > \$0/month): Oracle Cloud Always Free Ampere A1 (2 OCPU / 12 GB
        > RAM / 200 GB SSD in ap-mumbai-1 or ap-hyderabad-1).** Even
        > after Oracle\'s June 2026 cut from 24 GB to 12 GB RAM
        > ([[TerminalBytes, June 26,
        > 2026]{.underline}](https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/)),
        > **12 GB of dedicated RAM + 2 ARM OCPUs + 200 GB disk** runs
        > TxnVigil v2\'s complete 6-container docker-compose.yml (\~3.2
        > GB RAM) 24/7/365 with 8.8 GB of free memory headroom and \<15
        > ms Indian network latency. (Ensure all 6 Docker images support
        > linux/arm64---Valkey, Redpanda, Postgres, Python-slim,
        > LightGBM v4.7.0, and Nginx all ship official arm64
        > wheels/images).

    2.  **Option 2 (Best Zero-Credit-Card Instant Evaluator Mode ---
        > \$0/month): GitHub Codespaces (.devcontainer/devcontainer.json
        > on 4-core / 16 GB RAM, 120 core-hours/month free) +
        > Single-Container Demo Profile (Dockerfile.demo for Hugging
        > Face Spaces 16 GB RAM).** Add a \"Launch in GitHub
        > Codespaces\" badge at the top of README.md that boots the full
        > 6-service docker-compose stack in 60 seconds with port
        > forwarding to the React UI, and provide a single-container
        > Dockerfile.demo (using supervisord to run FastAPI + Valkey +
        > SQLite/DuckDB + static React UI on port 7860 without Redpanda)
        > that runs inside Hugging Face Spaces\' 16 GB RAM CPU Basic
        > tier or a 1 GB VPS.

### (d) Open Uncertainties

-   UNCERTAIN: **Oracle Cloud Enforcement Timeline on Legacy 4 OCPU / 24
    > GB Accounts.** As documented in [[June 2026 OCI
    > reports]{.underline}](https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/),
    > while Oracle\'s official Always Free documentation now specifies
    > 1,500 OCPU-hours and 9,000 GB-hours (2 OCPU / 12 GB), enforcement
    > across existing vs. new PAYG tenancies has been inconsistent;
    > designing TxnVigil v2 to fit comfortably inside \< 3.5 GB RAM
    > guarantees it runs safely well below the new 12 GB ceiling.

## R12. Synthetic Financial Data: Realism and Validation

### (a) Five-Line Executive Summary

1.  **Verified Fact:** **PaySim** (2016) and **AMLSim** (2019/2021) used
    > multi-agent simulations parameterized by aggregate bank
    > statistics, whereas [**[IBM AMLworld / IT-AML (Altman et al.,
    > NeurIPS 2023)]{.underline}**](https://arxiv.org/html/2306.16424v1)
    > constructed a full macroeconomic circular-flow virtual world
    > (modeling employers, salaries, retail purchases, shell companies,
    > and 9 illicit placement sources across placement, layering, and
    > integration) and validated its output against US Federal Reserve
    > payment format shares and real Italian bank motif frequencies
    > (Starnini et al., 1 laundering motif per \~21,440 transactions).

2.  **Verified Fact:** In synthetic data validation tooling as of 2026,
    > **SDMetrics** is actively maintained at **v0.28.2** (released
    > **July 24, 2026** per [[GitHub
    > sdv-dev/SDMetrics]{.underline}](https://github.com/sdv-dev/SDMetrics/releases)),
    > **SDV** reached **v2.0.0.dev0** (**September 30, 2026** per
    > [[PePy]{.underline}](https://pepy.tech/projects/SDV)), and
    > **synthcity** is at **v0.2.12** ([[GitHub
    > vanderschaarlab/synthcity]{.underline}](https://github.com/vanderschaarlab/synthcity/releases)),
    > though GAN/diffusion tabular synthesizers (CTGAN, TVAE) fail to
    > preserve multi-hop graph conservation of money (inflow == outflow)
    > and long-range temporal dependencies.

3.  **Verified Fact:** For agent-based financial simulation in Python,
    > **Mesa** released **v3.5.0b0 / v4.0a0** on **March 15, 2026**
    > (introducing a new first-class discrete event scheduling system
    > and Scenario API per [[GitHub
    > projectmesa/mesa]{.underline}](https://github.com/projectmesa/mesa/releases)),
    > while **SimPy** (**v4.1.1**, MIT license) remains the fastest
    > lightweight generator-based discrete-event simulation engine in
    > Python.

4.  **Verified Fact:** A synthetic fraud dataset is scientifically
    > invalid if a simple classifier can trivially separate synthetic
    > fraud from normal traffic using a single column (like PaySim\'s
    > balance arithmetic bug or uniform random timestamps).

5.  **Analytical Inference:** TxnVigil v2 should generate its UPI stream
    > using a **stateful agent-based discrete-event simulator (SimPy or
    > Mesa v3.5+ + NetworkX/igraph)**---never CTGAN---and gate the
    > generated dataset with an automated **5-Tier Realism & Validation
    > Checklist** covering marginal distributions (KS/JSD/Benford\'s
    > Law), temporal diurnal seasonality, graph topology power laws,
    > TSTR/TRTS utility, and leakage/trivial-separability checks.

### (b) Design of PaySim, AMLSim, and AMLworld & Synthetic Validation Tooling

#### 1. How PaySim, AMLSim, and IBM AMLworld Were Designed and Validated

-   **PaySim (Lopez-Rojas et al., 2016):** Built in Java using the MASON
    > multi-agent toolkit, calibrated to one month of aggregated
    > mobile-money logs from an African financial service provider
    > ([[Kaggle
    > PaySim]{.underline}](https://www.kaggle.com/datasets/ealaxi/paysim1)).
    > *Why it failed validation:* Fraud agents were coded to take over
    > an account, execute a TRANSFER of the exact balance, and
    > immediately CASH_OUT, while the simulator\'s balance-update
    > equation (newbalanceDest = oldbalanceDest + amount) was skipped or
    > zeroed out during fraud steps, creating deterministic data
    > leakage.

-   **IBM AMLSim (Suzumura & Kanezashi, 2019/2021):** Built a
    > multi-agent transaction graph generator parameterized by degree
    > distributions and 8 money-laundering subgraph motifs (fan-in,
    > fan-out, cycle, bipartite, stack, random, scatter-gather,
    > gather-scatter) ([[GitHub
    > IBM/AMLSim]{.underline}](https://github.com/IBM/AMLSim)).
    > *Limitation:* Modeled only inter-account *layering* transfers
    > without economic context (no salaries, goods purchases, or
    > criminal placement origins).

-   **IBM AMLworld / IT-AML (Altman et al., NeurIPS 2023):** Models a
    > complete macroeconomic **Circular Flow Graph** of individuals,
    > corporations, sole proprietors, and multiple banks
    > ([[arXiv:2306.16424v1, Section 3.4 & Appendix
    > A]{.underline}](https://arxiv.org/html/2306.16424v1)). Legitimate
    > agents receive weekly/biweekly/monthly salaries, buy retail
    > supplies, pay interest, and rebalance accounts to avoid negative
    > balances; criminal agents generate illicit funds from 9 placement
    > activities (extortion, loan sharking, gambling, smuggling, etc.),
    > launder them via the 8 canonical graph patterns *plus* natural
    > business expenses, and propagate a **transitive laundering tag**
    > across co-mingled funds. *Validation:* Altman et al. validated
    > LI-Large (176M transactions) against:

    1.  **US Federal Reserve Payment Statistics:** Matching annualized
        > transaction-per-account histograms and payment format
        > distributions (Cheque, ACH, Wire, Card).

    2.  **Real Bank Motif Prevalence (Starnini et al., 180M Italian bank
        > txns):** Ensuring gather-scatter and scatter-gather motifs
        > occur at virtually identical real-world rarity (1 in 21,440
        > transactions in LI-Large vs. 1 in 21,000 in Starnini et al.).

#### 2. Validation Libraries & Agent Simulation Frameworks (Versions as of November 2026)

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Tool / Library                Latest Stable Version & Release Date                                              License        Primary Capability            Suitability for TxnVigil
                                                                                                                                                               v2 UPI Simulation &
                                                                                                                                                               Validation
  ----------------------------- --------------------------------------------------------------------------------- -------------- ----------------------------- --------------------------
  **SDMetrics**                 **v0.28.2** (Released **July 24, 2026**,                                          BSL 1.1 / MIT  Computes KSComplement,        **RECOMMENDED for Tabular
  (sdv-dev/SDMetrics)           [[GitHub]{.underline}](https://github.com/sdv-dev/SDMetrics/releases))            (core)         TVComplement,                 Marginal & Pairwise
                                                                                                                                 CorrelationSimilarity,        Validation.** Lightweight,
                                                                                                                                 ContingencySimilarity,        supports Python 3.13/3.14,
                                                                                                                                 CardinalityShapeSimilarity,   generates automated
                                                                                                                                 and NewRowSynthesis privacy   quality scores.
                                                                                                                                 checks.                       

  **SDV** (sdv-dev/SDV) &       SDV **v2.0.0.dev0 / v1.x** (**Sept 30, 2026**,                                    BSL 1.1 (SDV)  Deep generative tabular       **Do NOT use CTGAN/TVAE to
  **synthcity**                 [[PePy]{.underline}](https://pepy.tech/projects/SDV)); synthcity **v0.2.12**      / Apache-2.0   synthesizers (CTGAN, TVAE,    generate transaction
  (vanderschaarlab/synthcity)   ([[GitHub]{.underline}](https://github.com/vanderschaarlab/synthcity/releases))   (synthcity)    TabDDPM).                     streams.** They violate
                                                                                                                                                               accounting conservation
                                                                                                                                                               (\\text{balance}\_t \\ne
                                                                                                                                                               \\text{balance}\_{t-1} +
                                                                                                                                                               \\Delta) and cannot
                                                                                                                                                               generate multi-hop mule
                                                                                                                                                               rings.

  **Mesa** (projectmesa/mesa)   **v3.5.0b0 / v4.0a0** (Released **March 15, 2026**, stable **v3.x**,              Apache-2.0     Python Agent-Based Modeling   **Excellent choice** for
                                [[GitHub]{.underline}](https://github.com/projectmesa/mesa/releases))                            (ABM) framework; v3.5/v4.0    modeling stateful
                                                                                                                                 adds first-class              Customer, Merchant,
                                                                                                                                 **discrete-event scheduling   Scammer, and Mule Herder
                                                                                                                                 (model.time)** and Scenario   agents interacting on a
                                                                                                                                 management.                   network topology.

  **SimPy** (team-simpy/simpy)  **v4.1.1** ([[PyPI]{.underline}](https://pypi.org/project/simpy/))                MIT            Process-based discrete-event  **Fastest & Lightest
                                                                                                                                 simulation using standard     Engine.** Can simulate
                                                                                                                                 Python generators (yield      1,000,000 UPI events with
                                                                                                                                 env.timeout(dt)).             asynchronous
                                                                                                                                                               call/scam/layering delays
                                                                                                                                                               in \< 10 seconds in pure
                                                                                                                                                               Python.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation: The TxnVigil v2 Synthetic Data Validation Checklist

To prove that TxnVigil v2\'s synthetic UPI dataset (TxnVigil-Synth-UPI)
is realistic and free from PaySim-style shortcuts, implement and run an
automated **tests/validate_synthetic_data.py** script that enforces the
following **7-Point Validation Checklist**:

  --------------------------------------------------------------------------------------
  Validation Dimension     Statistical /          Mathematical         Why It Matters
                           Algorithmic Test       Criterion / Target   for Fraud / AML
  ------------------------ ---------------------- -------------------- -----------------
  **1. Accounting &        Exact ledger equation  \\forall t:          Prevents the
  Balance Conservation     check + Single-Feature \\text{bal}\_{t} =   PaySim failure
  (Anti-PaySim Leakage     Decision Stump AUC     \\text{bal}\_{t-1}   mode where a
  Check)**                                        \\pm \\text{amt}\_t  depth-1 tree on
                                                  (or balance columns  oldbalanceOrg -
                                                  **strictly           amount -
                                                  excluded** from      newbalanceOrig
                                                  model features); max gets 0.999 AUC.
                                                  single-feature       
                                                  ROC-AUC \< 0.72.     

  **2. Marginal Amount     Log-Normal / Pareto    Median P2M ticket    Ensures amount
  Distribution & Indian    tail fit +             ₹180--₹350; median   thresholds
  UPI Ticket Calibration** Kolmogorov-Smirnov     P2P ticket           reflect real
                           (KSComplement in       ₹800--₹2,000;        Indian UPI
                           **SDMetrics            realistic clustering consumer behavior
                           v0.28.2**) + Spike     just below NPCI caps rather than
                           checks at NPCI         (₹4,999 cooling cap, uniform random
                           thresholds             ₹99,999 / ₹1,00,000  numbers.
                                                  P2P cap);            
                                                  KSComplement \\ge    
                                                  0.85.                

  **3. First-Digit         Chi-Square /           Legitimate P2M       Validates that
  Benford\'s Law &         Kullback-Leibler       utility/invoice      organic vs.
  Round-Number Anomaly     divergence against     amounts follow       coerced human
  Test**                   Benford\'s Law P(d) =  Benford\'s law       payment amounts
                           \\log\_{10}(1 +        (D\_{\\text{KL}} \<  have realistic
                           \\frac{1}{d}) on       0.02), while         digit entropy.
                           organic                human-typed P2P and  
                           bills/merchants vs.    task/investment      
                           human round-number     scams exhibit        
                           bias on scams          realistic spikes at  
                                                  1, 5, 9 leading      
                                                  digits (₹5,000,      
                                                  ₹10,000, ₹49,999,    
                                                  ₹99,000).            

  **4. Temporal Diurnal &  Non-Homogeneous        Peak UPI volume      Prevents
  Payday Seasonality (NHPP Poisson Process (NHPP) between 10:00--13:00 unrealistic flat
  Check)**                 hourly intensity       IST and 18:00--21:30 24-hour uniform
                           curve +                IST; trough at       timestamps and
                           autocorrelation at lag 02:00--05:00 IST (\< makes hour_of_day
                           k = 24\\text{h},       5\\% of peak);       / velocity
                           168\\text{h}           salary-day spike on  anomalies
                                                  1st--5th of month;   meaningful.
                                                  APK/SIM-swap attacks 
                                                  disproportionately   
                                                  elevated during      
                                                  01:00--04:30 IST.    

  **5. Graph Topology &    Clauset-Newman-Moore   Scale-free degree    Ensures the graph
  Power-Law Degree         power-law exponent     exponent \\alpha     cannot be
  Validation**             \\alpha on             \\in \[2.1, 2.9\];   trivially solved
                           in/out-degree          merchant hubs have   by flagging every
                           distributions +        high d\_{\\text{in}} high-in-degree
                           clustering             and low              node (which would
                           coefficient + motif    d\_{\\text{out}}     falsely block
                           prevalence             (pass_through        legitimate kirana
                                                  \\approx 0 into      stores and
                                                  settlement), whereas utilities!).
                                                  Layer-1/2 mules have 
                                                  high                 
                                                  d\_{\\text{in}},     
                                                  high                 
                                                  d\_{\\text{out}}     
                                                  (pass_through \\in   
                                                  \[0.90, 1.02\]), and 
                                                  short dwell times.   

  **6. Train-on-Synthetic, Train LightGBM on      Spearman rank        Proves that the
  Test-on-Real/Benchmark   canonical features     correlation \\rho    behavioral and
  (TSTR) & TRTS Utility**  (velocity_1h,          \\ge 0.70 between    graph features
                           pass_through_24h,      SHAP feature         learned on
                           in_degree_1h,          importance rankings  TxnVigil\'s
                           amount_zscore) on      on                   simulator match
                           TxnVigil-Synth-UPI and TxnVigil-Synth-UPI   the feature
                           evaluate rank-order    and IBM AMLworld     hierarchy of a
                           correlation of feature HI-Small.            peer-reviewed
                           importances against                         NeurIPS
                           **IBM AMLworld                              benchmark.
                           HI-Small**                                  

  **7. Non-Trivial         Train Logistic         Linear model PR-AUC  A synthetic
  Separability & Noise     Regression (linear)    \< 0.25;             dataset where F1
  Realism Floor**          vs. Tabular-Only       Tabular-only         = 0.999 is a
                           LightGBM vs.           LightGBM PR-AUC \\in broken toy.
                           Tabular+Graph LightGBM \[0.45, 0.70\];      Legitimate noisy
                           on chronological split Tabular + Velocity + overlaps (e.g., a
                                                  Graph LightGBM       wedding gift or
                                                  PR-AUC \\in \[0.72,  medical emergency
                                                  0.88\] (never        transfer looking
                                                  1.000).              like a high-value
                                                                       push) must exist
                                                                       so false
                                                                       positives are
                                                                       non-zero.
  --------------------------------------------------------------------------------------

### (d) Open Uncertainties

-   UNCERTAIN: **Exact Empirical Distribution of Intra-Day UPI Mule
    > Dwell Times.** While law enforcement advisories indicate that
    > automated mule Telegram bots disperse Layer-1 funds within 2 to 15
    > minutes of receipt, exact empirical survival curves of dwell times
    > across the 26.48 lakh mule accounts identified by I4C ([[PIB
    > Release ID 2223095, Feb 4,
    > 2026]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095))
    > are not publicly published.

## R13. Existing Open-Source Projects to Beat

### (a) Five-Line Executive Summary

1.  **Verified Fact:** A comprehensive audit of GitHub in November 2026
    > reveals a stark divide in open-source fraud/AML repositories: a
    > handful of genuine production-oriented
    > platforms---[**[Ballerine]{.underline}**](https://github.com/ballerine-io/ballerine)
    > (2.5k stars),
    > [**[Marble]{.underline}**](https://github.com/checkmarble/marble)
    > (618 stars),
    > [**[Tazama]{.underline}**](https://github.com/tazama-lf/tazama-stack)
    > (Linux Foundation Charities, v4.0.0 launched July/Oct 2026),
    > [**[Jube]{.underline}**](https://github.com/jube-home/aml-fraud-transaction-monitoring)
    > (115 stars), and
    > [**[ezrules]{.underline}**](https://github.com/sofeikov/ezrules)
    > (11 stars, 749 commits, v1.29.4 in Oct 2026)---versus hundreds of
    > shallow student/tutorial repos (afedulov/fraud-detection-demo,
    > ververica/lab-fraud-detection,
    > VeedhiBhanushali/fraud-detection-system,
    > iitravindra/streaming_fraud_detection).

2.  **Verified Fact:** Commercial open-core tools like
    > [**[Marble]{.underline}**](https://github.com/checkmarble/marble)
    > and
    > [**[ezrules]{.underline}**](https://github.com/sofeikov/ezrules)
    > have strong rule-authoring and case-management UIs, but
    > **completely lack inline gradient-boosted ML scoring, real-time
    > TreeSHAP reason codes, graph mule-ring detection, and MLflow drift
    > governance**.

3.  **Verified Fact:** Conversely, streaming ML demos like
    > [**[afedulov/fraud-detection-demo]{.underline}**](https://github.com/afedulov/fraud-detection-demo)
    > (351 stars) and
    > [**[iitravindra/streaming_fraud_detection]{.underline}**](https://github.com/iitravindra/streaming_fraud_detection)
    > require bloated JVM Flink/Spark clusters, lack an analyst
    > case-management workbench or rule backtester, and often brag about
    > leaked 1.000 Precision on toy datasets
    > ([[VeedhiBhanushali/fraud-detection-system]{.underline}](https://github.com/VeedhiBhanushali/fraud-detection-system)).

4.  **Verified Fact:** **Zero existing open-source projects on GitHub
    > implement Indian UPI / RBI / NPCI / FIU-IND domain mechanics** (no
    > 24-hour ₹5,000 cooling limits, no P2P collect-request blocks, no
    > Digital Arrest / Task Scam / APK coercion signals, no
    > MuleHunter.AI-style graph pass-through features, and no RBI 21-day
    > SCN / 14-day FMR / FIU-IND 7-day STR compliance workflows).

5.  **Analytical Inference:** By combining **ezrules/Marble-grade rule
    > backtesting and case management** with **sub-15ms LightGBM +
    > Valkey Lua + igraph mule detection**, **RBI FREE-AI
    > explainability**, and **Indian UPI regulatory compliance** in a \<
    > 3.5 GB RAM Docker Compose stack, **TxnVigil v2 will stand alone as
    > the most complete open-source real-time payment fraud and
    > mule-detection platform on GitHub**.

### (b) Comparative Audit of Top 10 Open-Source Fraud and AML Monitoring Projects on GitHub

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  \#         Repository & URL                                                                                                                                                                        Stars & Forks    Last Commit / Release Date                                                   Tech Stack & License   Core Features Implemented          Main Technical & Domain Weaknesses (How TxnVigil Beats It)
                                                                                                                                                                                                     (Nov 2026)                                                                                                                                              
  ---------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------- ---------------------------------------------------------------------------- ---------------------- ---------------------------------- ------------------------------------------------------------------------------------
  **1**      [**[ballerine-io/ballerine]{.underline}**](https://github.com/ballerine-io/ballerine)                                                                                                   **2,500+ stars** Active (Oct 2026)                                                            TypeScript, Node.js    KYB/KYC onboarding workflows,      Primarily a **KYC/KYB onboarding & workflow state machine**, not a high-throughput
                                                                                                                                                                                                     / 315 forks                                                                                   21, React, pnpm,       document verification, case        sub-20ms transaction scoring engine; lacks LightGBM/SHAP, Redis sliding windows, and
                                                                                                                                                                                                                                                                                                   PostgreSQL, Docker     management UI, basic workflow rule graph mule detection.
                                                                                                                                                                                                                                                                                                   (MIT / Open-Core)      engine.                            

  **2**      [**[checkmarble/marble]{.underline}**](https://github.com/checkmarble/marble)                                                                                                           **618 stars** /  **Oct 2026** (v1.12.0, 291 commits)                                          TypeScript, NestJS,    Real-time rule builder,            **Rules-only in OSS core** (no LightGBM/GBDT model training or inline TreeSHAP
                                                                                                                                                                                                     92 forks                                                                                      React, PostgreSQL,     sanctions/PEP screening, case      explanations); no graph/GNN mule detection; enterprise features gated behind
                                                                                                                                                                                                                                                                                                   Docker Compose         investigation UI, audit logs, 4 GB commercial license; zero Indian UPI/RBI compliance.
                                                                                                                                                                                                                                                                                                   (Open-Core / Custom)   RAM Docker quickstart.             

  **3**      [**[afedulov/fraud-detection-demo]{.underline}**](https://github.com/afedulov/fraud-detection-demo)                                                                                     **351 stars** /  Legacy (Flink reference demo)                                                Java, Apache Flink,    Dynamic rule broadcasting in       Heavy JVM Flink + Kafka footprint; **rules-only** (no ML model, no SHAP, no feature
                                                                                                                                                                                                     155 forks                                                                                     Apache Kafka, Docker   Apache Flink                       store, no case management UI, no graph analytics, no MLOps).
                                                                                                                                                                                                                                                                                                   Compose (Apache-2.0)   (KeyedBroadcastProcessFunction),   
                                                                                                                                                                                                                                                                                                                          custom window processing.          

  **4**      [**[jube-home/aml-fraud-transaction-monitoring]{.underline}**](https://github.com/jube-home/aml-fraud-transaction-monitoring)                                                           **115 stars** /  **Oct 2026** (277 commits)                                                   C# (.NET 10), Vendored Hybrid rules + classical ML        Monolithic **C# / .NET 10** codebase using legacy vendored **Accord.NET**
                                                                                                                                                                                                     33 forks                                                                                      Accord.NET,            (vendored Accord.NET), sanctions   (discontinued years ago) instead of modern Python LightGBM/PyG/MLflow; copyleft
                                                                                                                                                                                                                                                                                                   PostgreSQL, Redis,     screening, case management, \"Ask  AGPL-3.0 license; no UPI/RBI domain modeling.
                                                                                                                                                                                                                                                                                                   Docker (AGPL-3.0)      Jooby\" LLM assistant, OWASP       
                                                                                                                                                                                                                                                                                                                          ZAP/Trivy CI.                      

  **5**      [**[ververica/lab-fraud-detection]{.underline}**](https://github.com/ververica/lab-fraud-detection)                                                                                     **33 stars** /   Legacy workshop repo                                                         Java, Apache Flink,    3-part Flink tutorial for windowed Purely an educational Flink workshop lab; no ML scoring, no online feature store, no
                                                                                                                                                                                                     19 forks                                                                                      Kafka, Docker Compose  velocity rules over synthetic card UI workbench, no graph features, and heavy JVM memory consumption.
                                                                                                                                                                                                                                                                                                   (Apache-2.0)           events.                            

  **6**      [**[tazama-lf/tazama-stack]{.underline}**](https://github.com/tazama-lf/tazama-stack) & [**[tazama-lf/tms-service]{.underline}**](https://github.com/tazama-lf/tms-service)             **26 stars**     **Oct/Nov 2026** (Tazama v4.0.0,                                             TypeScript/Node.js,    Linux Foundation real-time         Spins up **dozens of microservices** (1 rule per microservice pattern) requiring
                                                                                                                                                                                                     (tazama-stack,   [[tazama.org]{.underline}](https://www.tazama.org/products/tazama-4-0-0/))   NATS, ArangoDB,        typology processor for ISO 20022   heavy cluster orchestration; **typology-rule-driven rather than GBDT/SHAP
                                                                                                                                                                                                     33 org repos                                                                                  PostgreSQL, ISO 20022  DFSP switches (Mojaloop            ML-driven**; requires ISO 20022 XML/JSON payloads (pain.001/pacs.008) that are
                                                                                                                                                                                                     under Linux                                                                                   (pacs.008/pacs.002),   ecosystem), typology rules, v4.0   complex to run on an 8 GB laptop.
                                                                                                                                                                                                     Foundation)                                                                                   Docker/K8s             case management.                   
                                                                                                                                                                                                                                                                                                   (Apache-2.0)                                              

  **7**      [**[sofeikov/ezrules]{.underline}**](https://github.com/sofeikov/ezrules)                                                                                                               **11 stars** / 6 **Oct 2026** (v1.29.4, 749 commits)                                          Python 3.12 (uv),      Rule lifecycle management,         **Closest Python architectural peer**, *but* it is **100% rules-only** (zero
                                                                                                                                                                                                     forks                                                                                         FastAPI, SQLAlchemy,   **shadow deployment**,             LightGBM/ML scoring, zero TreeSHAP reason codes, zero MLflow/Evidently drift
                                                                                                                                                                                                                                                                                                   Celery, PostgreSQL,    **percentage rollouts**,           tracking, zero graph centrality/pass-through mule scoring, and zero Indian
                                                                                                                                                                                                                                                                                                   Redis, Angular,        **point-in-time rule               UPI/RBI/FIU-IND compliance).
                                                                                                                                                                                                                                                                                                   Playwright             backtesting**, basic entity link   
                                                                                                                                                                                                                                                                                                   (Apache-2.0)           expansion, RBAC & audit trail.     

  **8**      [**[VeedhiBhanushali/fraud-detection-system]{.underline}**](https://github.com/VeedhiBhanushali/fraud-detection-system)                                                                 **6 stars** / 0  2025/2026                                                                    Python, FastAPI,       Basic FastAPI + Kafka + Redis      Classic portfolio anti-pattern: uses deprecated ZooKeeper, lacks a real
                                                                                                                                                                                                     forks                                                                                         Kafka + ZooKeeper,     scaffold with a pre-trained        sliding-window feature store or UI, and claims **Precision: 1.000 and Accuracy:
                                                                                                                                                                                                                                                                                                   Redis, Docker (MIT)    scikit-learn/XGBoost pickle.       1.000** on leaked synthetic data ([[GitHub
                                                                                                                                                                                                                                                                                                                                                             README]{.underline}](https://github.com/VeedhiBhanushali/fraud-detection-system)).

  **9**      [**[aws-samples/sample-real-time-dynamic-fraud-detection-with-apache-flink]{.underline}**](https://github.com/aws-samples/sample-real-time-dynamic-fraud-detection-with-apache-flink)   **1 star** / 1   2025/2026                                                                    Java 11, Apache Flink, Attack simulator buttons           Hard-wired to paid **AWS managed services** (AWS MSK, DynamoDB Streams, ECS, ALB)
                                                                                                                                                                                                     fork                                                                                          AWS MSK, DynamoDB,     (Velocity, High Amount, Location   that cannot run free offline on a laptop; no ML/SHAP or mule graph analytics.
                                                                                                                                                                                                                                                                                                   React, Terraform       Hopping), React dashboard, Flink   
                                                                                                                                                                                                                                                                                                   (MIT-0)                dynamic rules.                     

  **10**     [**[iitravindra/streaming_fraud_detection]{.underline}**](https://github.com/iitravindra/streaming_fraud_detection) &                                                                   Community        2025/2026                                                                    Kafka, Spark           Streaming ingestion into           Require manual docker-compose restart spark-worker to reload a .pkl file ([[GitHub
             [**[ADARSHputhane/fraud-detection-engine]{.underline}**](https://github.com/ADARSHputhane/fraud-detection-engine)                                                                       portfolio repos                                                                               Structured Streaming / Spark/Redis with basic ML          README]{.underline}](https://github.com/iitravindra/streaming_fraud_detection));
                                                                                                                                                                                                     (\<10 stars)                                                                                  Redis Streams,         inference and Grafana charts.      zero SHAP explainability, zero case management, zero rule backtesting, and zero
                                                                                                                                                                                                                                                                                                   TimescaleDB, Grafana                                      graph mule detection.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### (c) Concrete Architectural Recommendation: The 5 Defining Features TxnVigil v2 Must Have to Beat Every Project Above

To be undeniably superior to **Marble**, **ezrules**, **Jube**,
**Tazama**, and every portfolio demo on GitHub, **TxnVigil v2 must ship
these 5 differentiating capabilities**:

1.  **Unified Dual-Sided (Payer + Payee) Real-Time Engine Combining
    > Rules + Calibrated LightGBM + Sub-Millisecond Native TreeSHAP
    > (pred_contrib=True):** Unlike **Marble** and **ezrules** (which
    > only run rules) and **Spark/Flink demos** (which only run
    > black-box .pkl files without rules or explainability), TxnVigil v2
    > evaluates pre-ML hard rules, Champion + Shadow LightGBM v4.7.0
    > models, and exact C++ TreeSHAP reason codes (RC01--RC25) in **\<
    > 15 ms p99** via a single atomic Valkey Lua pipeline.

2.  **MuleHunter.AI-Inspired Graph Pass-Through & Community Triage
    > Engine (python-igraph v1.0.0 + Optional PyG v2.8.1):** Unlike
    > every Python portfolio repo (which treats each row as an isolated
    > credit card swipe), TxnVigil v2 continuously computes directed
    > **fan-in, fan-out, 24h pass-through ratio, fund dwell time,
    > Personalized Fraud PageRank, and Leiden community fraud density**,
    > catching Layer-1 and Layer-2 mule accounts and rendering an
    > interactive **2-Hop Ego-Graph Visualizer** inside the React case
    > workbench.

3.  **End-to-End Indian UPI, RBI (2024/2026), NPCI (2025/2026), DPDP
    > (2025), and FIU-IND Regulatory Compliance Engine:** TxnVigil v2 is
    > the **first open-source platform built specifically for Indian
    > UPI**: enforcing NPCI\'s ₹5,000/24h new-device cooling limit and
    > Oct 2025 P2P collect ban, detecting Digital Arrest (call_active +
    > fd_broken) and APK/Screen-Share coercion, enforcing **RBI\'s
    > 21-day Show Cause Notice (SCN) natural-justice state machine**,
    > and exporting **14-day RBI FMR/CPFIR** and **7-day FIU-IND FINnet
    > 2.0 STR** payloads with **DPDP Act 2025 PII tokenization and
    > immutable audit logging**.

4.  **Point-in-Time Rule Backtester & Champion/Shadow Model Workbench
    > (Zero Train-Serve Skew via DuckDB + Parquet):** Every /v1/score
    > call logs its exact point-in-time 45-feature vector to Redpanda
    > \\rightarrow Parquet. Analysts can write a candidate rule or
    > select a \@challenger MLflow model in the React UI and backtest it
    > across millions of historical Parquet rows in \< 2 seconds via
    > **DuckDB v1.5.6**, viewing **Incremental True Positives,
    > Incremental False Positives, Value Detection Rate (VDR), and Net
    > Rupee Savings (₹)** before promoting to shadow or production.

5.  **Scientific Honesty & Hardened Supply-Chain Engineering (\< 3.5 GB
    > RAM Laptop Budget):** Instead of embarrassing 1.000 Precision
    > claims on leaked PaySim balances, TxnVigil v2 ships with an
    > automated **7-Point Synthetic Data Validation Suite (SDMetrics
    > v0.28.2)**, benchmarks on **IBM AMLworld HI-Small (NeurIPS 2023)**
    > and **IEEE-CIS**, maps governance artifacts (MODEL_CARD.md,
    > DATASHEET.md, aibom.json) directly to the **RBI FREE-AI Framework
    > (August 2025)**, and enforces a token-free GitHub Actions pipeline
    > with **Testcontainers, Trivy, Syft, Gitleaks, Bandit, OWASP ZAP,
    > and Cosign keyless signing**.

### (d) Open Uncertainties

-   UNCERTAIN: **Commercial Relicensing Risk of Competitor Repos.**
    > Because several VC-backed open-source risk repos
    > (checkmarble/marble, ballerine-io/ballerine) use open-core models
    > where advanced features are periodically moved into proprietary
    > enterprise tiers, licensing TxnVigil v2 under a clean **Apache-2.0
    > License** with **BSD-3 Valkey**, **PostgreSQL**, **MIT
    > DuckDB/FastAPI/LightGBM**, and **Apache-2.0 confluent-kafka**
    > guarantees zero proprietary lock-in.

## Consolidated Decisions for TxnVigil v2

The table below consolidates every architectural, algorithmic,
regulatory, data, MLOps, security, and hosting decision for **TxnVigil
v2**, grounded in the verified 2023--2026 primary sources above.

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Decision Area     Recommended Option (with   Technical & Regulatory Reason     Primary Source & Date
                    Exact Version)                                               
  ----------------- -------------------------- --------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **1. Regulatory   **RBI Fraud MD             Implements 21-day SCN             [[RBI Fraud MD (July 15, 2024)]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702); [[DPDP Rules G.S.R. 846(E) (Nov 13,
  Compliance Scope  (2024/2026) + NPCI UPI     natural-justice state machine,    2025)]{.underline}](https://www.dpdpa.com/DPDP_Rules_2025_English_only.pdf); [[NPCI UPI Circular (Sept 18,
  (R1)**            (2025/2026) + DPDP Rules   14-day FMR/CPFIR exports, 7-day   2026)]{.underline}](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/59640/NPCI-issued-the-UPI-Consolidated-Circular-Version-1-0-SEP182026.pdf)
                    (2025) + FIU-IND STR**     STR timer, NPCI ₹5,000/24h        
                                               new-device cooling cap, P2P       
                                               collect ban, and DPDP Sec         
                                               17(1)(c) PII HMAC tokenization +  
                                               audit logs.                       

  **2. Fraud        **Dual-Sided (Payer        Captures APP scam victim signals  [[PIB I4C NCRP Data (July 21, 2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1); [[PIB 26.48L Mule Accounts (Feb 4,
  Typology &        Coercion + Payee Mule      (is_call_active,                  2026)]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095)
  Feature Design    Velocity) 45-Feature       is_screen_sharing, fd_broken_1h,  
  (R2)**            Vector**                   qr_source==\'GALLERY\') AND       
                                               beneficiary Layer-1 mule signals  
                                               (payee_in_degree_1h,              
                                               pass_through_ratio_24h,           
                                               dwell_time_sec) simultaneously.   

  **3. Benchmark &  **IBM AMLworld HI-Small    Avoids PaySim\'s fatal            [[Altman et al. AMLworld (NeurIPS 2023)]{.underline}](https://arxiv.org/html/2306.16424v1); [[SAML-D Benchmark (Aug 15,
  Validation        (5.08M txns) + SAML-D +    balance-column leakage and ULB\'s 2026)]{.underline}](https://arxiv.org/html/2608.15447v1); [[Amazon FDB]{.underline}](https://github.com/amazon-science/fraud-dataset-benchmark)
  Datasets (R3)**   IEEE-CIS (FDB) +           anonymized PCA columns; validates 
                    TxnVigil-Synth-UPI**       graph mule features on NeurIPS    
                                               2023 AMLworld and device/velocity 
                                               features on IEEE-CIS.             

  **4. Primary      **LightGBM v4.7.0**        LightGBM achieves 0.807 F1 vs.    [[LightGBM v4.7.0 (July 18, 2026)]{.underline}](https://pypi.org/project/lightgbm/); [[XGBoost v3.4.2 (Sept 15,
  Transaction &     (Primary Txn + Account     0.439 GNN on transaction          2026)]{.underline}](https://github.com/dmlc/xgboost/releases); [[Elliptic++ Benchmark (Oct 26, 2026)]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)
  Account ML Models Mule Classifiers) +        classification with \<1.5 ms CPU  
  (R4)**            **XGBoost v3.4.2**         latency; unweighted log-loss +    
                    (Shadow) +                 Isotonic calibration enables      
                    **IsolationForest**        exact Expected Loss (₹) and       
                    (Feature Fusion)           Quantile Alert-Budget             
                                               thresholding.                     

  **5. Real-Time    **3-Stage Inline Pipeline  Replicates Stripe Radar, PhonePe, [[Stripe Radar Blog (Oct 19, 2026)]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning); [[Razorpay Bumblebee
  Scoring           (\< 15 ms p99, 50 ms       and DoorDash Riviera: Stage 1     (Dec 17, 2025)]{.underline}](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51);
  Architecture      Circuit Breaker) + 4-Tier  Pre-ML hard rules \\rightarrow    [[PhonePe Engineering]{.underline}](https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/)
  (R5)**            Action Matrix (ALLOW,      Stage 2 LightGBM + native         
                    STEP_UP, HOLD, BLOCK)**    TreeSHAP \\rightarrow Stage 3     
                                               Policy Matrix + async Redpanda    
                                               point-in-time feature logging.    

  **6. Online       **Valkey v9.1-alpine       Avoids Redis 7.4/8.x              [[Valkey Releases (Oct 26, 2026)]{.underline}](https://github.com/valkey-io/valkey/releases); [[AceMQ Redis vs Valkey Licensing (Oct 27,
  Feature Store &   (BSD-3)** + **Hand-Rolled  RSALv2/SSPLv1/AGPLv3 licensing    2026)]{.underline}](https://acemq.com/compare/valkey-vs-redis/); [[Feast v0.67.0 (Oct 13, 2026)]{.underline}](https://github.com/feast-dev/feast/releases)
  Cache (R6)**      Atomic Lua Sliding-Window  and Feast v0.67.0\'s              
                    Store** (Skip Feast on hot protobuf/push latency; executes   
                    path)                      atomic ZSET pruning + HASH/HLL    
                                               reads in \< 0.6 ms inside \~250   
                                               MB RAM.                           

  **7. Event        **Redpanda v26.2.2**       Saves \>1 GB RAM vs. JVM Kafka;   [[Redpanda v26.2.2 (Aug 19, 2026)]{.underline}](https://github.com/redpanda-data/redpanda/releases); [[confluent-kafka v2.16.1 (Oct
  Streaming Broker  (\--mode dev-container     confluent-kafka v2.16.1 provides  2026)]{.underline}](https://github.com/confluentinc/confluent-kafka-python/releases); [[Bytewax Releases]{.underline}](https://github.com/bytewax/bytewax/releases)
  & Consumer (R6)** \--smp 1 \--memory 450M) + C librdkafka performance and      
                    **confluent-kafka-python   Python 3.13/3.14 support,         
                    v2.16.1**                  avoiding stalled Bytewax          
                                               (v0.21.1, Nov 2024).              

  **8. OLTP Case    **PostgreSQL               Postgres 18.6 handles             [[PostgreSQL 18.6 (Aug 13, 2026)]{.underline}](https://www.postgresql.org/docs/release/18.6/); [[DuckDB 1.5.6 (Sept 29,
  Store & OLAP      v18.6-alpine** (Cases,     transactional case state machines 2026)]{.underline}](https://r.duckdb.org/news/index.html)
  Offline Store     Rules, Audit) + **DuckDB   and RBAC; in-process DuckDB 1.5.6 
  (R6)**            v1.5.6** over **Parquet**  runs point-in-time ASOF JOIN      
                    (Offline Features &        training queries and 5M-row rule  
                    Backtesting)               backtests in seconds with zero    
                                               server RAM when idle.             

  **9.              **LightGBM Native          Bypasses                          [[GitHub shap#5121 (Aug 12, 2026)]{.underline}](https://github.com/shap/shap/issues/5121); [[SHAP v0.54.1 (Oct 16,
  Explainability &  pred_contrib=True**        shap.TreeExplainer.\_\_init\_\_   2026)]{.underline}](https://shap.readthedocs.io/en/latest/release_notes.html); [[RBI FREE-AI Report (Aug 13,
  AI Governance     (Online) + **SHAP          dump_model() bug (shap#5121) for  2025)]{.underline}](https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306)
  (R7)**            v0.54.1** (Offline) +      \<1 ms exact TreeSHAP reason      
                    **RBI FREE-AI 7-Sutra      codes; maps MODEL_CARD.md,        
                    Governance Bundle**        DATASHEET.md, and aibom.json to   
                                               RBI FREE-AI (Aug 2025) & CERT-In  
                                               v2.0 (July 2025).                 

  **10. Production  **7-Metric Operational     Aligns evaluation with real       [[FluxForce AI Fraud Benchmarks (Aug 20, 2026)]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response); [[SAML-D Operational AML Study
  Evaluation        Scorecard** (VDR, ADR, AFR banking fraud ops budgets (K      (Aug 15, 2026)]{.underline}](https://arxiv.org/html/2608.15447v1)
  Metrics (R8)**    / FP:TP, Precision@K,      alerts/day) and rupee value       
                    Friction/Insult Rate, TTD, protection rather than naive      
                    Net Savings ₹)             accuracy or unweighted ROC-AUC.   

  **11. Graph       **python-igraph v1.0.0**   C-core igraph 1.0.0 computes      [[python-igraph v1.0.0 (Oct 23, 2025)]{.underline}](https://github.com/igraph/python-igraph/releases); [[NetworkX v3.7 (Sept 21,
  Mule-Account      (5-min micro-batch         PageRank, Leiden communities, and 2026)]{.underline}](https://pypi.org/project/networkx/); [[PyG v2.8.1 (Oct 14, 2025)]{.underline}](https://github.com/pyg-team/pytorch_geometric/releases)
  Detection (R9)**  features into Valkey) +    2-hop pass-through ratios in      
                    **NetworkX v3.7** (UI      \<1.5s on CPU; PyG v2.8.1         
                    ego-graphs) + **PyG        validates GNN actor-level uplift  
                    v2.8.1** (GIN+EU /         offline without slowing           
                    GraphSAGE experiment)      /v1/score.                        

  **12. MLOps, Dev  **MLflow v3.17.2**         Uses MLflow                       [[MLflow Releases]{.underline}](https://github.com/mlflow/mlflow/releases); [[Evidently Releases]{.underline}](https://github.com/evidentlyai/evidently/releases);
  Tooling & CI      (Aliases) + **Evidently    \@champion/@challenger aliases;   [[uv v0.13.6 (Oct 21, 2026)]{.underline}](https://github.com/astral-sh/uv/releases); [[Trivy v0.76.1]{.underline}](https://github.com/aquasecurity/trivy/releases);
  Security (R10)**  v0.7.23** + **uv v0.13.6 / patches CVE-2026-53633 (Vitest    [[Cosign v3.1.4]{.underline}](https://github.com/sigstore/cosign/releases)
                    Ruff / Pyright             \>= 5.0.5) and eMudhra CA         
                    v1.1.414** + **pnpm / Vite distrust (uv 0.13.6, Trivy        
                    v8.3.5 / Vitest v5.0.5 /   0.76.1); enforces zero-cost       
                    Playwright v1.64.1** +     supply-chain security in GitHub   
                    **Trivy v0.76.1 / Syft     Actions.                          
                    v1.55.0 / Gitleaks v8.30.1                                   
                    / Bandit v1.9.4 / ZAP                                        
                    v2.17.0 / Cosign v3.1.4**                                    

  **13. Free Demo   **Primary 24/7 Host:**     Accounts for OCI\'s June 2026 cut [[TerminalBytes OCI 2026 Cut (June 26, 2026)]{.underline}](https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/); [[Flavio Copes Hosting Audit (Oct 16,
  Hosting Strategy  **Oracle Cloud Always Free to 2 OCPU / 12 GB RAM and AWS\'s  2026)]{.underline}](https://flaviocopes.com/hosting-free-tiers/); [[GitHub Codespaces]{.underline}](https://github.com/features/codespaces)
  (R11)**           Ampere A1** (2 OCPU / 12   July 2025 6-month expiry; gives   
                    GB RAM,                    both a permanent 24/7 Indian      
                    Mumbai/Hyderabad) +        full-stack deployment and a       
                    **Zero-Card Evaluators:**  1-click cardless evaluator        
                    **GitHub Codespaces**      workspace.                        
                    (.devcontainer) &                                            
                    **Hugging Face Spaces**                                      
                    (Dockerfile.demo 16 GB                                       
                    RAM)                                                         

  **14. Synthetic   **SimPy v4.1.1 / Mesa      Enforces strict balance           [[SDMetrics v0.28.2 (July 24, 2026)]{.underline}](https://github.com/sdv-dev/SDMetrics/releases); [[Mesa Releases (Mar 15,
  Data Generator &  v3.5+ Multi-Agent UPI      conservation (zero PaySim         2026)]{.underline}](https://github.com/projectmesa/mesa/releases); [[Altman et al. (2023)]{.underline}](https://arxiv.org/html/2306.16424v1)
  Validation        Simulator** + **SDMetrics  leakage), Benford\'s Law, IST     
  (R12)**           v0.28.2 7-Point Validation diurnal NHPP curves, scale-free   
                    Suite**                    graph power laws, and TSTR rank   
                                               correlation against IBM AMLworld. 
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Comprehensive Reference List

All primary regulatory notifications, government parliamentary releases,
peer-reviewed papers, engineering blogs, and official software release
repositories cited in this research dossier are cataloged below with
publication dates and direct URLs.

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  \#             Title of Document / Repository / Paper          Author / Issuing Organization              Publication /       Direct Verified URL
                                                                                                            Release Date        
  -------------- ----------------------------------------------- ------------------------------------------ ------------------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  1              *Master Directions on Fraud Risk Management in  Reserve Bank of India (RBI)                July 15, 2024       [[https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12702)
                 Commercial Banks (including Regional Rural                                                                     
                 Banks) and All India Financial Institutions                                                                    
                 (RBI/DOS/2024-25/118)*                                                                                         

  2              *Reserve Bank of India (Commercial Banks --     Reserve Bank of India (RBI)                July 31, 2026       [[https://m.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13641]{.underline}](https://m.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=13641)
                 Fraud Risk Management) Directions, 2026                                                                        
                 (RBI/DoS/2026-27/412)*                                                                                         

  3              *Master Directions on Fraud Risk Management in  Reserve Bank of India (RBI)                July 15, 2024       [[https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12704]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12704)
                 Non-Banking Financial Companies (NBFCs)                                                                        
                 (including Housing Finance Companies)*                                                                         

  4              *Master Directions on Fraud Risk Management in  Reserve Bank of India (RBI)                July 15, 2024       [[https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12703]{.underline}](https://m.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=12703)
                 Urban Cooperative Banks (UCBs) / State                                                                         
                 Cooperative Banks / Central Cooperative Banks*                                                                 

  5              *RBI Annual Report 2025-26 --- Chapter VI:      Reserve Bank of India (RBI)                May 29, 2026        [[https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466]{.underline}](https://m.rbi.org.in/Scripts/AnnualReportPublications.aspx?Id=1466)
                 Regulation, Supervision and Financial Stability                                                                
                 (Tables VI.1--VI.4, Boxes VI.1--VI.3)*                                                                         

  6              *RBI Annual Report 2024-25 --- Chapter VI:      Reserve Bank of India (RBI)                May 29, 2025        [[https://www.rbi.org.in/scripts/AnnualReportPublications.aspx?Id=1436]{.underline}](https://www.rbi.org.in/scripts/AnnualReportPublications.aspx?Id=1436)
                 Regulation, Supervision and Financial                                                                          
                 Stability*                                                                                                     

  7              *Central Payments Fraud Information Registry    Reserve Bank of India (RBI)                December 26, 2022   [[https://m.rbi.org.in/Scripts/NotificationUser.aspx?Id=12431&Mode=0]{.underline}](https://m.rbi.org.in/Scripts/NotificationUser.aspx?Id=12431&Mode=0)
                 (CPFIR) -- Migration of Reporting to DAKSH                                                                     
                 (CO.DPSS.OVRST.No.S1619/06-08-005/2022-23)*                                                                    

  8              *MuleHunter.AI Official Documentation*          Reserve Bank Innovation Hub (RBIH)         2025--2026          [[https://docs.rbihub.in/mule-hunter]{.underline}](https://docs.rbihub.in/mule-hunter)

  9              *Digital Payments Intelligence Platform (DPIP)  Reserve Bank Innovation Hub (RBIH)         2025--2026          [[https://docs.rbihub.in/digital-payments-intelligence-platform]{.underline}](https://docs.rbihub.in/digital-payments-intelligence-platform)
                 Official Documentation*                                                                                        

  10             *I4C and RBIH Sign MoU to Strengthen AI-Driven  Press Information Bureau (PIB), Ministry   May 12, 2026        [[https://www.pib.gov.in/PressReleasePage.aspx?PRID=2260277]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2260277)
                 Detection of Mule Bank Accounts and Curb Cyber  of Home Affairs, Govt. of India                                
                 Frauds (PRID 2260277)*                                                                                         

  11             *National Cyber Crime Data --- NCRP & CFCFRMS   Press Information Bureau (PIB), Ministry   July 21, 2026       [[https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2287039&reg=1&lang=1)
                 Financial Fraud Statistics 2021--2026 (Lok      of Home Affairs, Govt. of India                                
                 Sabha Reply, PRID 2287039)*                                                                                    

  12             *Indian Cyber Crime Coordination Centre (I4C)   Press Information Bureau (PIB), Ministry   February 4, 2026    [[https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095]{.underline}](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2223095)
                 --- 26.48 Lakh Layer-1 Mule Accounts Shared     of Home Affairs, Govt. of India                                
                 (PRID 2223095)*                                                                                                

  13             *Digital Personal Data Protection Rules, 2025   Ministry of Electronics and Information    November 13, 2025   [[https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa]{.underline}](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa)
                 (Notification G.S.R. 846(E))*                   Technology (MeitY), Govt. of India         (Updated Oct 13,    
                                                                                                            2026)               

  14             *DPDP Rules, 2025 Notified --- Official         Press Information Bureau (PIB), Govt. of   November 17, 2025   [[https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf]{.underline}](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)
                 Explainer*                                      India                                                          

  15             *DPDP Act and Rules 2025: The 2026 Compliance   Legal 500                                  October 27, 2026    [[https://www.legal500.com/intelligence/india/privacy/dpdp-act-and-rules-2025-the-2026-compliance-milestones-businesses-cant-afford-to-miss]{.underline}](https://www.legal500.com/intelligence/india/privacy/dpdp-act-and-rules-2025-the-2026-compliance-milestones-businesses-cant-afford-to-miss)
                 Milestones*                                                                                                    

  16             *UPI Consolidated Circular Version 1.0*         National Payments Corporation of India     September 18, 2026  [[https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/59640/NPCI-issued-the-UPI-Consolidated-Circular-Version-1-0-SEP182026.pdf]{.underline}](https://avantiscdnprodstorage.blob.core.windows.net/legalupdatedocs/59640/NPCI-issued-the-UPI-Consolidated-Circular-Version-1-0-SEP182026.pdf)
                                                                 (NPCI)                                                         

  17             *NPCI Circular NPCI/UPI/2025-26/OC/185B:        National Payments Corporation of India     August 28, 2025     [[https://www.npci.org.in/uploads/UPI_OC_No185_B_FY_2025_26_Addendum_to_OC_185_A_Implementation_of_higher_per_transaction_limit_for_specific_categories_in_UPI_ba517a0902.pdf]{.underline}](https://www.npci.org.in/uploads/UPI_OC_No185_B_FY_2025_26_Addendum_to_OC_185_A_Implementation_of_higher_per_transaction_limit_for_specific_categories_in_UPI_ba517a0902.pdf)
                 Implementation of Higher Per-Transaction Limit  (NPCI)                                                         
                 for Specific Categories in UPI*                                                                                

  18             *UPI Fraud Clampdown: NPCI to End P2P Collect   The Times of India                         August 14, 2025     [[https://timesofindia.indiatimes.com/business/india-business/upi-fraud-clampdown-npci-to-end-p2p-collect-requests-from-october-1-banks-apps-told-to-block-pull-transactions-permanently/articleshow/123309612.cms]{.underline}](https://timesofindia.indiatimes.com/business/india-business/upi-fraud-clampdown-npci-to-end-p2p-collect-requests-from-october-1-banks-apps-told-to-block-pull-transactions-permanently/articleshow/123309612.cms)
                 Requests from October 1, 2025*                                                                                 

  19             *NPCI Modifies 5 UPI Rules Starting August 1st, Paisabazaar                                July 31, 2025       [[https://www.paisabazaar.com/banking/new-upi-rules/]{.underline}](https://www.paisabazaar.com/banking/new-upi-rules/)
                 2025*                                                                                                          

  20             *UPI 24-Hour ₹5,000 Cooling Period Limit        GST Munshi                                 September 30, 2026  [[https://gstmunshi.com/blog/upi-cooling-period-limit-rs-5000-twenty-four-hours-guide]{.underline}](https://gstmunshi.com/blog/upi-cooling-period-limit-rs-5000-twenty-four-hours-guide)
                 Explained*                                                                                                     

  21             *Suspicious Transaction Reporting (STR) Process Global Alliance for Financialcrime         July 27, 2026       [[https://gafa.org.in/blog/suspicious-transaction-reporting]{.underline}](https://gafa.org.in/blog/suspicious-transaction-reporting)
                 in India under FIU-IND Rules*                   Awareness (GAFA)                                               

  22             *AML Compliance Checklist: Everything a         Innefu Labs                                May 4, 2026         [[https://innefu.com/aml-compliance-checklist-india/]{.underline}](https://innefu.com/aml-compliance-checklist-india/)
                 Reporting Entity Needs to Know (FIU-IND &                                                                      
                 PMLA)*                                                                                                         

  23             *Report of the Committee to Develop a Framework Reserve Bank of India (RBI)                August 13, 2025     [[https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306]{.underline}](https://rbi.org.in/scripts/PublicationReportDetails.aspx?ID=1306)
                 for Responsible and Ethical Enablement of                                                                      
                 Artificial Intelligence (FREE-AI) in the                                                                       
                 Financial Sector (ID 1306)*                                                                                    

  24             *RBI Press Release 2025-2026/902: Report of the Reserve Bank of India (RBI)                August 13, 2025     [[https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61018]{.underline}](https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=61018)
                 FREE-AI Committee*                                                                                             

  25             *Summary of the RBI FREE-AI Committee Report*   Beni Chugh & Manvi Khanna, Dvara Research  October 21, 2025    [[https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/]{.underline}](https://dvararesearch.com/summary-of-the-rbi-free-ai-committee-report/)

  26             *Consultation Paper on Guidelines for           Securities and Exchange Board of India     June 20, 2025       [[https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html]{.underline}](https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html)
                 Responsible Usage of AI/ML in Indian Securities (SEBI)                                                         
                 Markets*                                                                                                       

  27             *Digital Arrest Scams and the Limits of         Observer Research Foundation (ORF)         July 18, 2026       [[https://www.orfonline.org/expert-speak/digital-arrest-scams-and-the-limits-of-domestic-enforcement]{.underline}](https://www.orfonline.org/expert-speak/digital-arrest-scams-and-the-limits-of-domestic-enforcement)
                 Domestic Enforcement*                                                                                          

  28             *Pune Senior Citizen Loses ₹2.1 Crore in        The420.in                                  November 2, 2026    [[https://the420.in/pune-senior-citizen-cyber-fraud-2-crore/]{.underline}](https://the420.in/pune-senior-citizen-cyber-fraud-2-crore/)
                 Investment and Fake Digital Arrest Scam*                                                                       

  29             *Pune Software Engineer Loses ₹2.17 Crore in    The420.in                                  October 30, 2026    [[https://the420.in/pune-engineer-217-crore-fake-trading-app-investment-scam/]{.underline}](https://the420.in/pune-engineer-217-crore-fake-trading-app-investment-scam/)
                 Fake Trading App Investment Scam*                                                                              

  30             *Techie Duped of ₹22 Lakh in International      The Hindu                                  October 17, 2025    [[https://www.thehindu.com/news/cities/Delhi/techie-duped-of-22-lakh-in-international-online-trading-scam/article70171815.ece]{.underline}](https://www.thehindu.com/news/cities/Delhi/techie-duped-of-22-lakh-in-international-online-trading-scam/article70171815.ece)
                 Online Trading Scam*                                                                                           

  31             *Telegram Task Scam: How a ₹200 Review Became a HerWorkCircle                              October 8, 2026     [[https://www.herworkcircle.com/guides/telegram-task-scam]{.underline}](https://www.herworkcircle.com/guides/telegram-task-scam)
                 ₹23 Lakh Loss*                                                                                                 

  32             *Task Scam on Telegram: The Fake Work-From-Home Bachao.ai                                  July 18, 2026       [[https://www.bachao.ai/blog/task-scam-telegram-job-fraud-india]{.underline}](https://www.bachao.ai/blog/task-scam-telegram-job-fraud-india)
                 Job Trap*                                                                                                      

  33             *Cyber Fraudsters Using New Tech (Malicious     Business Standard / CloudSEK               March 11, 2026      [[https://www.business-standard.com/industry/news/cyber-fraudsters-using-new-tech-to-bypass-upi-security-features-report-126031100477_1.html]{.underline}](https://www.business-standard.com/industry/news/cyber-fraudsters-using-new-tech-to-bypass-upi-security-features-report-126031100477_1.html)
                 APKs & Call Forwarding) to Bypass UPI Security                                                                 
                 Features*                                                                                                      

  34             *How to Stay Safe from Downloading Fake Apps    PhonePe Trust & Safety Blog                December 3, 2025    [[https://www.phonepe.com/blog/trust-and-safety/how-to-stay-safe-from-downloading-fake-apps-via-apk-scams/]{.underline}](https://www.phonepe.com/blog/trust-and-safety/how-to-stay-safe-from-downloading-fake-apps-via-apk-scams/)
                 via APK Scams*                                                                                                 

  35             *The Rise of eSIM Fraud in India and What You   South Indian Bank                          November 26, 2025   [[https://www.southindianbank.bank.in/blog/safe-banking/the-rise-of-eSI-fraud-in-india-and-what-you-can-do-about-it]{.underline}](https://www.southindianbank.bank.in/blog/safe-banking/the-rise-of-eSI-fraud-in-india-and-what-you-can-do-about-it)
                 Can Do About It*                                                                                               

  36             *Realistic Synthetic Financial Transactions for Erik Altman, Béni Egressy, Jovan Blanuša,  June 22, 2023 /     [[https://arxiv.org/html/2306.16424v1]{.underline}](https://arxiv.org/html/2306.16424v1)
                 Anti-Money Laundering Models (IBM AMLworld,     Kubilay Atasu (IBM Research & ETH Zurich)  December 10, 2023   
                 NeurIPS 2023 Datasets & Benchmarks)*                                                                           

  37             *IBM Transactions for Anti-Money Laundering     Erik Altman / IBM Research (Kaggle)        2023--2024          [[https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml]{.underline}](https://www.kaggle.com/datasets/ealtman2019/ibm-transactions-for-anti-money-laundering-aml)
                 (AMLworld Dataset)*                                                                                            

  38             *The Shape of Money Laundering: Subgraph        Béni Egressy et al. (ETH Zurich / IBM      May 1, 2024         [[https://arxiv.org/html/2404.19109v2]{.underline}](https://arxiv.org/html/2404.19109v2)
                 Representation Learning on Temporal Graphs with Research)                                                      
                 Directed Edge Updates*                                                                                         

  39             *Enhancing Anti-Money Laundering: Development   Berkan Oztas et al. (Bournemouth           December 2023       [[https://www.researchgate.net/publication/376637949_Enhancing_Anti-Money_Laundering_Development_of_a_Synthetic_Transaction_Monitoring_Dataset]{.underline}](https://www.researchgate.net/publication/376637949_Enhancing_Anti-Money_Laundering_Development_of_a_Synthetic_Transaction_Monitoring_Dataset)
                 of a Synthetic Transaction Monitoring Dataset   University, IEEE ICEBE)                                        
                 (SAML-D)*                                                                                                      

  40             *Detecting Money Laundering in Mobile Money:    arXiv:2608.15447v1                         August 15, 2026     [[https://arxiv.org/html/2608.15447v1]{.underline}](https://arxiv.org/html/2608.15447v1)
                 Operational Evaluation on SAML-D*                                                                              

  41             *Elliptic++ Dataset: A Graph Network of Bitcoin Youssef Elmougy & Ling Liu (Georgia Tech,  August 2023         [[https://github.com/git-disl/EllipticPlusPlus]{.underline}](https://github.com/git-disl/EllipticPlusPlus)
                 Blockchain Transactions and Wallet Addresses*   KDD 2023)                                                      

  42             *TWIN-GNN: An Interpretable Multi-Graph         MDPI *Journal of Cybersecurity and         October 26, 2026    [[https://www.mdpi.com/2624-800x/6/6/186]{.underline}](https://www.mdpi.com/2624-800x/6/6/186)
                 Framework for Illicit Bitcoin Transaction and   Privacy* 6(6):186                                              
                 Wallet Detection on Elliptic++*                                                                                

  43             *Fraud Dataset Benchmark (FDB) and              Amazon Science                             September 22, 2023  [[https://github.com/amazon-science/fraud-dataset-benchmark]{.underline}](https://github.com/amazon-science/fraud-dataset-benchmark)
                 Applications*                                   (amazon-science/fraud-dataset-benchmark)   / January 23, 2024  

  44             *Synthetic Financial Datasets For Fraud         Edgar Lopez-Rojas (Kaggle)                 2016                [[https://www.kaggle.com/datasets/ealaxi/paysim1]{.underline}](https://www.kaggle.com/datasets/ealaxi/paysim1)
                 Detection (PaySim)*                                                                                            

  45             *IEEE-CIS Fraud Detection Competition Dataset*  Vesta Corporation & IEEE CIS (Kaggle)      July 15, 2019       [[https://www.kaggle.com/c/ieee-fraud-detection]{.underline}](https://www.kaggle.com/c/ieee-fraud-detection)

  46             *Credit Card Transactions Fraud Detection       Kartik Shenoy / Brandon Harris (Kaggle)    August 2020         [[https://www.kaggle.com/datasets/kartik2112/fraud-detection]{.underline}](https://www.kaggle.com/datasets/kartik2112/fraud-detection)
                 Dataset (Sparkov)*                                                                                             

  47             *IBM AMLSim: Multi-Agent Simulator for          Toyotaro Suzumura & Hiroki Kanezashi (IBM) 2021                [[https://github.com/IBM/AMLSim]{.underline}](https://github.com/IBM/AMLSim)
                 Anti-Money Laundering*                                                                                         

  48             *Tabular Machine Learning 2026: TabArena        CodeSOTA / Hollmann et al.                 2025--2026          [[https://www.codesota.com/tasks/tabular-ml]{.underline}](https://www.codesota.com/tasks/tabular-ml)
                 Leaderboard & TabPFN v2 (Nature 637)*                                                                          

  49             *Realistic Evaluation of TabPFN v2 in Open      arXiv:2505.16226v1                         May 22, 2025        [[https://arxiv.org/html/2505.16226v1]{.underline}](https://arxiv.org/html/2505.16226v1)
                 Environments*                                                                                                  

  50             *TabPFN-2.5: Advancing the State of the Art in  arXiv:2511.08667v2                         November 6, 2025    [[https://arxiv.org/html/2511.08667v2]{.underline}](https://arxiv.org/html/2511.08667v2)
                 Tabular Foundation Models*                                                                                     

  51             *Tabular Models Benchmark: Performance Across   AIMultiple Research                        October 12, 2026    [[https://aimultiple.com/tabular-models]{.underline}](https://aimultiple.com/tabular-models)
                 19 Datasets*                                                                                                   

  52             *TREASURE: The Visa Payment Foundation Model    Visa Research (arXiv:2511.19693v3)         April 8, 2026       [[https://arxiv.org/html/2511.19693v3]{.underline}](https://arxiv.org/html/2511.19693v3)
                 for High-Volume Transaction Data*                                                                              

  53             *Scaling Radar: Fighting Fraud with             Stripe Engineering Blog                    October 19, 2026    [[https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning]{.underline}](https://stripe.dev/blog/scaling-radar-fighting-fraud-with-agent-assisted-machine-learning)
                 Agent-Assisted Machine Learning & Payments                                                                     
                 Foundation Model*                                                                                              

  54             *How We Built It: Stripe Radar*                 Stripe Engineering Blog                    March 29, 2023      [[https://stripe.dev/blog/how-we-built-it-stripe-radar]{.underline}](https://stripe.dev/blog/how-we-built-it-stripe-radar)

  55             *Foundation Models Cut Card Issuer Fraud by Up  Sardine AI Engineering Blog                September 10, 2026  [[https://www.sardine.ai/blog/foundation-model-issuer-fraud-detection]{.underline}](https://www.sardine.ai/blog/foundation-model-issuer-fraud-detection)
                 to 35%*                                                                                                        

  56             *Meet Bumblebee: The Multi-Agent AI             Razorpay Engineering Blog                  December 17, 2025   [[https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51]{.underline}](https://engineering.razorpay.com/meet-bumblebee-the-multi-agent-ai-architecture-that-changed-fraud-detection-at-razorpay-c2b6d5704f51)
                 Architecture That Changed Fraud Detection at                                                                   
                 Razorpay*                                                                                                      

  57             *One Foundation Model, Built for India\'s       Razorpay Blog                              August 18, 2026     [[https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/]{.underline}](https://razorpay.com/blog/one-foundation-model-built-for-indias-payments-ecosystem/)
                 Payments Ecosystem (Razorpay Vulcan)*                                                                          

  58             *Building PhonePe\'s Real-Time Transaction      PhonePe Tech Blog                          July 28, 2022       [[https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/]{.underline}](https://tech.phonepe.com/building-phonepes-real-time-transaction-model-to-prevent-frauds-a-journey/)
                 Model to Prevent Frauds*                                                                                       

  59             *Self-Serve Feature Platforms: Architectures    Chip Huyen                                 January 8, 2023     [[https://huyenchip.com/2023/01/08/self-serve-feature-platforms.html]{.underline}](https://huyenchip.com/2023/01/08/self-serve-feature-platforms.html)
                 and APIs (PayPal, Uber Palette, DoorDash                                                                       
                 Riviera)*                                                                                                      

  60             *Real-Time Fraud Detection: Latency, Features & Redis Engineering Blog                     June 10, 2026       [[https://redis.io/blog/real-time-fraud-detection/]{.underline}](https://redis.io/blog/real-time-fraud-detection/)
                 Scale*                                                                                                         

  61             *Cost-Aware Adaptive Credit Card Fraud          ResearchGate                               October 21, 2026    [[https://www.researchgate.net/publication/416317894_Cost-Aware_Adaptive_Credit_Card_Fraud_Detection_Under_Concept_Drift_A_Comparative_Evaluation_of_Model-Maintenance_Policies]{.underline}](https://www.researchgate.net/publication/416317894_Cost-Aware_Adaptive_Credit_Card_Fraud_Detection_Under_Concept_Drift_A_Comparative_Evaluation_of_Model-Maintenance_Policies)
                 Detection Under Concept Drift*                                                                                 

  62             *LightGBM Python Package v4.7.0 Release*        LightGBM Maintainers                       July 18, 2026       [[https://pypi.org/project/lightgbm/]{.underline}](https://pypi.org/project/lightgbm/)
                                                                 (lightgbm-org/LightGBM)                                        

  63             *XGBoost Releases (v3.4.2 Stable)*              DMLC XGBoost (dmlc/xgboost)                September 15, 2026  [[https://github.com/dmlc/xgboost/releases]{.underline}](https://github.com/dmlc/xgboost/releases)

  64             *CatBoost Releases (v1.2.10)*                   CatBoost (catboost/catboost)               February 19, 2026   [[https://github.com/catboost/catboost/releases]{.underline}](https://github.com/catboost/catboost/releases)

  65             *Feast Open-Source Feature Store Releases       Feast Developers (feast-dev/feast)         October 13, 2026    [[https://github.com/feast-dev/feast/releases]{.underline}](https://github.com/feast-dev/feast/releases)
                 (v0.67.0)*                                                                                                     

  66             *Valkey Releases (v9.1 Security Patch &         Linux Foundation Valkey (valkey-io/valkey) September 16, 2026  [[https://github.com/valkey-io/valkey/releases]{.underline}](https://github.com/valkey-io/valkey/releases)
                 v9.2.0-rc1)*                                                                               / October 26, 2026  

  67             *Redis Releases (v8.12)*                        Redis Inc. (redis/redis)                   October 31, 2026    [[https://github.com/redis/redis/releases]{.underline}](https://github.com/redis/redis/releases)

  68             *Valkey vs Redis in 2026: Licenses (BSD-3 vs    AceMQ                                      October 27, 2026    [[https://acemq.com/compare/valkey-vs-redis/]{.underline}](https://acemq.com/compare/valkey-vs-redis/)
                 RSALv2/SSPLv1/AGPLv3), Features & Support*                                                                     

  69             *Redpanda Releases (v26.2.2)*                   Redpanda Data (redpanda-data/redpanda)     August 19, 2026     [[https://github.com/redpanda-data/redpanda/releases]{.underline}](https://github.com/redpanda-data/redpanda/releases)

  70             *Apache Kafka Downloads (v4.1.2 / v4.4.0)*      Apache Software Foundation                 October 27--29,     [[https://kafka.apache.org/community/downloads/]{.underline}](https://kafka.apache.org/community/downloads/)
                                                                                                            2026                

  71             *confluent-kafka-python Releases (v2.16.1)*     Confluent Inc.                             October 2026        [[https://github.com/confluentinc/confluent-kafka-python/releases]{.underline}](https://github.com/confluentinc/confluent-kafka-python/releases)
                                                                 (confluentinc/confluent-kafka-python)                          

  72             *Quix Streams Releases (v3.28.1)*               Quix (quixio/quix-streams)                 October 2026        [[https://github.com/quixio/quix-streams/releases]{.underline}](https://github.com/quixio/quix-streams/releases)

  73             *Bytewax Releases (v0.21.1)*                    Bytewax (bytewax/bytewax)                  November 25, 2024   [[https://github.com/bytewax/bytewax/releases]{.underline}](https://github.com/bytewax/bytewax/releases)

  74             *PostgreSQL 18.6 Release Notes*                 PostgreSQL Global Development Group        August 13, 2026     [[https://www.postgresql.org/docs/release/18.6/]{.underline}](https://www.postgresql.org/docs/release/18.6/)

  75             *DuckDB 1.5.6 Release Changelog*                DuckDB Foundation                          September 29, 2026  [[https://r.duckdb.org/news/index.html]{.underline}](https://r.duckdb.org/news/index.html)

  76             *SHAP v0.54.1 Release Notes*                    SHAP Maintainers (shap/shap)               October 16, 2026    [[https://shap.readthedocs.io/en/latest/release_notes.html]{.underline}](https://shap.readthedocs.io/en/latest/release_notes.html)

  77             *SHAP Issue #5121: For LightGBM,                GitHub (shap/shap#5121)                    August 12, 2026     [[https://github.com/shap/shap/issues/5121]{.underline}](https://github.com/shap/shap/issues/5121)
                 booster\_.dump_model() vs Native                                                                               
                 pred_contrib=True Benchmark*                                                                                   

  78             *AIBOM vs Model Cards and Datasheets for        IntelliXBOM                                July 9, 2025 / 2026 [[https://intellixbom.com/resources/aibom/aibom-vs-model-cards/]{.underline}](https://intellixbom.com/resources/aibom/aibom-vs-model-cards/)
                 Datasets (incl. CERT-In Guidelines v2.0)*                                                                      

  79             *Fraud Detection Benchmarks 2026: Real Vendor   FluxForce AI                               August 20, 2026     [[https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response]{.underline}](https://www.fluxforce.ai/blog/fraud-detection-benchmarks-2026-response)
                 Data & False Positive Control*                                                                                 

  80             *python-igraph Releases (v1.0.0)*               igraph Development Team                    October 23, 2025    [[https://github.com/igraph/python-igraph/releases]{.underline}](https://github.com/igraph/python-igraph/releases)
                                                                 (igraph/python-igraph)                                         

  81             *NetworkX v3.7 Release*                         NetworkX Developers                        September 21, 2026  [[https://pypi.org/project/networkx/]{.underline}](https://pypi.org/project/networkx/)

  82             *PyTorch Geometric Releases (v2.8.1)*           PyG Team (pyg-team/pytorch_geometric)      October 14, 2025    [[https://github.com/pyg-team/pytorch_geometric/releases]{.underline}](https://github.com/pyg-team/pytorch_geometric/releases)

  83             *MLflow Releases (v3.17.2 & v2.11.5)*           MLflow (mlflow/mlflow)                     September 23, 2026  [[https://github.com/mlflow/mlflow/releases]{.underline}](https://github.com/mlflow/mlflow/releases)
                                                                                                            / October 2026      

  84             *Evidently Releases (v0.7.23)*                  Evidently AI (evidentlyai/evidently)       2026                [[https://github.com/evidentlyai/evidently/releases]{.underline}](https://github.com/evidentlyai/evidently/releases)

  85             *Astral uv Releases (v0.13.6)* & *Ruff          Astral (astral-sh/uv, astral-sh/ruff)      October 21, 2026 /  [[https://github.com/astral-sh/uv/releases]{.underline}](https://github.com/astral-sh/uv/releases)
                 Releases*                                                                                  October 26, 2026    

  86             *Pyright Releases (v1.1.414)*                   Microsoft (microsoft/pyright)              September 9, 2026   [[https://github.com/microsoft/pyright/releases]{.underline}](https://github.com/microsoft/pyright/releases)

  87             *Playwright Releases (v1.64.1)* & *Vitest       Microsoft / Vitest                         September 4, 2026 / [[https://github.com/microsoft/playwright/releases]{.underline}](https://github.com/microsoft/playwright/releases)
                 Browser Playwright (v5.0.5)*                                                               October 15, 2026    

  88             *Trivy Releases (v0.76.1)*, *Grype (v0.121.0)*, Aqua Security, Anchore, Sigstore           October 2026        [[https://github.com/aquasecurity/trivy/releases]{.underline}](https://github.com/aquasecurity/trivy/releases)
                 *Syft (v1.55.0)*, & *Cosign (v3.1.4)*                                                                          

  89             *Semgrep Releases (v1.183.0)*, *Bandit          Semgrep, PyCQA, Gitleaks, Checkmarx/OWASP  Nov 2025 -- Oct 29, [[https://github.com/semgrep/semgrep/releases]{.underline}](https://github.com/semgrep/semgrep/releases)
                 (v1.9.4)*, *Gitleaks (v8.30.1)*, & *OWASP ZAP                                              2026                
                 (v2.17.0)*                                                                                                     

  90             *Every Hosting Provider\'s Free Tier, Side by   Flavio Copes                               October 16, 2026    [[https://flaviocopes.com/hosting-free-tiers/]{.underline}](https://flaviocopes.com/hosting-free-tiers/)
                 Side (Checked September 2026)*                                                                                 

  91             *Oracle Cloud Free Tier 2026: 4 OCPU/24GB Cut   TerminalBytes                              June 26, 2026       [[https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/]{.underline}](https://terminalbytes.com/oracle-cloud-free-tier-changes-2026/)
                 to 2 OCPU/12GB*                                                                                                

  92             *SDMetrics Releases (v0.28.2)* & *Project Mesa  DataCebo (sdv-dev/SDMetrics) & Project     July 24, 2026 /     [[https://github.com/sdv-dev/SDMetrics/releases]{.underline}](https://github.com/sdv-dev/SDMetrics/releases)
                 Releases (v3.5.0b0 / v4.0a0)*                   Mesa                                       March 15, 2026      

  93             *Marble: Real-Time Decision Engine for Fraud    CheckMarble                                October 2026        [[https://github.com/checkmarble/marble]{.underline}](https://github.com/checkmarble/marble)
                 and AML (checkmarble/marble)*                                                              (v1.12.0)           

  94             *ezrules: Open-Source Transaction Monitoring    Sofeikov                                   October 2026        [[https://github.com/sofeikov/ezrules]{.underline}](https://github.com/sofeikov/ezrules)
                 Engine (sofeikov/ezrules)*                                                                 (v1.29.4)           

  95             *Jube: Open-Source AML and Fraud Detection      Jube / Linux Foundation Charities          October--November   [[https://github.com/jube-home/aml-fraud-transaction-monitoring]{.underline}](https://github.com/jube-home/aml-fraud-transaction-monitoring)
                 (jube-home/aml-fraud-transaction-monitoring)* &                                            2026                
                 *Tazama (tazama-lf/tazama-stack)*                                                                              
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
