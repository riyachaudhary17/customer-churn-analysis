-- Analysis-ready dataset: join 4 relational tables (built in src/build_db.py)
SELECT c.customerID, c.gender, c.SeniorCitizen, c.Partner, c.Dependents, c.tenure,
       s.PhoneService, s.MultipleLines, s.InternetService, s.OnlineSecurity, s.OnlineBackup,
       s.DeviceProtection, s.TechSupport, s.StreamingTV, s.StreamingMovies,
       k.Contract, k.PaperlessBilling, k.PaymentMethod,
       b.MonthlyCharges, b.TotalCharges, c.Churn
FROM customers c
JOIN services  s ON s.customerID = c.customerID
JOIN contracts k ON k.customerID = c.customerID
JOIN billing   b ON b.customerID = c.customerID;
