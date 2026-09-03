-- ============================================================
-- HR Analytics & Employee Attrition - Key SQL Queries (MySQL)
-- ============================================================

USE hr_analytics;

-- ----------------------------------------------------------
-- 1. OVERALL KPIs
-- ----------------------------------------------------------
SELECT 
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(MonthlyIncome), 0) AS avg_monthly_income,
    ROUND(AVG(YearsAtCompany), 1) AS avg_tenure_years,
    ROUND(AVG(Age), 1) AS avg_age
FROM employees;


-- ----------------------------------------------------------
-- 2. ATTRITION BY DEPARTMENT
-- ----------------------------------------------------------
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(AVG(MonthlyIncome), 0) AS avg_income
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;


-- ----------------------------------------------------------
-- 3. ATTRITION BY JOB ROLE
-- ----------------------------------------------------------
SELECT 
    JobRole,
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY JobRole, Department
ORDER BY attrition_rate_pct DESC;


-- ----------------------------------------------------------
-- 4. ATTRITION BY OVERTIME
-- ----------------------------------------------------------
SELECT 
    OverTime,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY OverTime;


-- ----------------------------------------------------------
-- 5. ATTRITION BY JOB SATISFACTION
-- ----------------------------------------------------------
SELECT 
    JobSatisfaction,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;


-- ----------------------------------------------------------
-- 6. ATTRITION BY WORK-LIFE BALANCE
-- ----------------------------------------------------------
SELECT 
    WorkLifeBalance,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;


-- ----------------------------------------------------------
-- 7. ATTRITION BY YEARS AT COMPANY (TENURE BANDS)
-- ----------------------------------------------------------
SELECT 
    CASE 
        WHEN YearsAtCompany = 0 THEN '0 years (New)'
        WHEN YearsAtCompany BETWEEN 1 AND 2 THEN '1-2 years'
        WHEN YearsAtCompany BETWEEN 3 AND 5 THEN '3-5 years'
        WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
        ELSE '10+ years'
    END AS tenure_band,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY 
    CASE 
        WHEN YearsAtCompany = 0 THEN '0 years (New)'
        WHEN YearsAtCompany BETWEEN 1 AND 2 THEN '1-2 years'
        WHEN YearsAtCompany BETWEEN 3 AND 5 THEN '3-5 years'
        WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
        ELSE '10+ years'
    END
ORDER BY MIN(YearsAtCompany);


-- ----------------------------------------------------------
-- 8. ATTRITION BY GENDER & MARITAL STATUS
-- ----------------------------------------------------------
SELECT 
    Gender,
    MaritalStatus,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY Gender, MaritalStatus
ORDER BY attrition_rate_pct DESC;


-- ----------------------------------------------------------
-- 9. SALARY ANALYSIS BY ATTRITION
-- ----------------------------------------------------------
SELECT 
    Attrition,
    COUNT(*) AS employees,
    ROUND(AVG(MonthlyIncome), 0) AS avg_monthly_income,
    ROUND(MIN(MonthlyIncome), 0) AS min_income,
    ROUND(MAX(MonthlyIncome), 0) AS max_income,
    ROUND(AVG(PercentSalaryHike), 1) AS avg_salary_hike
FROM employees
GROUP BY Attrition;


-- ----------------------------------------------------------
-- 10. PROMOTION & ATTRITION
-- ----------------------------------------------------------
SELECT 
    CASE 
        WHEN YearsSinceLastPromotion = 0 THEN 'Recently Promoted'
        WHEN YearsSinceLastPromotion BETWEEN 1 AND 3 THEN '1-3 years ago'
        ELSE '4+ years ago'
    END AS promotion_status,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_employees,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM employees
GROUP BY 
    CASE 
        WHEN YearsSinceLastPromotion = 0 THEN 'Recently Promoted'
        WHEN YearsSinceLastPromotion BETWEEN 1 AND 3 THEN '1-3 years ago'
        ELSE '4+ years ago'
    END
ORDER BY MIN(YearsSinceLastPromotion);
