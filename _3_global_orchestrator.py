# global_orchestrator.py
# ----------------------
# Runs all ETL segments: pricing, financials, fundamentals
#
# Author: Nicholas Papadimitris
# Created: July 2025
# GitHub: https://github.com/NPStraight2ThePoint/yahooquery-etl-postgresql-prod
#
# Use this script to automate the full ETL pipeline run.

import os
import sys

# Add project root to sys.path so you can import all ETL folder orchestrators
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # assuming this script is at /etl/
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# Now import the ETL orchestrators
from etl._1_pricing.pricing_orchestrator import main as run_pricing_etl
from etl._2_financial_statements.financial_statements_orchestrator import main as run_financials_etl
from etl._3_fundamentals.fundamentals_orchestrator import main as run_fundamentals_etl

def run_step(func, name):
    print(f"\n🚀 Running: {name}")
    try:
        func()
        print(f"✅ Done: {name}")
    except Exception as e:
        print(f"❌ Failed: {name} → {e}")

def main():
    print("🔁 Starting GLOBAL ETL Orchestration")

    run_step(run_pricing_etl, "Pricing ETL")
    run_step(run_financials_etl, "Financial Statements ETL")
    run_step(run_fundamentals_etl, "Fundamentals ETL")

    print("\n🏁 GLOBAL ETL Orchestration Complete")

if __name__ == '__main__':
    main()
