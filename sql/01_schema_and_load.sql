-- ============================================================
-- HR Analytics & Employee Attrition - MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS hr_analytics;
USE hr_analytics;

CREATE TABLE IF NOT EXISTS employees (
    EmployeeID                  VARCHAR(20) PRIMARY KEY,
    Age                         INT,
    Gender                      VARCHAR(10),
    Department                  VARCHAR(50),
    JobRole                     VARCHAR(50),
    Education                   VARCHAR(30),
    EducationField              VARCHAR(50),
    MaritalStatus               VARCHAR(20),
    BusinessTravel              VARCHAR(30),
    MonthlyIncome               INT,
    PercentSalaryHike           INT,
    YearsAtCompany              INT,
    YearsInCurrentRole          INT,
    YearsSinceLastPromotion     INT,
    TotalWorkingYears           INT,
    NumCompaniesWorked          INT,
    OverTime                    VARCHAR(5),
    JobSatisfaction             INT,
    EnvironmentSatisfaction     INT,
    WorkLifeBalance             INT,
    RelationshipSatisfaction    INT,
    JobInvolvement              INT,
    PerformanceRating           INT,
    DistanceFromHome            INT,
    Attrition                   VARCHAR(5)
);

-- ============================================================
-- Import instructions (MySQL Workbench):
-- Right-click employees table → Table Data Import Wizard
-- Select data/employee_data.csv → Finish
-- ============================================================
