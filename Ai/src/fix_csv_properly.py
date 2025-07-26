import csv
import pandas as pd

def fix_csv_properly():
    """Fix the CSV file properly by handling all parsing issues"""
    input_file = "../data/simfluence_reddit_training.csv"
    output_file = "../data/simfluence_reddit_training_clean.csv"
    
    print("🔧 Fixing CSV file properly...")
    
    # Read the original file line by line
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    print(f"Original file has {len(lines)} lines")
    
    # Process each line
    cleaned_lines = []
    problematic_lines = []
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue
            
        # Count commas in the line
        comma_count = line.count(',')
        
        if comma_count == 18:  # Correct number of commas (19 fields)
            cleaned_lines.append(line)
        elif comma_count > 18:  # Too many commas
            # Split by comma and rejoin the extra fields in the suggestions column
            parts = line.split(',')
            if len(parts) > 19:
                # Join the extra parts into the suggestions field
                suggestions = ','.join(parts[18:])
                new_line = ','.join(parts[:18]) + ',' + suggestions
                cleaned_lines.append(new_line)
                print(f"Fixed line {i+1}: {len(parts)} fields -> 19 fields")
            else:
                problematic_lines.append((i+1, line))
        else:  # Too few commas
            problematic_lines.append((i+1, line))
    
    print(f"Cleaned {len(cleaned_lines)} lines")
    print(f"Problematic lines: {len(problematic_lines)}")
    
    if problematic_lines:
        print("Problematic lines:")
        for line_num, line in problematic_lines[:5]:  # Show first 5
            print(f"  Line {line_num}: {line.strip()}")
    
    # Write the cleaned data
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        file.writelines(cleaned_lines)
    
    print(f"Cleaned file saved: {output_file}")
    
    # Test the cleaned file
    try:
        df = pd.read_csv(output_file)
        print(f"✅ Cleaned file loads successfully: {df.shape}")
        return output_file
    except Exception as e:
        print(f"❌ Error loading cleaned file: {e}")
        return None

if __name__ == "__main__":
    fixed_file = fix_csv_properly()
    if fixed_file:
        print(f"✅ CSV file fixed successfully!")
    else:
        print("❌ Failed to fix CSV file") 