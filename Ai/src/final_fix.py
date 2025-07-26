import csv
import pandas as pd

def final_csv_fix():
    """Final robust CSV fixing that handles all edge cases"""
    input_file = "../data/simfluence_reddit_training.csv"
    output_file = "../data/simfluence_reddit_training_final.csv"
    
    print("🔧 Final CSV fix with robust parsing...")
    
    # Read the original file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split into lines
    lines = content.split('\n')
    print(f"Original file has {len(lines)} lines")
    
    # Process each line
    cleaned_lines = []
    skipped_lines = 0
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue
            
        # Skip problematic lines that start with certain patterns
        if line.strip().startswith("Here are 20 dummy data entries"):
            print(f"Skipping problematic line {i+1}: {line.strip()[:50]}...")
            skipped_lines += 1
            continue
        
        # Count commas
        comma_count = line.count(',')
        
        if comma_count == 18:  # Correct number
            cleaned_lines.append(line)
        elif comma_count > 18:  # Too many commas
            # Split and rejoin
            parts = line.split(',')
            if len(parts) > 19:
                # Join extra parts into suggestions
                suggestions = ','.join(parts[18:])
                new_line = ','.join(parts[:18]) + ',' + suggestions
                cleaned_lines.append(new_line)
            else:
                # Skip this line
                print(f"Skipping malformed line {i+1}")
                skipped_lines += 1
        else:  # Too few commas
            print(f"Skipping line {i+1} with {comma_count} commas")
            skipped_lines += 1
    
    print(f"Cleaned {len(cleaned_lines)} lines")
    print(f"Skipped {skipped_lines} problematic lines")
    
    # Write the cleaned data
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        file.write('\n'.join(cleaned_lines))
    
    print(f"Final cleaned file saved: {output_file}")
    
    # Test the cleaned file
    try:
        df = pd.read_csv(output_file)
        print(f"✅ Final file loads successfully: {df.shape}")
        
        # Show sample data
        print(f"\nSample data:")
        print(df.head(3)[['postText', 'receivedLikes', 'receivedComments', 'receivedShares']])
        
        return output_file
    except Exception as e:
        print(f"❌ Error loading final file: {e}")
        return None

if __name__ == "__main__":
    fixed_file = final_csv_fix()
    if fixed_file:
        print(f"✅ CSV file fixed successfully!")
    else:
        print("❌ Failed to fix CSV file") 