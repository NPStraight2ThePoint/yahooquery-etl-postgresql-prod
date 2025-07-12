import os
import sys

# Add project root to sys.path so you can import all ETL folder orchestrators
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # assuming this script is at /etl/
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import os
from pathlib import Path
from datetime import date
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Date Helper
today_str = date.today().isoformat()

# Resolve Root Directory from Marker
def get_repo_root_from_marker(marker_filename="yahooquery_UI_prod_1.txt") -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        marker_path = parent / marker_filename
        if marker_path.exists():
            return parent
    raise FileNotFoundError(f"❌ Could not find '{marker_filename}' in any parent directory.")

ROOT_DIR = get_repo_root_from_marker()
print("📁 ROOT DIR:", ROOT_DIR)

# - Main Directories

MAIN_OUTPUT_DIR = ROOT_DIR / "output"
ARCHIVE_DIR = ROOT_DIR / "Archive/Data"

STATIC_DIR = ROOT_DIR / "output/Static Data"
MERGED_DIR = ROOT_DIR / "output/merged"
MERGED_DIR_CLEAN = (ROOT_DIR / "output/merged").resolve()

# Tickers
TICKERS_CSV = STATIC_DIR / "Tickers.csv"

# Pricing
PRICING_HISTORY_OUTPUT_DIR = ROOT_DIR / "output/_1_pricing/history"
PRICING_OPTION_CHAIN_OUTPUT_DIR = ROOT_DIR / "output/_1_pricing/option_chain"
PRICING_TECHNICAL_INSIGHTS_OUTPUT_DIR = ROOT_DIR / "output/_1_pricing/technical_insights"

# Financial Statements
FINANCIAL_STATEMENTS_DIR = ROOT_DIR / "output/_2_financial_statements"
FINANCIAL_STATEMENTS_OUTPUT_DIRS = {
    'balance_sheet': {
        'annual': FINANCIAL_STATEMENTS_DIR / 'Balance Sheet' / 'Annual',
        'quarterly': FINANCIAL_STATEMENTS_DIR / 'Balance Sheet' / 'Quarterly',
    },
    'income_statement': {
        'annual': FINANCIAL_STATEMENTS_DIR / 'Income Statement' / 'Annual',
        'quarterly': FINANCIAL_STATEMENTS_DIR / 'Income Statement' / 'Quarterly',
    },
    'cash_flow': {
        'annual': FINANCIAL_STATEMENTS_DIR / 'Cash Flow' / 'Annual',
        'quarterly': FINANCIAL_STATEMENTS_DIR / 'Cash Flow' / 'Quarterly',
    }
}

# Fundamentals
FUNDAMENTALS_OUTPUT_DIR = ROOT_DIR / "output" / "_3_fundamentals" / "Batches"
FUNDAMENTALS_FINANCIAL_DATA = MERGED_DIR_CLEAN / 'fin_merged.csv'
FUNDAMENTALS_KEY_STATS = MERGED_DIR_CLEAN / 'keystats_merged.csv'
FUNDAMENTALS_PRICE_DATA = MERGED_DIR_CLEAN / 'price_merged.csv'
FUNDAMENTALS_PROFILE_DATA = MERGED_DIR_CLEAN / 'profile_merged.csv'
FUNDAMENTALS_SUMMARY_DATA = MERGED_DIR_CLEAN / 'summary_merged.csv'
FUNDAMENTALS_VALUATION = MERGED_DIR_CLEAN / 'valuation_merged.csv'
FUNDAMENTALS_OFFICERS = MERGED_DIR_CLEAN / 'officers_merged.csv'

# Table Names
PRICING_HISTORY_TABLE_NAME = 'yahooquery.pricing_history'
OPTION_CHAIN_TABLE_NAME = 'yahooquery.pricing_option_chain'
PRICING_TECHNICAL_INSIGHTS_TABLE_NAME = 'yahooquery.pricing_technical_insights'
PRICING_TECHNICAL_REPORTS_TABLE_NAME = 'yahooquery.pricing_technical_reports'
FUNDAMENTALS_FINANCIAL_DATA_TABLE_NAME = 'yahooquery.fundamentals_financial_data'
FUNDAMENTALS_KEY_STATS_TABLE_NAME = 'yahooquery.fundamentals_key_stats'
FUNDAMENTALS_PRICE_DATA_TABLE_NAME = 'yahooquery.fundamentals_price_data'
FUNDAMENTALS_PROFILE_DATA_TABLE_NAME = 'yahooquery.fundamentals_profile_data'
FUNDAMENTALS_SUMMARY_DATA_TABLE_NAME = 'yahooquery.fundamentals_summary_data'
FUNDAMENTALS_VALUATION_TABLE_NAME = 'yahooquery.fundamentals_valuation_data'
FUNDAMENTALS_OFFICERS_TABLE_NAME = 'yahooquery.fundamentals_officers_data'


# DB Credentials from .env
DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}
conn_params = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'dbname': os.getenv('DB_NAME', 'Yahoo_Finance_API'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', '5432'),
}

# Optional strict validation:
missing_keys = [k for k, v in DB_PARAMS.items() if not v]
if missing_keys:
    print(f"⚠️ Warning: Missing DB keys → {missing_keys}")

# Rename Map for Technical Insights Columns
rename_map = {
    'instrumentinfo_technicalevents_provider': 'instrument_provider',
    'instrumentinfo_technicalevents_sector': 'sector',
    'instrumentinfo_technicalevents_shorttermoutlook_statedescription': 'st_state_desc',
    'instrumentinfo_technicalevents_shorttermoutlook_direction': 'st_direction',
    'instrumentinfo_technicalevents_shorttermoutlook_score': 'st_score',
    'instrumentinfo_technicalevents_shorttermoutlook_scoredescription': 'st_score_desc',
    'instrumentinfo_technicalevents_shorttermoutlook_sectordirection': 'st_sector_direction',
    'instrumentinfo_technicalevents_shorttermoutlook_sectorscore': 'st_sector_score',
    'instrumentinfo_technicalevents_shorttermoutlook_sectorscoredescription': 'st_sector_score_desc',
    'instrumentinfo_technicalevents_shorttermoutlook_indexdirection': 'st_index_direction',
    'instrumentinfo_technicalevents_shorttermoutlook_indexscore': 'st_index_score',
    'instrumentinfo_technicalevents_shorttermoutlook_indexscoredescription': 'st_index_score_desc',
    'instrumentinfo_technicalevents_intermediatetermoutlook_statedescription': 'it_state_desc',
    'instrumentinfo_technicalevents_intermediatetermoutlook_direction': 'it_direction',
    'instrumentinfo_technicalevents_intermediatetermoutlook_score': 'it_score',
    'instrumentinfo_technicalevents_intermediatetermoutlook_scoredescription': 'it_score_desc',
    'instrumentinfo_technicalevents_intermediatetermoutlook_sectordirection': 'it_sector_direction',
    'instrumentinfo_technicalevents_intermediatetermoutlook_sectorscore': 'it_sector_score',
    'instrumentinfo_technicalevents_intermediatetermoutlook_sectorscoredescription': 'it_sector_score_desc',
    'instrumentinfo_technicalevents_intermediatetermoutlook_indexdirection': 'it_index_direction',
    'instrumentinfo_technicalevents_intermediatetermoutlook_indexscore': 'it_index_score',
    'instrumentinfo_technicalevents_intermediatetermoutlook_indexscoredescription': 'it_index_score_desc',
    'instrumentinfo_technicalevents_longtermoutlook_statedescription': 'lt_state_desc',
    'instrumentinfo_technicalevents_longtermoutlook_direction': 'lt_direction',
    'instrumentinfo_technicalevents_longtermoutlook_score': 'lt_score',
    'instrumentinfo_technicalevents_longtermoutlook_scoredescription': 'lt_score_desc',
    'instrumentinfo_technicalevents_longtermoutlook_sectordirection': 'lt_sector_direction',
    'instrumentinfo_technicalevents_longtermoutlook_sectorscore': 'lt_sector_score',
    'instrumentinfo_technicalevents_longtermoutlook_sectorscoredescription': 'lt_sector_score_desc',
    'instrumentinfo_technicalevents_longtermoutlook_indexdirection': 'lt_index_direction',
    'instrumentinfo_technicalevents_longtermoutlook_indexscore': 'lt_index_score',
    'instrumentinfo_technicalevents_longtermoutlook_indexscoredescription': 'lt_index_score_desc',
    'instrumentinfo_keytechnicals_provider': 'keytechnicals_provider',
    'instrumentinfo_keytechnicals_support': 'support',
    'instrumentinfo_keytechnicals_resistance': 'resistance',
    'instrumentinfo_keytechnicals_stoploss': 'stoploss',
    'instrumentinfo_valuation_color': 'valuation_color',
    'instrumentinfo_valuation_description': 'valuation_desc',
    'instrumentinfo_valuation_discount': 'valuation_discount',
    'instrumentinfo_valuation_relativevalue': 'valuation_relative',
    'instrumentinfo_valuation_provider': 'valuation_provider',
    'companysnapshot_sectorinfo': 'company_sector_info',
    'companysnapshot_company_innovativeness': 'comp_innovativeness',
    'companysnapshot_company_hiring': 'comp_hiring',
    'companysnapshot_company_sustainability': 'comp_sustainability',
    'companysnapshot_company_insidersentiments': 'comp_insider_sentiments',
    'companysnapshot_company_earningsreports': 'comp_earnings_reports',
    'companysnapshot_company_dividends': 'comp_dividends',
    'companysnapshot_sector_innovativeness': 'sector_innovativeness',
    'companysnapshot_sector_hiring': 'sector_hiring',
    'companysnapshot_sector_sustainability': 'sector_sustainability',
    'companysnapshot_sector_insidersentiments': 'sector_insider_sentiments',
    'companysnapshot_sector_earningsreports': 'sector_earnings_reports',
    'companysnapshot_sector_dividends': 'sector_dividends',
    'recommendation_targetprice': 'target_price',
    'recommendation_provider': 'recommendation_provider',
    'recommendation_rating': 'recommendation_rating',
    'upsell_msbullishsummary': 'ms_bullish_summary',
    'upsell_msbearishsummary': 'ms_bearish_summary',
    'upsell_companyname': 'company_name',
    'upsell_msbullishbearishsummariespublishdate': 'ms_summary_date',
    'upsell_upsellreporttype': 'upsell_report_type',
    'upsellsearchdd_researchreports_reportid': 'research_report_id',
    'upsellsearchdd_researchreports_provider': 'research_provider',
    'upsellsearchdd_researchreports_title': 'research_title',
    'upsellsearchdd_researchreports_reportdate': 'research_date',
    'upsellsearchdd_researchreports_summary': 'research_summary',
    'upsellsearchdd_researchreports_investmentrating': 'research_rating',
    'events': 'events',
    'sigdevs': 'sig_devs',
    'secreports': 'sec_reports'
}



