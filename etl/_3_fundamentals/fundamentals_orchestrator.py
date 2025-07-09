import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from etl._3_fundamentals import _1_fundamentals, merge_fundamentals, load_fundamentals

def run_step(func, name):
    print(f"\n🚀 Running: {name}")
    try:
        func()
        print(f"✅ Done: {name}")
    except Exception as e:
        print(f"❌ Failed: {name} → {e}")

def main():
    print("🔁 Starting FUNDAMENTALS ETL")

    run_step(_1_fundamentals.main, '1_fundamentals.py')
    run_step(merge_fundamentals.main, 'merge_fundamentals.py')
    run_step(load_fundamentals.main, 'load_fundamentals.py')

    print("\n🏁 FUNDAMENTALS ETL Complete")

if __name__ == '__main__':
    main()
