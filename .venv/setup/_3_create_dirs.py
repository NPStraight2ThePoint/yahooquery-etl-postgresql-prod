from pathlib import Path
from utils import ROOT_DIR

# Define ROOT_DIR — adjust if this script is inside a subfolder, else use `.parent`
ROOT_DIR = Path(__file__).parent.parent  # example: two levels up to repo root

REQUIRED_DIRS = [
    ROOT_DIR / "output",
    ROOT_DIR / "output" / "_1_pricing" / "history",
    ROOT_DIR / "output" / "_1_pricing" / "option_chain",
    ROOT_DIR / "output" / "_1_pricing" / "technical_insights",
    ROOT_DIR / "output" / "_2_financial_statements",
    ROOT_DIR / "output" / "_2_financial_statements" / "Balance Sheet" / "Annual",
    ROOT_DIR / "output" / "_2_financial_statements" / "Balance Sheet" / "Quarterly",
    ROOT_DIR / "output" / "_2_financial_statements" / "Cash Flow" / "Annual",
    ROOT_DIR / "output" / "_2_financial_statements" / "Cash Flow" / "Quarterly",
    ROOT_DIR / "output" / "_2_financial_statements" / "Income Statement" / "Annual",
    ROOT_DIR / "output" / "_2_financial_statements" / "Income Statement" / "Quarterly",
    ROOT_DIR / "output" / "_3_fundamentals",
    ROOT_DIR / "output" / "_3_fundamentals" / "Batches",
    ROOT_DIR / "output" / "Static Data",
    ROOT_DIR / "Archive",
    ROOT_DIR / "Archive" / "data",
]

def create_dirs():
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

if __name__ == "__main__":
    create_dirs()
