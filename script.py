import sqlite3
import pandas as pd # type: ignore

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Queries Dictionary
queries = {
    "finance_lending_blockchain_clients": """
        SELECT industry, COUNT(client_id) 
        FROM clients 
        WHERE industry IN ('Finance Lending', 'Blockchain') 
        GROUP BY industry;
    """,
    "highest_renewal_rate": """
        SELECT industry, (SUM(renewed) * 100.0 / COUNT(client_id)) AS renewal_rate 
        FROM clients 
        GROUP BY industry 
        ORDER BY renewal_rate DESC 
        LIMIT 1;
    """,
    "average_inflation_rate": """
        SELECT AVG(ir.average_inflation_rate) AS avg_inflation_rate 
        FROM subscriptions s 
        JOIN inflation_rates ir 
        ON strftime('%Y', s.renewal_date) = strftime('%Y', ir.year);
    """,
    "median_payment_per_year": """
        WITH PaymentRanked AS (
            SELECT amount_paid, 
                   payment_method, 
                   renewal_date,
                   ROW_NUMBER() OVER (PARTITION BY strftime('%Y', renewal_date) ORDER BY amount_paid) AS row_num,
                   COUNT(*) OVER (PARTITION BY strftime('%Y', renewal_date)) AS total_count
            FROM subscriptions
        )
        SELECT renewal_date, AVG(amount_paid) AS median_amount
        FROM PaymentRanked
        WHERE row_num IN (total_count / 2, total_count / 2 + 1)
        GROUP BY renewal_date;
    """
}

# Execute and display query results
for name, query in queries.items():
    try:
        df = pd.read_sql_query(query, conn)
        print(f"\n{name.upper()}:\n", df)
    except Exception as e:
        print(f"Error executing {name}: {e}")

# Close connection
conn.close()

