import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

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
# Step 2: Get data from MySQL
# --------------------------
query = """
SELECT s.temperature, s.vibration, s.power_consumption, s.output_units,
       CASE WHEN m.issue_reported IS NOT NULL THEN 1 ELSE 0 END AS maintenance_needed
FROM SensorsData s
LEFT JOIN MaintenanceLogs m 
ON s.machine_id = m.machine_id
LIMIT 500;
"""

df = pd.read_sql(query, conn)
conn.close()

print("Sample data from SensorsData table:\n")
print(df.head())

# --------------------------
# Step 3: Prepare features & labels
# --------------------------
X = df[["temperature", "vibration", "power_consumption", "output_units"]]
y = df["maintenance_needed"]

# --------------------------
# Step 4: Train-test split
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --------------------------
# Step 5: Train Random Forest Model
# --------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --------------------------
# Step 6: Evaluate Model
# --------------------------
y_pred = model.predict(X_test)
print("\nModel Performance:\n")
print(classification_report(y_test, y_pred))

# --------------------------
# Step 7: Predict new sensor reading
# --------------------------
# Example: temperature, vibration, power, output
new_data = [[85.0, 0.65, 240, 90]]  
prediction = model.predict(new_data)

print("\nPrediction for new data:", 
      "Maintenance Needed" if prediction[0] == 1 else "No Maintenance")