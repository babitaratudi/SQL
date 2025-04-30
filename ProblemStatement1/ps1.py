import pandas as pd
from pandasql import sqldf

# Load Excel sheet
orders = pd.read_excel("PS1Assignment.xlsx", sheet_name=0, header=0)  # Change sheet name if needed
orders['Date'] = pd.to_datetime(orders['Date']).dt.strftime('%d-%b')
print(orders.columns)

# # Write SQL query
query = """
WITH original_orders AS (
  SELECT 
    Date,
    OrderId,
    [User Id],
    Category,
    Value,
    Qty,
    1 AS sort_order
  FROM orders
  WHERE Category != 'Bed + Mattress'
),
split_bed AS (
  SELECT 
    Date,
    OrderId,
    [User Id],
    'Bed' AS Category,
    CAST(Value * 0.80 AS INT) AS Value,
    Qty,
    2 AS sort_order
  FROM orders
  WHERE Category = 'Bed + Mattress'
),
split_mattress AS (
  SELECT 
    Date,
    OrderId,
    [User Id],
    'Mattress' AS Category,
    CAST(Value * 0.20 AS INT) AS Value,
    Qty,
    3 AS sort_order
  FROM orders
  WHERE Category = 'Bed + Mattress'
)

SELECT 
  Date, OrderId, [User Id], Category, Value, Qty
FROM (
  SELECT * FROM original_orders
  UNION ALL
  SELECT * FROM split_bed
  UNION ALL
  SELECT * FROM split_mattress
) AS combined
ORDER BY sort_order
"""

# # # Run SQL query
result = sqldf(query, locals())

# # # Save result to new Excel
result.to_excel('ps1_output.xlsx', index=False)