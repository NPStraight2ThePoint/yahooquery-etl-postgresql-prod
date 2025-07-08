import os
import sys

# Add the local directory to sys.path so relative imports work
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import ETL steps
import _1_financial_statements
import merge_financial_statements
import load_financial_statements

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

# Make this callable both as script or from global orchestrator
if __name__ == '__main__':
    main()
