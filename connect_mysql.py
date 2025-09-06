import pandas as pd
import mysql.connector

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",       
    user="root",           
    password="Khushi@1608",
    database="project"     
)

# Step 2: Query data from SensorsData table
query = "SELECT * FROM SensorsData;"

# Step 3: Fetch into DataFrame
df = pd.read_sql(query, conn)

# Step 4: Print first 5 rows
print("Data from SensorsData table:")
print(df.head())

# Step 5: Close connection
conn.close()
