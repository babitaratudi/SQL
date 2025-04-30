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

# # Write SQL query
query = """
SELECT
    u.industry,
    ROUND(SUM(o.invoice) / COUNT(DISTINCT (strftime('%Y-%m', o.purchase_date))), 2) AS total_avg_monthly_revenue
FROM
    OrderData o
    JOIN
    UserLevelData u ON o.userid = u.userid
GROUP BY
    u.industry
ORDER BY
    total_avg_monthly_revenue DESC
"""

# # # Run SQL query
result = sqldf(query, locals())

# Add a dollar sign to the total_avg_monthly_revenue column
result['total_avg_monthly_revenue'] = result['total_avg_monthly_revenue'].apply(lambda x: f"${x}")

# # # Save result to new Excel
result.to_excel('question1_output.xlsx', index=False)