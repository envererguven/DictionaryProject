import sqlite3
import os

# The database is located inside the 'app' directory
DB_PATH = os.path.join('app', 'dictionary.db')

def drop_table():
    """Connects to the database and drops the 'translations' table."""
    try:
        # Check if the database file exists before trying to connect
        if not os.path.exists(DB_PATH):
            print(f"Database file not found at '{DB_PATH}'. Nothing to do.")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        print("Dropping table 'translations'...")
        c.execute("DROP TABLE IF EXISTS translations")
        
        conn.commit()
        conn.close()
        print("Table 'translations' has been successfully dropped.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # This confirmation step prevents accidental deletion
    confirm = input("Are you sure you want to drop the 'translations' table? This cannot be undone. (yes/no): ")
    if confirm.lower() == 'yes':
        drop_table()
    else:
        print("Operation cancelled.")import sqlite3
import os

# The database is located inside the 'app' directory
DB_PATH = os.path.join('app', 'dictionary.db')

def drop_table():
    """Connects to the database and drops the 'translations' table."""
    try:
        # Check if the database file exists before trying to connect
        if not os.path.exists(DB_PATH):
            print(f"Database file not found at '{DB_PATH}'. Nothing to do.")
            return

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        print("Dropping table 'translations'...")
        c.execute("DROP TABLE IF EXISTS translations")
        
        conn.commit()
        conn.close()
        print("Table 'translations' has been successfully dropped.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # This confirmation step prevents accidental deletion
    confirm = input("Are you sure you want to drop the 'translations' table? This cannot be undone. (yes/no): ")
    if confirm.lower() == 'yes':
        drop_table()
    else:
        print("Operation cancelled.")
