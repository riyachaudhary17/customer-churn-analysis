-- Overall churn rate
SELECT ROUND(100.0*SUM(Churn='Yes')/COUNT(*),2) AS churn_pct FROM customers;

-- Churn by contract type
SELECT k.Contract, COUNT(*) AS customers,
       ROUND(100.0*SUM(c.Churn='Yes')/COUNT(*),2) AS churn_pct
FROM customers c JOIN contracts k USING(customerID)
GROUP BY k.Contract ORDER BY churn_pct DESC;

-- Churn by tenure bucket
SELECT CASE WHEN tenure<=12 THEN '0-12' WHEN tenure<=24 THEN '13-24'
            WHEN tenure<=48 THEN '25-48' ELSE '49+' END AS tenure_bucket,
       COUNT(*) AS customers,
       ROUND(100.0*SUM(Churn='Yes')/COUNT(*),2) AS churn_pct
FROM customers GROUP BY 1 ORDER BY MIN(tenure);

-- Churn by internet service and tech support
SELECT s.InternetService, s.TechSupport, COUNT(*) AS customers,
       ROUND(100.0*SUM(c.Churn='Yes')/COUNT(*),2) AS churn_pct
FROM customers c JOIN services s USING(customerID)
GROUP BY 1,2 ORDER BY churn_pct DESC;
