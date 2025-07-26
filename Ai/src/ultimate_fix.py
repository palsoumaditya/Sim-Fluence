import csv
import pandas as pd

def ultimate_csv_fix():
    """Ultimate CSV fixing that handles all quote and comma issues"""
    input_file = "../data/simfluence_reddit_training.csv"
    output_file = "../data/simfluence_reddit_training_ultimate.csv"
    
    print("🔧 Ultimate CSV fix with proper CSV parsing...")
    
    # Use proper CSV reader to handle quotes
    cleaned_rows = []
    problematic_lines = 0
    
    with open(input_file, 'r', encoding='utf-8') as file:
        # Use csv.reader with proper quote handling
        reader = csv.reader(file)
        
        for i, row in enumerate(reader):
            if len(row) == 19:  # Correct number of fields
                cleaned_rows.append(row)
            elif len(row) > 19:  # Too many fields
                # Join extra fields into suggestions
                suggestions = ','.join(row[18:])
                new_row = row[:18] + [suggestions]
                cleaned_rows.append(new_row)
                print(f"Fixed line {i+1}: {len(row)} fields -> 19 fields")
            else:  # Too few fields
                problematic_lines += 1
                print(f"Skipping line {i+1}: {len(row)} fields")
    
    print(f"Cleaned {len(cleaned_rows)} rows")
    print(f"Problematic lines: {problematic_lines}")
    
    # Write the cleaned data
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(cleaned_rows)
    
    print(f"Ultimate cleaned file saved: {output_file}")
    
    # Test the cleaned file
    try:
        df = pd.read_csv(output_file)
        print(f"✅ Ultimate file loads successfully: {df.shape}")
        
        # Show sample data
        print(f"\nSample data:")
        print(df.head(3)[['postText', 'receivedLikes', 'receivedComments', 'receivedShares']])
        
        # Check data quality
        print(f"\nData quality check:")
        print(f"Total samples: {len(df):,}")
        print(f"Missing values: {df.isnull().sum().sum()}")
        print(f"Data types: {df.dtypes.tolist()}")
        
        return output_file
    except Exception as e:
        print(f"❌ Error loading ultimate file: {e}")
        return None

if __name__ == "__main__":
    fixed_file = ultimate_csv_fix()
    if fixed_file:
        print(f"✅ CSV file fixed successfully!")
    else:
        print("❌ Failed to fix CSV file") 