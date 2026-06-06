# Customer-Engagement-Product-Utilization-Analytics-for-Retention-Strategy - European-Central-Bank
This project analyzes European banking customer data to evaluate churn behavior, customer loyalty, engagement trends, and credit score distribution using interactive Power BI dashboards ,Streamlit live analytics and SQL-driven analytics on 2025 data.
This project evaluates retention through the lens of customer behavior and relationship strength.
# Background and Context
Banks increasingly recognize that customer behavior and engagement—not just demographics—determine long-term retention. Customers may appear financially strong (high balance or salary) but still churn due to:
* Low engagement
* Limited product adoption
* Weak relationship depth with the bank

  
Understanding how customers use banking products and services is essential to designing:
* Cross-sell strategies
* Loyalty programs
* Engagement-driven retention initiatives

# Project Objectives
  * Evaluate the relationship between engagement and churn
  * Measure retention impact of product count and product mix
  * Identify disengaged yet high-value customers

# Dataset Description
  ![img](Images/Data.png)
| Column|	Description|
|---|---|
|CustomerId|Unique customer identifier|
|Surname|	Customer surname|
|CreditScore	|Customer creditworthiness|
|Geography	|France, Spain, Germany|
|Gender	|Male / Female|
|Age	|Customer age|
|Tenure	|Years with the bank|
|Balance|	Account balance|
|NumOfProducts|	Number of bank products|
|HasCrCard|	Credit card ownership|
|IsActiveMember|	Activity indicator|
|EstimatedSalary|	Estimated annual salary|
|Exited|	Churn indicator (target)|
### Dashboard
<p>
  <img src="Images/Dashboard_1.png"
    width="45%">
  <img src="Images/Dashboard_2.png"
    width="45%">
</p>
For this analysis, an interactive dashboard was developed in Power BI that allows observation of the behavior of 10K banking customers in Europe. It has different slicers that allow the selection of specific characteristics for detailed analysis. Some measures were also created that complement the information provided by the dataset.

# Product Utilization  Analysis 
### Single-product vs multi-product retention
Retention rates among single-product customers are lower compared to multi-product customers, indicating stronger loyalty and engagement among customers using multiple banking services such as credit cards, loans, and insurance products. Long-term customers demonstrate higher product adoption and deeper banking relationships over time. Out of 10K total customers, 5.08K are single-product customers, while 4.92K are multi-product customers. The customer base consists of 5.46K male customers and 4.54K female customers.

France has the highest customer concentration with 5.01K customers, where single-product and multi-product customer distributions are nearly balanced, and male customers slightly outnumber female customers. Germany has 2.51K customers, with male customers representing a higher proportion than female customers. Spain has 2.48K customers, where male customers also slightly exceed female customers in distribution.
<p>
  <img src="Images/Retention.png"
    width="45%">
  <img src="Images/TenureProduct.png"
    width="45%">
</p>

### Churn Rate 
Single-product customers exhibit significantly higher churn rates compared to multi-product customers, suggesting that customers with limited product engagement are more likely to leave the bank. In contrast, customers using multiple banking services such as credit cards, loans, and insurance products demonstrate stronger retention and long-term engagement.

Long-term customers also show higher churn levels than newer customers, indicating that extended tenure alone does not guarantee loyalty. This may result from changing financial needs, dissatisfaction with banking services, lack of personalized engagement, or competitive offers from other banks.

The overall churn rate is 20.37%, with female customers contributing 11.39% and male customers contributing 8.98%, indicating that female customers experience comparatively higher churn. This suggests potential differences in customer satisfaction, service expectations, or engagement patterns across gender segments.
<p>
  <img src="Images/ChurnProduct.png"
    width="35%">
  <img src="Images/Churntenure.png"
    width="60%">
</p>

# Financial Commitment vs Engagement Analysis
###  Salary–balance mismatch detection
This analysis evaluates customer financial commitment by comparing estimated salary with current account balance to identify unusual balance patterns and potential financial mismatches. The study highlights customers with high salaries but very low balances, as well as customers with low salaries but unexpectedly high balances, helping identify irregular financial behavior, disengagement patterns, or potential risk segments. Additionally, customers maintaining zero account balances were analyzed as possible indicators of inactivity or churn risk.

The analysis also examines customers who actively use credit card services, focusing on their average account balances, product adoption behavior, and overall financial engagement. Customers using two or more banking products demonstrate stronger product depth and higher engagement levels compared to single-product users. Furthermore, the average credit score of credit card users was analyzed to evaluate financial reliability, customer quality, and creditworthiness across engaged banking segments.




<table>
<tr>
<td>

| Details | Value |
|---|---|
| 💳 Total Credit Card Users | 7.06K |
| 👩 Female Credit Card Users | 3.19K |
| 👨 Male Credit Card Users | 3.86K |
| 🧑 Young Customers (≤23) | 225 |
| 🚨 Churned Customers | 1.42K |
| ⚠️ Churned Young Customers | 16 |
| 🏦 Zero Balance Customers | 2.592K |
| 📈 Avg Credit Score | 650.19 |
| ⏳ Avg Tenure | 5.05 Years |

</td>

<td>
  
## 📉 Credit Card Churn Distribution by Geography
  
| 🌍 Geography | 💳 Total Credit Card Customers | 🚨 Churned Customers | 📉 Churn Rate |
|---|---|---|---|
|France|3.54K|569|16.07%|
|Germany|1.79K|577|32.23%|
|Spain|1.72K|278|16.16%|

</td>
</tr>
</table>

## Customer Risk Classification
* At Risk: Customer has churned (Exited = 1) or is inactive{IsActiveMember = 0}.
* Stable: Customer has not churned and remains an active member.
<p>
  <img src="Images/atrisk.png"
    width="35%">
</p>







# Skills and Tools
* Data analysis
* Critical thinking
* Dashboard creation
* Power BI

