import os
import sys

# Ensure the root path is included
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ✅ Use package-style imports
from etl._2_financial_statements import (
    _1_financial_statements,
    merge_financial_statements,
    load_financial_statements
)

def run_step(func, name):
    print(f"\n🚀 Running: {name}")
    try:
        func()
        print(f"✅ Done: {name}")
    except Exception as e:
        print(f"❌ Failed: {name} → {e}")

def main():
    print("🔁 Starting FINANCIAL STATEMENTS ETL")

    run_step(_1_financial_statements.main, '1_financial_statements.py')
    run_step(merge_financial_statements.main, 'merge_financial_statements.py')
    run_step(load_financial_statements.main, 'load_financial_statements.py')

    print("\n🏁 FINANCIAL STATEMENTS ETL Complete")

if __name__ == '__main__':
    main()
