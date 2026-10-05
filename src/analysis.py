"""Customer Churn & Retention Analysis: SQL join -> Pandas EDA -> stats -> drivers."""
import pandas as pd, numpy as np, sqlite3, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, seaborn as sns
from scipy import stats
sns.set_theme(style="whitegrid"); NAVY="#1F3864"; RED="#C0392B"
con = sqlite3.connect("data/churn.db")
df = pd.read_sql(open("sql/01_schema_and_join.sql").read(), con)
df["churn"] = (df.Churn=="Yes").astype(int)
out=[]; P=lambda *a: out.append(" ".join(str(x) for x in a))

# 1. Overview + descriptive statistics
P("ROWS:",len(df),"| CHURN RATE: %.2f%%"%(df.churn.mean()*100))
P("\nDESCRIPTIVE STATS (numeric) by churn:\n", df.groupby("Churn")[["tenure","MonthlyCharges","TotalCharges"]].agg(["mean","median"]).round(2).to_string())

# 2. Churn rate by segment
def rate(col):
    g=df.groupby(col).churn.agg(["count","mean"]); g["mean"]=(g["mean"]*100).round(2)
    return g.rename(columns={"mean":"churn_pct"}).sort_values("churn_pct",ascending=False)
for c in ["Contract","InternetService","TechSupport","OnlineSecurity","PaymentMethod","PaperlessBilling","SeniorCitizen","Partner","Dependents"]:
    P(f"\nCHURN BY {c}:\n", rate(c).to_string())
df["tenure_bucket"]=pd.cut(df.tenure,[-1,12,24,48,72],labels=["0-12","13-24","25-48","49-72"])
P("\nCHURN BY tenure_bucket:\n", rate("tenure_bucket").to_string())

# 3. Correlation analysis
num=df[["tenure","MonthlyCharges","TotalCharges","churn"]]
P("\nPEARSON CORRELATION WITH CHURN:\n", num.corr()["churn"].round(3).to_string())
enc=pd.get_dummies(df.drop(columns=["customerID","Churn","tenure_bucket"]),drop_first=True).astype(float)
corr=enc.corr()["churn"].drop("churn").sort_values()
P("\nTOP 8 POSITIVE (raise churn):\n", corr.tail(8)[::-1].round(3).to_string())
P("\nTOP 8 NEGATIVE (lower churn):\n", corr.head(8).round(3).to_string())

# 4. Hypothesis tests
def chi(col):
    ct=pd.crosstab(df[col],df.churn); chi2,p,_,_=stats.chi2_contingency(ct); return chi2,p
P("\nCHI-SQUARE TESTS (H0: churn independent of feature):")
for c in ["Contract","InternetService","TechSupport","PaymentMethod","PaperlessBilling","gender"]:
    chi2,p=chi(c); P(f"  {c:18s} chi2={chi2:8.1f}  p={p:.2e}  ->", "significant" if p<0.05 else "NOT significant")
t,p=stats.ttest_ind(df[df.churn==1].tenure, df[df.churn==0].tenure, equal_var=False)
P(f"  Welch t-test tenure churned vs retained: t={t:.1f}, p={p:.2e}")
t,p=stats.ttest_ind(df[df.churn==1].MonthlyCharges, df[df.churn==0].MonthlyCharges, equal_var=False)
P(f"  Welch t-test monthly charges churned vs retained: t={t:.1f}, p={p:.2e}")

# 5. Revenue at risk + high-risk segment
risk=df[(df.Contract=="Month-to-month")&(df.tenure<=12)]
P("\nHIGH-RISK SEGMENT (month-to-month, tenure<=12m): customers=%d (%.1f%% of base), churn=%.1f%%"%(len(risk),len(risk)/len(df)*100,risk.churn.mean()*100))
lost=df[df.churn==1].MonthlyCharges.sum()
P("MONTHLY REVENUE LOST TO CHURN: %.0f (%.1f%% of total monthly revenue)"%(lost,lost/df.MonthlyCharges.sum()*100))
fo=df[(df.InternetService=="Fiber optic")]
P("FIBER: churn with TechSupport=No: %.1f%% vs TechSupport=Yes: %.1f%%"%(fo[fo.TechSupport=="No"].churn.mean()*100, fo[fo.TechSupport=="Yes"].churn.mean()*100))
open("outputs_summary.txt","w").write("\n".join(out)); print("\n".join(out))

# 6. Charts
fig,ax=plt.subplots(1,3,figsize=(15,4.2))
r=rate("Contract").reset_index(); sns.barplot(data=r,x="Contract",y="churn_pct",color=NAVY,ax=ax[0]); ax[0].set_title("Churn % by Contract")
r=rate("tenure_bucket").reset_index().sort_values("tenure_bucket"); sns.barplot(data=r,x="tenure_bucket",y="churn_pct",color=NAVY,ax=ax[1]); ax[1].set_title("Churn % by Tenure (months)")
r=rate("InternetService").reset_index(); sns.barplot(data=r,x="InternetService",y="churn_pct",color=NAVY,ax=ax[2]); ax[2].set_title("Churn % by Internet Service")
for a in ax:
    a.set_ylabel("Churn %"); a.set_xlabel("")
    for c in a.containers: a.bar_label(c,fmt="%.1f%%")
plt.tight_layout(); plt.savefig("charts/churn_by_segment.png",dpi=150); plt.close()
fig,ax=plt.subplots(figsize=(7,5)); sns.kdeplot(data=df,x="tenure",hue="Churn",fill=True,common_norm=False,palette={"No":NAVY,"Yes":RED},ax=ax)
ax.set_title("Tenure distribution: churned customers leave early"); plt.tight_layout(); plt.savefig("charts/tenure_distribution.png",dpi=150); plt.close()
top=pd.concat([corr.head(8),corr.tail(8)]).sort_values()
fig,ax=plt.subplots(figsize=(8,6)); ax.barh(top.index,top.values,color=[NAVY if v<0 else RED for v in top.values]); ax.set_title("Top correlations with churn"); plt.tight_layout(); plt.savefig("charts/churn_drivers_correlation.png",dpi=150); plt.close()
