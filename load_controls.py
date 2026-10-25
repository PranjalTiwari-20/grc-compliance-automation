
import pandas as pd
import sqlite3

# Step 1: Read the Excel control matrix
file_path = "data/GRC_Control_Matrix_ID_Code_Description.xlsx"
controls = pd.read_excel(file_path)

# Step 2: Connect to the database
connection = sqlite3.connect("grc_database.db")

# Step 3: Identify each control's category
controls["Category"] = (
    controls["Control Code"].str.split("-").str[0]
)

# Step 4: Insert controls into the database
for _, row in controls.iterrows():
    connection.execute(
        """
        INSERT OR IGNORE INTO controls
        (id, control_code, control_description, category)
        VALUES (?, ?, ?, ?)
        """,
        (
            int(row["ID"]),
            row["Control Code"],
            row["Control Description"],
            row["Category"]
        )
    )

# Step 5: Save the changes
connection.commit()

# Step 6: Check the total number of controls
result = connection.execute(
    "SELECT COUNT(*) FROM controls"
).fetchone()

print("Controls loaded successfully!")
print("Total controls in database:", result[0])

# Step 7: Display the first five controls
rows = connection.execute(
    """
    SELECT id, control_code, category
    FROM controls
    ORDER BY id
    LIMIT 5
    """
).fetchall()

for row in rows:
    print(tuple(row))

connection.close()
