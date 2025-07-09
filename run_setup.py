# run_setup.py
# ----------------------
# Creates DB,Schemas,Tables,Folders
#
# Author: Nicholas Papadimitris
# Created: July 2025
# GitHub: https://github.com/NPStraight2ThePoint/yahooquery-etl-postgresql-prod

import os
import sys

# Add project root to sys.path so you can import all ETL folder orchestrators
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # assuming this script is at /etl/
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from setup._1_create_db.py import main as run_create_db
from setup._2_init_schema_tables.py import main as run_schema_tables
from setup._3_create_dirs import main as run_create_dirs

def run_step(func, name):
    print(f"\n🚀 Running: {name}")
    try:
        func()
        print(f"✅ Done: {name}")
    except Exception as e:
        print(f"❌ Failed: {name} → {e}")

def main():
    print("🔁 Starting Setup")

    run_step(run_create_db, "Creating DB")
    run_step(run_schema_tables, "Creating Schemas/Tables")
    run_step(run_create_dirs, "Creating folders")

    print("\n🏁 Setup Complete")

if __name__ == '__main__':
    main()
