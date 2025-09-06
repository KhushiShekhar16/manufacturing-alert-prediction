import pandas as pd
import mysql.connector
from sklearn.ensemble import RandomForestClassifier

# --------------------------
# Step 1: Connect to MySQL
# --------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",            
    password="Khushi@1608",
    database="project"
)

# --------------------------
# Step 2: Get all sensor data
# --------------------------
query = """
SELECT reading_id, machine_id, timestamp, temperature, vibration, power_consumption, output_units
FROM SensorsData;
"""

df = pd.read_sql(query, conn)

# --------------------------
# Step 3: Prepare features
# --------------------------
features = ["temperature", "vibration", "power_consumption", "output_units"]
X = df[features]

# --------------------------
# Step 4: Train a simple Random Forest model
# --------------------------
# For demo, we use past maintenance as label
query_label = """
SELECT s.reading_id, 
       CASE WHEN m.issue_reported IS NOT NULL THEN 1 ELSE 0 END AS maintenance_needed
FROM SensorsData s
LEFT JOIN MaintenanceLogs m
ON s.machine_id = m.machine_id
LIMIT 500;
"""
label_df = pd.read_sql(query_label, conn)
y = label_df["maintenance_needed"]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --------------------------
# Step 5: Predict on all sensor data
# --------------------------
df["fail_prob"] = model.predict_proba(X)[:,1]
df["alert_flag"] = (df["fail_prob"] >= 0.5).astype(int)  # threshold 0.5

# --------------------------
# Step 6: Save predictions back to MySQL
# --------------------------
# Create table if not exists
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Predictions (
    pred_id INT AUTO_INCREMENT PRIMARY KEY,
    reading_id INT,
    machine_id INT,
    timestamp DATETIME,
    fail_prob FLOAT,
    alert_flag INT
);
""")
conn.commit()

# Insert predictions
for index, row in df.iterrows():
    cursor.execute("""
    INSERT INTO Predictions (reading_id, machine_id, timestamp, fail_prob, alert_flag)
    VALUES (%s, %s, %s, %s, %s)
    """, (row.reading_id, row.machine_id, row.timestamp, float(row.fail_prob), int(row.alert_flag)))

conn.commit()
conn.close()
print("Predictions saved to Predictions table successfully!")
