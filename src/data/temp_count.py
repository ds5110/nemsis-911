import sqlite3

conn = sqlite3.connect('../db/NEMSIS_PUB.db')
cursor = conn.cursor()

# Find duplicate PcrKey values in FACTPCRARRESTROSC
cursor.execute("""
    SELECT PcrKey, COUNT(*)
    FROM FACTPCRARRESTROSC
    GROUP BY PcrKey
    HAVING COUNT(*) > 1
""")
duplicates_rosc = cursor.fetchall()

# Find duplicate PcrKey values in FACTPCRARRESTWITNESS
cursor.execute("""
    SELECT PcrKey, COUNT(*)
    FROM FACTPCRARRESTWITNESS
    GROUP BY PcrKey
    HAVING COUNT(*) > 1
""")
duplicates_witness = cursor.fetchall()

conn.close()

# Print the duplicate PcrKey values (if any)
print("Duplicate PcrKey values in FACTPCRARRESTROSC:")
for row in duplicates_rosc:
    print(f"PcrKey: {row[0]}, Count: {row[1]}")

print("\nDuplicate PcrKey values in FACTPCRARRESTWITNESS:")
for row in duplicates_witness:
    print(f"PcrKey: {row[0]}, Count: {row[1]}")
