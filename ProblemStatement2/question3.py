import pandas as pd
from pandasql import sqldf

# Load Excel sheet
OrderData = pd.read_excel("TSCAssignment.xlsx", sheet_name=1, header=0)  # Change sheet name if needed
UserLevelData = pd.read_excel("TSCAssignment.xlsx", sheet_name=2 , header=0)  # Change sheet name if needed

OrderData.columns = OrderData.columns.str.lower()
UserLevelData.columns = UserLevelData.columns.str.lower()

print(OrderData.columns)
print(UserLevelData.columns)
# Ensure purchase_date is in a proper date format
OrderData['purchase_date'] = pd.to_datetime(OrderData['purchase date'], format='%m/%d/%y')

# Corrected SQL query
query = """
WITH purchase_data AS (
  SELECT 
    userid,
    invoice,
    DATE(purchase_date) AS purchase_date,
    CAST(STRFTIME('%Y%m', purchase_date) AS INTEGER) AS purchase_month_key
  FROM OrderData
),
month_keys AS (
  SELECT 
    CAST(STRFTIME('%Y%m', DATE('2020-11-01')) AS INTEGER) AS current_month_key,
    CAST(STRFTIME('%Y%m', DATE('2020-11-01', '-1 month')) AS INTEGER) AS prev_month_key,
    CAST(STRFTIME('%Y%m', DATE('2020-11-01', '-2 month')) AS INTEGER) AS prev_1_month_key
)
SELECT 
  p.userid,
  ROUND(SUM(CASE WHEN p.purchase_month_key = m.current_month_key THEN p.invoice ELSE 0 END),2) AS current_month_revenue,
  COUNT(CASE WHEN p.purchase_month_key = m.current_month_key THEN 1 ELSE NULL END) AS current_month_orders,
  ROUND(SUM(CASE WHEN p.purchase_month_key = m.prev_month_key THEN p.invoice ELSE 0 END),2) AS prev_month_revenue,
  COUNT(CASE WHEN p.purchase_month_key = m.prev_month_key THEN 1 ELSE NULL END) AS prev_month_orders,
  ROUND(SUM(CASE WHEN p.purchase_month_key = m.prev_1_month_key THEN p.invoice ELSE 0 END),2) AS prev_1_month_revenue,
  COUNT(CASE WHEN p.purchase_month_key = m.prev_1_month_key THEN 1 ELSE NULL END) AS prev_1_month_orders
FROM purchase_data p
JOIN month_keys m
GROUP BY p.userid
ORDER BY p.userid
"""

# # # Run SQL query
result = sqldf(query, locals())

# Add a dollar sign to the total_avg_monthly_revenue column
result['current_month_revenue'] = result['current_month_revenue'].apply(lambda x: f"${x}")
result['prev_month_revenue'] = result['prev_month_revenue'].apply(lambda x: f"${x}")
result['prev_1_month_revenue'] = result['prev_1_month_revenue'].apply(lambda x: f"${x}")

# # # Save result to new Excel
result.to_excel('question3_output.xlsx', index=False)