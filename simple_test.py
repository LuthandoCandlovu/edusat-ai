"""
Simple test to verify data loading
"""
import pandas as pd
import sys

print("🚀 EduSat AI - Simple Test")
print("="*50)

try:
    # Try to load the data
    df = pd.read_excel("data/Eastern_Cape_Education_Factors_Dataset.xlsx", sheet_name="data")
    print(f"✅ Success! Loaded {len(df)} learners")
    print(f"📊 Columns: {list(df.columns)}")
    print("\n📈 First 3 rows:")
    print(df.head(3))
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

input("\nPress Enter to exit...")
