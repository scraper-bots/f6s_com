# F6S — Kazakhstan Startups (Analysis & Visuals)
This README accompanies the chart assets and analysis generated from the `f6s_kazakhstan_companies.csv` dataset. It contains the geographic chart (companies by city), a concise set of verified statistics derived from the dataset, and **actionable insights** derived from the actual numeric values.
## Geographic Distribution
![Companies by City](charts/02_geographic_distribution.png)
_Figure: Horizontal bar chart — number of companies per city (saved to `charts/02_geographic_distribution.png`)._
## Key summary statistics (computed from dataset)
| Metric | Value |
|---|---:|
| Total companies | 96 |
| Cities represented | 7 |
| Industries represented | 10 |
| Total funding (USD) | $3.67M |
| Funded companies | 18 |
| Companies with investors | 35 |
| Average funding (funded companies) | $204K |
| Average team size | 1.2 |
| Top city (companies) | Almaty (57) |
| Top industry (companies) | AI & Machine Learning (53) |
| Most funded company | Gen2B |
| Most funded amount (USD) | $1.30M |

### Top funding by industry (top 5)
| Industry | Total funding |
|---|---:|
| AI & Machine Learning | $3.50M |
| SaaS & Enterprise Software | $100K |
| FinTech | $50K |
| Other | $15K |
| Blockchain & Web3 | $5K |

### Top investors by number of portfolio entries (top 10)
| Investor | Count |
|---|---:|
| Murat Aibassov | 5 |
| Activat | 4 |
| Kairat Dikhayev | 2 |
| Yerlan Kondybayev | 2 |
| Astana Hub | 1 |
| Vladimir Popov | 1 |
| Alexey Shangin | 1 |
| Yevgeniy Samoilenko | 1 |
| Vladislav Vinogradov | 1 |
| Microsoft for Startups | 1 |

## Data completeness (percent of records populated)
| Field | Completeness (%) |
|---|---:|
| company_name | 100.0% |
| tagline | 96.9% |
| location | 100.0% |
| founded_year | 83.3% |
| funding_amount | 18.8% |
| investors | 36.5% |
| team_members | 86.5% |
| description | 82.3% |

## Actionable insights (driven by dataset values)
The following recommendations are directly tied to the numbers above. Each action is prioritized and includes a short rationale.
### 1) Support geographic diversification — prioritize regions outside the top city
- **Observation:** Almaty hosts 57 of 96 companies (59.4%).
- **Why it matters:** High concentration increases regional competition for talent, capital, and mentorship, leaving underserved cities with less growth potential.
- **Action:** Establish 2–3 targeted outreach & incubator programs in the next 12 months for cities in the 2nd–5th rank by company count. Pilot mentorship hubs + local investor roadshows. Use the dataset's city ranking to select targets.

### 2) Channel sector-specific investor matchmaking
- **Observation:** AI & Machine Learning leads funding with $3.50M (top 5 industries shown above).
- **Why it matters:** Concentrated capital flows imply repeatable investor thesis — matching similar startups to active investors raises fundraising success rates.
- **Action:** Create sector briefs (one-page decks) for the top 3 funded industries and present them to local and regional VCs. Include traction metrics from the dataset (team sizes, founding year distribution, and exemplar funded companies).

### 3) Increase funding access — many companies are unfunded or micro-funded
- **Observation:** 18 out of 96 (18.8%) companies have recorded funding; total funding is $3.67M.
- **Why it matters:** Low funding penetration suggests a large pool of early-stage ventures needing capital, which is both an opportunity for angel syndicates and a sign that many teams are pre-seed.
- **Action:** Promote structured seed programs: (a) a rolling angel demo day quarterly; (b) a matching platform for founders and micro-investors (ticket sizes $10k–$100k). Track conversion and re-run using dataset as baseline.

### 4) Improve dataset completeness to raise analysis confidence
- **Observation:** Several fields show incomplete coverage (see completeness table). In particular, fields with <70% completeness should be prioritized.
- **Fields to prioritize for cleanup:** funding_amount, investors.
- **Action:** Implement a lightweight enrichment pipeline: (1) standardize location names; (2) attempt automated enrichment for missing founded years and team counts via company websites/LinkedIn; (3) normalise investor names using fuzzy matching and a canonical mapping. Target a 90% completeness for core fields within 3 months.

### 5) Tailor support by company maturity and team size
- **Observation:** Average team size is 1.2. Age distribution shows many early-stage companies (refer to founding-year timeline chart saved separately).
- **Why it matters:** Acceleration programs need to be calibrated — very small teams require founder training and business development; larger teams are investment-ready.
- **Action:** Create two program tracks: 'Pre-seed builder' (0–3 team members, focus: MVP & customer discovery) and 'Scale readiness' (4+ members, focus: metrics, sales, investor readiness). Use dataset filters to populate cohorts.

## Closing notes & next steps
1. The dataset and chart assets live alongside this README. The geographic bar chart is referenced above (`charts/02_geographic_distribution.png`).
2. Next recommended deliverables (rapid, priority-ordered):
   - Clean investor canonicalisation and produce a 'lead investor' shortlist (2 weeks).
   - Build a simple dashboard (interactive) showing funding by city and industry with filters (4 weeks).
   - Outreach plan to top 5 'other' cities to seed two pilot incubators (12 weeks).

---
_This README was generated programmatically from `f6s_kazakhstan_companies.csv`. Contact the data steward for updates or to request additional slices of analysis._
