import json
import pandas as pd
import sqlite3
#import requests
#import subprocess
import sys
def main():
    print("This is the main function")

#subprocess.run(["python", "json_llm.py"])
    
def determine_file_format(file_path):
    """Determine the file format of the given file."""
    with open(file_path, 'rb') as f:
        file_content = f.read(8)

    if file_content.startswith(b'\x50\x4B\x03\x04'):
        return 'Microsoft Excel'
    elif file_content.startswith(b'\xEF\xBB\xBF'):
        return 'JSON'
    elif file_content.startswith(b'SQLite format 3\000'):
        return 'SQLite database'
    else:
        return 'CSV'

def convert_excel_to_csv(excel_file, csv_file):
    """Convert an Excel file to a CSV file."""
    df = pd.read_excel(excel_file)
    df.to_csv(csv_file, index=False)

def convert_json_to_csv(json_file, csv_file):
    """Convert a JSON file to a CSV file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)

def convert_sql_to_csv(db_file, table_name, csv_file):
    """Convert a SQLite database file to a CSV file."""
    conn = sqlite3.connect(db_file)
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    df.to_csv(csv_file, index=False)
    conn.close()

def convert_file_to_json(file_path, json_file):
    """Convert a file to a JSON file."""
    file_format = determine_file_format(file_path)

    if file_format == 'Microsoft Excel':
        # Excel file
        csv_file = 'log_data.csv'  # Create the file if it doesn't exist
        convert_excel_to_csv(file_path, csv_file)
        df = pd.read_csv(csv_file)
        json_data = df.to_json()
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        print(f"Created log_data.json")
    elif file_format == 'JSON':
        # JSON file
        json_data = json.load(open(file_path))
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        print(f"Created log_data.json")
    elif file_format == 'SQLite database':
        # SQLite database file
        csv_file = 'log_data.csv'  # Create the file if it doesn't exist
        db_table_name = 'your_table_name'  # Replace with your table name
        convert_sql_to_csv(file_path, db_table_name, csv_file)
        df = pd.read_csv(csv_file)
        json_data = df.to_json()
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        print(f"Created log_data.json")
    else:
        # CSV file
        json_data = pd.read_csv(file_path).to_json()
        with open(json_file, 'w') as f:
            json.dump(json_data, f)
        print(f"Created log_data.json")

if __name__ == "__main__":
    input_file_path = "/path/to/your/input/file.txt"  # Replace with the actual file path

    with open(input_file_path, 'r') as f:
        input_data = f.read()
    print("hiiii")
    convert_file_to_json(input_data,"input.json")
