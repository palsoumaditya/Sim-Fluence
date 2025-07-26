import os
import pandas as pd

def quick_check():
    """Quick check of the dataset and training process"""
    print("🔍 QUICK DATASET CHECK")
    print("=" * 40)
    
    csv_path = "../data/simfluence_reddit_training_fixed.csv"
    
    # Check file size
    file_size = os.path.getsize(csv_path)
    print(f"File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    # Count lines
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"Total lines: {len(lines):,}")
    print(f"Data rows (excluding header): {len(lines)-1:,}")
    
    # Try to read with pandas
    try:
        df = pd.read_csv(csv_path)
        print(f"Pandas DataFrame shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # Check sample data
        print(f"\nSample data (first 3 rows):")
        print(df.head(3)[['postText', 'receivedLikes', 'receivedComments', 'receivedShares']])
        
        # Check data types
        print(f"\nData types:")
        print(df.dtypes)
        
        # Check for missing values
        missing = df.isnull().sum()
        print(f"\nMissing values:")
        print(missing[missing > 0])
        
        print(f"\n✅ Dataset loaded successfully!")
        print(f"   You have {len(df):,} samples to train on")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

if __name__ == "__main__":
    quick_check() 