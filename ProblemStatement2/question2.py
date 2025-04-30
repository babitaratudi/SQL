import pandas as pd
from pandasql import sqldf

# Load Excel sheet
OrderData = pd.read_excel("TSCAssignment.xlsx", sheet_name=1, header=0)  # Change sheet name if needed
UserLevelData = pd.read_excel("TSCAssignment.xlsx", sheet_name=2 , header=0)  # Change sheet name if needed

OrderData.columns = OrderData.columns.str.lower()
UserLevelData.columns = UserLevelData.columns.str.lower()

print(OrderData.columns)
print(UserLevelData.columns)

# # Write SQL query
query = """
WITH user_revenue AS (
  SELECT
    u.industry,
    o.userid,
    SUM(o.invoice) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY u.industry ORDER BY SUM(o.invoice) DESC) AS rank
  FROM
    OrderData o
  JOIN
    UserLevelData u ON o.userid = u.userid
  GROUP BY
    u.industry, o.userid
)

SELECT
  industry,
  userid,
  total_revenue
FROM
  user_revenue
WHERE
  rank <= 2
ORDER BY
  industry,
  total_revenue DESC
"""

# # # Run SQL query
result = sqldf(query, locals())

# Add a dollar sign to the total_avg_monthly_revenue column
result['total_revenue'] = result['total_revenue'].apply(lambda x: f"${x}")

# # # Save result to new Excel
result.to_excel('question2_output.xlsx', index=False)