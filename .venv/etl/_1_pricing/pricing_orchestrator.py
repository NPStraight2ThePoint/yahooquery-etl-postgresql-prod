import os
import sys

# Add project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from etl._1_pricing import _1_history, _2_option_chain, _3_technical_insights, merge_pricing, load_pricing

def run_step(func, name):
    print(f"\n🚀 Running: {name}")
    try:
        func()
        print(f"✅ Done: {name}")
    except Exception as e:
        print(f"❌ Failed: {name} → {e}")

def main():
    print("🔁 Starting PRICING ETL")

    run_step(_1_history.main, '1_history.py')
    run_step(_2_option_chain.main, '2_option_chain.py')
    run_step(_3_technical_insights.main, '3_technical_insights.py')
    run_step(merge_pricing.main, 'merge_pricing.py')
    run_step(load_pricing.main, 'load_pricing.py')

    print("\n🏁 PRICING ETL Complete")

if __name__ == '__main__':
    main()
