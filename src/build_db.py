"""Split the flat CSV into 4 relational tables in SQLite (mimics a real warehouse)."""
import pandas as pd, sqlite3
df = pd.read_csv("data/telco_raw.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].str.strip(), errors="coerce")  # 11 blank rows (tenure 0)
df["TotalCharges"] = df["TotalCharges"].fillna(0)
con = sqlite3.connect("data/churn.db")
cols = {
 "customers":["customerID","gender","SeniorCitizen","Partner","Dependents","tenure","Churn"],
 "services":["customerID","PhoneService","MultipleLines","InternetService","OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies"],
 "contracts":["customerID","Contract","PaperlessBilling","PaymentMethod"],
 "billing":["customerID","MonthlyCharges","TotalCharges"]}
for t,c in cols.items(): df[c].to_sql(t,con,if_exists="replace",index=False)
con.close(); print("built", {t:len(df) for t in cols})
