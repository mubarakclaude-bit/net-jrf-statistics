# Official Statistics — factual accuracy audit (Paper 2)

**Audit date:** 14 November 2026  
**Repository:** https://github.com/mubarakclaude-bit/net-jrf-statistics  
**Base:** `main` at `b78be4bf68a02029d4c906a9afa760eb54aec40f`  
**Branch:** `audit/official-statistics-factual-accuracy-2026-11-14`  
**Scope:** Official Statistics module only; five catalog topics and their mastery pools.

## Executive summary

The actual catalog is `seed/catalog.json` (not `seed/meta_lessons.json`). It identifies these five topics:

| Catalog topic ID | Topic | Lesson file | Mastery pool |
|---|---|---|---|
| `official-t1` | CSO, NSSO, NSO, MoSPI, NSC | `seed/lesson_10a1.json` | `seed/official_t1_mastery.json` |
| `official-t2` | Commissions and committees | `seed/lesson_10a2.json` | `seed/official_t2_mastery.json` |
| `official-t3` | Indian statisticians | `seed/lesson_10a3.json` | `seed/official_t3_mastery.json` |
| `official-t4` | Major surveys and indices | `seed/lesson_10a4.json` | `seed/official_t4_mastery.json` |
| `official-t5` | Census and vital statistics | `seed/lesson_10a5.json` | `seed/official_t5_mastery.json` |

**Audit accounting (claim groups, not raw sentence count):**
- **94 claim groups reviewed:** T1 13, T2 14, T3 19, T4 25, T5 23.
- **16 confirmed factual errors corrected** in lesson text or mastery explanations.
- **16 additional qualifications or unsupported claims corrected/removed** to avoid overstatement and to distinguish recommendation, legal authority, survey coverage, historical status and current status.
- **12 currency updates** applied to current institutions, survey releases, index series, census schedules and vital-statistics figures.
- **5 source-page follow-ups remain:** SRS 2024 annual rate tables, SRS 2024 sex-ratio tables, MMR 2022–24 table, the 2024 SRS sample-coverage count (removed from learner-facing content pending verification), and the OEA WPI/PPI transition detail. The official report/catalog records were located, but the relevant SRS/MMR PDFs or OEA page could not be retrieved for page-level inspection. No page number is claimed for them.

The branch changes **10 JSON files** (five lessons and five mastery pools) and this report. Each lesson retains 13 scenes; each mastery pool retains 20 items. No catalog, manifest, application code, configuration, workflow, shared infrastructure or other module was modified.

---

## Topic-wise audit reports

### T1 — CSO, NSSO, NSO, MoSPI, NSC

**Claim groups checked: 13**

| Claim area | Finding and action |
|---|---|
| MoSPI/NSO structure and 2019 merger | Current institutional descriptions checked against MoSPI's organisation material. Historical CSO/NSSO functions are distinguished from the post-merger NSO structure. |
| NSC origin and legal status | NSC was created by Government resolution in 2005 and constituted in 2006. It is not a statutory commission created by an Act. |
| NSC powers | The old shorthand that the NSC simply “cannot command” was too broad. The revised lesson explains that it is advisory and resolution-based, while its notified mandate includes requiring documents/information/attendance and conducting statistical audits. It does not itself compile the statistics. |
| GDP/CPI/IIP base changes | GDP moved to 2022–23, CPI to calendar 2024, and IIP to 2022–23. |
| IIP release date | **Corrected:** the first monthly IIP release on the 2022–23 base was 1 June 2026, not May. The 29 June 2026 release superseded the initial WPI-deflated series with the Output-PPI-deflated series; the first-release date and revised-series date are distinguished. |
| RBI inflation target | Current target period added: 1 April 2026 to 31 March 2031, 4 per cent with a 2–6 per cent tolerance band. |

**Primary sources (verified 14 November 2026):**
- MoSPI, *Know Your Ministry*: https://mospi.gov.in/sites/default/files/publication_reports/Know_Your_Ministry_MoSPI_27022025.pdf
- MoSPI, *National Statistical Commission — RTI Manual* (revised 12 January 2024): https://www.mospi.gov.in/sites/default/files/Manual/mannualNSCunderRTIAct_Revised12012024.pdf
- MoSPI/PIB, new GDP/CPI/IIP series release: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2226269&reg=3&lang=1
- MoSPI/PIB, new IIP series, base 2022–23: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2267531&reg=3&lang=1
- RBI, Monetary Policy Framework: https://www.rbi.org.in/Scripts/FS_Overview.aspx?fn=2752

### T2 — Commissions and committees

**Claim groups checked: 14**

| Claim area | Finding and action |
|---|---|
| Bowley–Robertson Committee | The official MoSPI chronology dates the committee to 1934. The lesson now uses 1934 rather than leaving the date as an unresolved 1933/1934 hedge. |
| National Income Committee | The 1949 constitution, chair and membership, and April 1951 / February 1954 report chronology were checked against official MoSPI material. Its contribution to national accounts and central coordination is not presented as the sole cause of the CSO. |
| Rangarajan Commission | The report submission date is August 2001. |
| “National Statistician” vs CSI | **Corrected:** “National Statistician” is the professional role recommended by the Rangarajan Commission; the official post/designation is Chief Statistician of India (CSI). |
| Statistical audits | The claim that statistical audits “were not instituted” was too categorical. The NSC's notified mandate includes statistical audit; whether a regular audit cycle operated is not established by the sources checked. |
| Collection of Statistics Act | The 2008 Act replaced the 1953 Act; the 2017 amendment was checked against the official statutory text. |
| SCES/SCoS chronology | The full SCES → SCoS → dissolution chain was not supported by an accessible primary order. It is no longer asserted as established fact. |
| NSS Steering Committee | MoSPI's Lok Sabha reply confirms an order dated 14 June 2024, a 17-member Steering Committee for National Sample Surveys, chaired by the NSC Chairperson, with a two-year original tenure. That original tenure reached its end in June 2026. No official extension or reconstitution order was located by 14 November 2026; current status is therefore marked unverified. The committee is not described as a direct successor to every SCoS function. |

**Primary sources (verified 14 November 2026):**
- MoSPI, *Sarvekshan Supplement: A Chronology of Events leading to the Birth of NSS* (2025): https://mospi.gov.in/sites/default/files/publication_reports/Sarvekshan_Supplement_Final_10_11_2025.pdf
- MoSPI, *National Statistical Commission Annual Report 2013–14*: https://mospi.gov.in/sites/default/files/annual_report/nsc_AR_2013-14.pdf
- MoSPI/PIB, Lok Sabha reply on Steering Committee for National Sample Surveys (24 July 2024): https://www.pib.gov.in/PressReleasePage.aspx?PRID=2036289
- India Code, *Collection of Statistics (Amendment) Act, 2017*: https://www.indiacode.nic.in/repealedfileopen?rfilename=A2017-21.pdf

Secondary references already present in the lesson (Carnegie, PRS and current-affairs reporting) are retained only as reading/context aids, not as primary evidence for statutory status or committee dissolution.

### T3 — Indian statisticians

**Claim groups checked: 19**

| Claim area | Finding and action |
|---|---|
| ISI founding and status | The 17 December 1931 founding meeting, formal registration in 1932 and 1959 Institute of National Importance status are distinguished. |
| Mahalanobis distance | 1930 refers to the initial distance concept; 1936 refers to the formal generalized-distance paper. These are not competing dates for the same event. |
| National Statistics Day | **Corrected:** 29 June was designated by Gazette notification dated 5 June 2007; the first observance was in 2007. The previous 2006 designation date was incorrect. |
| C. R. Rao | Official MoSPI biographical material was used for the career and contributions. Rao's 1945 estimation paper is kept distinct from the later score-test contribution. |
| P. V. Sukhatme | **Corrected:** MoSPI's official biography gives FAO Statistics Division service as 1952–1970 and retirement in 1971; it records the Padma Bhushan in 1973. The 1963 date refers to presentation of the nutrition paper associated with the Guy Medal, not a separately verified medal-award date. Other institutional biographies give differing service endpoints; the lesson follows the Government of India biography and flags the discrepancy in provenance. |
| R. C. Bose and S. N. Roy | Their statistical contributions were reviewed. Birth/death chronology for these two remains partly dependent on academic secondary biographies; no unsupported primary-biography claim is made. |
| Euler's conjecture | **Corrected:** Bose and Shrikhande gave the order-22 construction; Parker supplied the order-10 construction. The precise statement is that for (n=4k+2), (n>2), the conjecture fails except at (n=6); order 2 is also a trivial no-pair case. The previous attribution of the order-10 construction to all three and the omission of order 2 were corrected. |

**Primary/institutional sources (verified 14 November 2026):**
- MoSPI, *Statistics Day 2018 — life sketches of P. C. Mahalanobis, P. V. Sukhatme and C. R. Rao*: https://www.mospi.gov.in/sites/default/files/publication_reports/12_Statistics_Day_29jun18_rev.pdf
- Indian Statistical Institute, *Annual Report 2023–24*: https://asd.isical.ac.in/isical_web/files/about/publications/annual-reports/Annual_report_2023-24.pdf
- Bose and Shrikhande, original 1959 PNAS paper: https://www.pnas.org/doi/10.1073/pnas.45.5.734
- Bose–Mesner, original association-scheme article record/full text: https://digitalcommons.unl.edu/mathfacpub/7/

Academic secondary biographies (including MacTutor) are used only where an institutional primary biography was not located. Recommended books remain reading suggestions; no specific edition or page is claimed as checked.

### T4 — Major surveys and indices

**Claim groups checked: 25**

| Claim area | Finding and action |
|---|---|
| HCES periodicity | **Corrected:** HCES is conducted at regular intervals, not on a guaranteed decennial cycle. The 2022–23 and 2023–24 rounds were consecutive. |
| HCES 2017–18 | The official parliamentary answer attributes non-publication to data-quality concerns identified during vetting. The unsupported “after figures leaked” attribution was removed. |
| HCES and poverty | HCES supplies consumption data used in poverty analysis and budget shares used for CPI weights; it does not itself set the official poverty line or issue official poverty estimates. |
| HCES urban-rural gap | **Corrected:** 69.7% is the urban-minus-rural MPCE difference expressed as a percentage of rural MPCE. It is not rural MPCE as a percentage of urban MPCE. The 2011–12, 2022–23 and 2023–24 values are labelled consistently. |
| HCES food shares | The small increase from 2022–23 to 2023–24 is distinguished from the longer decline since 2011–12. |
| ASI | **Corrected:** ASI is an annual sample survey, not a census of every factory. Coverage now includes registered factories, specified bidi/cigar and electricity establishments, and eligible 100+ employee units listed in State Business Registers where shared. Latest published reference year is 2024–25; detailed release dated 4 November 2026. |
| ASUSE | Coverage is described as unincorporated non-agricultural establishments in manufacturing, trade and services (excluding construction), not merely the “unregistered counterpart” of ASI. ASUSE 2025 is the latest annual release; detailed report dated 6 May 2026. |
| PLFS and NFHS | PLFS 2025 redesign facts and the NFHS-5 institutional arrangement are retained. NFHS-6 outcomes are not quoted without a released official report. |
| AHS/SRS/CRS | **Corrected:** AHS is a separate historical sample survey; SRS is a sample registration system; CRS is the legal administrative registration system. They are not interchangeable. |
| CPI 2024 | Base 2024=100, COICOP 2018, 358 items, HCES 2023–24 weights, 1,465 villages and **1,407** urban markets. The previous 1,395 urban-market count was corrected. Six-group comparison weights are not confused with COICOP division weights. |
| IIP 2022–23 | 1,042 products / 463 item groups and the first-release/revised-release chronology are stated. Sectoral linking factors are included; the new water-supply sector has no direct old-series factor. |
| WPI/PPI | The 2022–23 WPI basket and June 2026 producer-price introduction are described. The lesson now states a five-year WPI transition rather than implying permanent parallel publication or immediate discontinuation. **The OEA source page could not be retrieved directly; the transition detail requires reviewer confirmation against the full OEA release before merge.** |
| RBI | CPI-Combined is the inflation-target index; the 2026–31 target period is added. |

**Primary sources (verified 14 November 2026 unless noted):**
- MoSPI, HCES 2023–24 Fact Sheet: https://mospi.gov.in/sites/default/files/publication_reports/HCES%20FactSheet%202023-24.pdf
- Parliament of India, Rajya Sabha Unstarred Question 2554 (8 August 2022): https://sansad.in/getFile/annex/257/AU2554.pdf?source=pqars
- MoSPI, ASI 2024–25 press note: https://www.mospi.gov.in/uploads/latestReleases/latest_release_1793786418398_98cc12b7-5c29-4865-9530-c0d4f2d3e645_PressNote_ASI_2024-25_publication_English.pdf
- MoSPI, ASUSE 2025 press note: https://www.mospi.gov.in/uploads/latestReleases/latest_release_1778063743760_e338f15d-195f-429f-892d-aa4155c7c4ce_Press_Note_ASUSE_2025_Report-English_%281%29.pdf
- MoSPI/PIB, CPI 2024=100 release: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2227012&reg=3&lang=1
- MoSPI/PIB, IIP 2022–23 release: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2267531&reg=3&lang=1
- MoSPI/PIB, revised IIP release using Output PPI: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2278961&lang=1&reg=3
- OEA/DPIIT, WPI/PPI 2022–23 portal: https://eaindustry.nic.in/download_data_2223.asp (**portal retrieval timed out; full release not page-verified**)
- RBI, Monetary Policy Framework: https://www.rbi.org.in/Scripts/FS_Overview.aspx?fn=2752

### T5 — Census and vital statistics

**Claim groups checked: 23**

| Claim area | Finding and action |
|---|---|
| Census history | The first non-synchronous population census exercise is distinguished as 1865–1872 (1872 commonly cited); 1881 was the first synchronous census. |
| Census 2027 | General Phase-II and the separately notified Goa, Uttar Pradesh, Punjab and non-snow-bound Uttarakhand schedule are distinguished. Reference moments are separated from enumeration windows: 1 March 2027 generally, 5 January 2027 for the four specially scheduled areas, and 1 October 2026 for snow-bound areas/Ladakh. Digital census, 16 self-enumeration languages, caste enumeration and workforce figures are sourced to official releases. |
| CRS | The 21-day reporting period and ORGI's 2024 registration levels (99.1% births, 99.4% deaths) are stated as registration-completeness levels, not SRS rates. An unsupported claim that the completeness denominator was necessarily SRS-based was removed. |
| RBD Amendment Act 2026 | **Clarified:** more than one year but not more than two years requires an order of the DM, SDM or authorised Executive Magistrate; more than two years requires a Judicial Magistrate First Class. The ordinary 21-day reporting period is unchanged. |
| SRS method | **Corrected:** continuous enumeration by a resident part-time enumerator plus an independent half-yearly retrospective survey by a full-time supervisor; records are matched and discrepancies verified. The incorrect monthly-urban/quarterly-rural description was removed. |
| SRS frame and precision | The 2014 frame revision and ten-year cycle are stated. The 2020 report's ≤15% relative-standard-error criterion is limited to IMR at natural-division level in major States, not generalised to every rate. |
| SRS/CRS distinction | SRS provides sample-based demographic rates; CRS provides legal counts of individually registered events. High registration levels do not make the two systems interchangeable. |
| Vital rates | IMR updated from 25 to 24; MMR updated from 93 to 87 with the relevant reference periods. The exact NRR definition is distinguished from the shortcut approximation (NRR \approx GRR \times) survival to mean age of childbearing. |
| Sex ratio at birth | The prior claim that the observed gap “is not sampling error” was removed. The lesson now notes that three-year averaging reduces year-to-year fluctuation but does not eliminate sampling or registration uncertainty. |

**Primary sources (verified 14 November 2026):**
- ORGI, Vital Statistics Division: https://censusindia.gov.in/census.website/en/node/180
- PIB, Census 2027 official backgrounder: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2255461
- ORGI, Census 2027 general Phase-II Gazette catalogue record: https://censusindia.gov.in/nada/index.php/catalog/47179
- ORGI, Census 2027 special schedule catalogue record: https://censusindia.gov.in/nada/index.php/catalog/47170
- Government of India, Registration of Births and Deaths (Amendment) Act, 2026: https://cdnbbsr.s3waas.gov.in/s3ec02e8258e5140317ff36c7f8225a3bf/uploads/2026/10/2026103088.pdf
- ORGI, SRS Statistical Report 2024 catalogue record: https://censusindia.gov.in/nada/index.php/catalog/47152 (**catalogue metadata checked; PDF/table pages not retrieved**)
- ORGI, MMR 2022–24 special bulletin catalogue record: https://censusindia.gov.in/nada/index.php/catalog/47151 (**catalogue metadata checked; PDF/table pages not retrieved**)
- ORGI, SRS Bulletin 2024 catalogue record: https://censusindia.gov.in/nada/index.php/catalog/47150 (**catalogue metadata checked; PDF/table pages not retrieved**)
- ORGI, SRS Statistical Report 2020: https://censusindia.gov.in/nada/index.php/catalog/44376/download/48048/SRS_STAT_2020.pdf

**Important limitation:** the official SRS 2024 annual report and MMR 2022–24 bulletin records are linked, but the PDFs could not be retrieved for table-level inspection. No specific table/page is claimed as checked. The exact 2024 sample-coverage count (8,839 units / 8.981 million population) was removed from learner-facing material pending verification. The current IMR/TFR/SRB and MMR values remain linked to the official report records, but the draft PR must not be merged until the corresponding tables are checked.

---

## Source-quality report

1. **Primary government sources used for current institutional, legal and statistical facts:** MoSPI/NSO, ORGI, PIB, RBI, India Code, official Gazette records, Parliament answers and OEA/DPIIT.
2. **Official institutional sources used for historical biography:** MoSPI life sketches and the ISI Annual Report. These are authoritative institutional sources, though not all are the original research papers.
3. **Original research records used where available:** Bose–Shrikhande's PNAS paper and the Bose–Mesner article record/full text.
4. **Secondary material:** MacTutor, ASA, Carnegie, PRS and current-affairs reporting are retained only as supplementary context where relevant; they are not used as primary authority for current legal status or official statistics.
5. **Books:** references to recommended textbooks remain reading suggestions. No specific book edition or page is represented as checked.
6. **Access limitations:** SRS 2024 and MMR 2022–24 PDFs could not be retrieved; the OEA WPI/PPI portal timed out. Their source records/links are supplied, but the affected claims require page-level reviewer confirmation before merge.

No homepage-only visit is represented as proof of a specific table, page, legal provision or publication date.

## Facts requiring periodic updating

| Fact set | Update trigger / recommended review |
|---|---|
| NSC composition, mandate and current members | On every new Government resolution, annual report or RTI-manual revision |
| NSS Steering Committee | Before describing it as active; original two-year term ended June 2026 |
| GDP/CPI/IIP/WPI base years, baskets and linking factors | Whenever a new base series, revised release or linking-factor note is published |
| RBI inflation target | At the end of the notified period (31 March 2031) or earlier notification |
| ASI, ASUSE and PLFS | Every annual report/factsheet; update latest reference period, sample frame and coverage |
| HCES | On each new round; update periodicity, reference periods, MPCE, weights and comparability caveats |
| NFHS | When NFHS-6 official factsheets/final report are released |
| WPI/PPI transition | Review the five-year transition and intended WPI discontinuation date (June 2031) against the full OEA order |
| Census 2027 | Every Gazette notification, state schedule, reference-date change or official Census backgrounder |
| RBD Act / Rules | Every amendment, commencement notification or rule change |
| CRS registration levels | Every annual Vital Statistics Report |
| SRS and MMR rates | Every SRS Statistical Report, SRS bulletin and MMR special bulletin; check tables before replacing figures |

## Files and validation

**Inspected**
- `seed/catalog.json` (actual catalog)
- `seed/lesson_10a1.json` through `seed/lesson_10a5.json`
- `seed/official_t1_mastery.json` through `seed/official_t5_mastery.json`

**Modified**
- The five lesson JSON files above
- The five mastery-pool JSON files above
- This audit report

**Not modified**
- `seed/catalog.json`, manifests, application code, shared tools, configuration, workflows, Paper 1 or any other module.

**Checks performed**
- All 10 modified JSON files parsed successfully.
- Catalog mapping checked: five topic IDs map to the five lesson files shown above.
- All five lessons retain 13 scenes.
- All five mastery pools retain 20 items.
- All lesson source references have verification date `2026-11-14`.
- The source records and claim ledger were reviewed manually.

**Not run / outstanding**
- Local `npm ci`, `npm run check`, `npm run build`, `npm test` and repository shell validators were not run in this environment.
- The latest GitHub Actions `Validate` run observed for the current branch head was **cancelled**. The new audit-report commit should trigger a fresh run; confirm its result before merge.
- SRS 2024/MMR table-level checks and the OEA WPI/PPI transition detail remain outstanding as described above.

## Publication decision

**Draft review only. Do not merge or deploy.** The SRS 2024 and MMR tables require page-level confirmation, and the WPI/PPI transition needs confirmation against the full OEA release. The user retains control of review, merge and deployment.
