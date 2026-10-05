# Customer Churn & Retention Analysis

End-to-end analysis of **why customers leave** a telecom subscription business and **what to do about it**.
**Stack:** SQL (SQLite) · Python · Pandas · NumPy · SciPy · Matplotlib · Seaborn

## Business question
Which customers churn, what drives it, how much revenue is at risk, and which retention actions are worth testing?

## Data
Public IBM Telco Customer Churn dataset (7,043 customers, 21 attributes).
To mimic a real warehouse, the flat file is split into 4 relational tables
(`customers`, `services`, `contracts`, `billing`) in SQLite and re-joined with SQL
into one analysis-ready dataset (`sql/01_schema_and_join.sql`).

## Method
1. **SQL**: build and join 4 tables; segment churn queries (`sql/02_churn_queries.sql`)
2. **Pandas cleaning**: fixed 11 blank `TotalCharges` values (new customers, tenure 0)
3. **Descriptive statistics**: mean/median tenure and charges, churned vs retained
4. **Correlation analysis**: Pearson on numeric + one-hot encoded features
5. **Hypothesis testing**: chi-square (categorical) and Welch t-test (numeric)

## Key findings
| Finding | Evidence |
|---|---|
| Overall churn | **26.5%** (1,869 of 7,043) |
| Contract is the strongest lever | Month-to-month **42.7%** vs one-year 11.3% vs two-year 2.8% |
| Early tenure is the danger zone | **47.4%** churn in months 0-12 vs 9.5% after 49 months |
| Fiber customers churn most | **41.9%** vs DSL 19.0% |
| Support/security cuts churn | No tech support **41.6%** vs with tech support 15.2% |
| Fiber + no tech support | **49.4%** churn vs 22.6% with tech support |
| Payment friction | Electronic check **45.3%** vs automatic payments 15-17% |
| Pricing signal | Churned customers pay more: avg monthly **74.4 vs 61.3** |
| Gender is irrelevant | chi-square p = 0.49 (not significant) |
| High-risk segment | Month-to-month and tenure <= 12m: **28.3% of customers, 51.4% churn** |
| Revenue at risk | Churned customers = **30.5%** of total monthly revenue |

All drivers above are statistically significant (p < 0.001) except gender.
Tenure has the strongest correlation with churn (r = -0.35).

## Recommendations
1. **Onboarding program for months 0-12**: proactive check-ins, since nearly half of churn happens here.
2. **Contract migration offer**: discount to move month-to-month customers to 1-year contracts.
3. **Bundle tech support and online security** with fiber plans; test a free trial period.
4. **Push automatic payments**: small incentive to move electronic-check users to auto-pay.
5. **Review fiber pricing/quality**: highest churn and highest charges.
6. **Validate with an A/B test** before rollout: measure 90-day churn in treated vs control.

## Limitations
Correlation is not causation; the dataset is a single snapshot with no time dimension, so
recommendations should be validated experimentally.

## Run it
```bash
pip install -r requirements.txt
python src/build_db.py
python src/analysis.py   # prints results, saves charts/ and outputs_summary.txt
```
