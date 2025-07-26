import pandas as pd
import csv

def fix_csv_file():
    """Fix the CSV file by properly handling commas in the suggestions field"""
    input_file = "../data/simfluence_reddit_training.csv"
    output_file = "../data/simfluence_reddit_training_fixed.csv"
    
    print("🔧 Fixing CSV file...")
    
    # Read the file with proper CSV handling
    with open(input_file, 'r', encoding='utf-8') as file:
        # Use csv.reader to properly handle quoted fields
        reader = csv.reader(file)
        rows = list(reader)
    
    print(f"Original file has {len(rows)} rows")
    
    # Clean the data
    cleaned_rows = []
    for i, row in enumerate(rows):
        if len(row) != 19:
            print(f"Row {i+1} has {len(row)} fields instead of 19")
            # Try to fix by joining extra fields in the suggestions column
            if len(row) > 19:
                # Join the extra fields into the suggestions field
                suggestions = ','.join(row[18:])
                new_row = row[:18] + [suggestions]
                cleaned_rows.append(new_row)
            else:
                # Skip malformed rows
                print(f"Skipping row {i+1} due to insufficient fields")
                continue
        else:
            cleaned_rows.append(row)
    
    # Write the cleaned data
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_rows)
    
    print(f"Fixed file saved with {len(cleaned_rows)} rows")
    
    # Test the fixed file
    try:
        df = pd.read_csv(output_file)
        print(f"✅ Fixed file loads successfully: {df.shape}")
        return output_file
    except Exception as e:
        print(f"❌ Error loading fixed file: {e}")
        return None

if __name__ == "__main__":
    fixed_file = fix_csv_file()
    if fixed_file:
        print(f"✅ CSV file fixed successfully: {fixed_file}")
    else:
        print("❌ Failed to fix CSV file") 