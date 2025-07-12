import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from etl._4_technicals import _1_technical_insights, merge_technicals, load_technicals

def run_step(func, name):
    print(f"\n🚀 Running: {name}")
    try:
        func()
        print(f"✅ Done: {name}")
    except Exception as e:
        print(f"❌ Failed: {name} → {e}")

def main():
    print("🔁 Starting PRICING ETL")
    run_step(_1_technical_insights.main, '1_technical_insights.py')
    run_step(merge_technicals.main, 'merge_technicals.py')
    run_step(load_technicals.main, 'load_technicals.py')

    print("\n🏁 PRICING ETL Complete")

if __name__ == '__main__':
    main()
