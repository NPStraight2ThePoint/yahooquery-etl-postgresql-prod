# 📊 Yahoo Finance ETL to PostgreSQL

**Automated, scalable, and modular ETL pipeline** using [`yahooquery`](https://github.com/dpguthrie/yahooquery) to extract pricing, financial statements, and fundamental data — all stored in a **PostgreSQL database** for easy querying and analysis.

---

## 🚀 Features

- ✅ Clean, plug-and-play ETL pipeline (3 segments: Pricing, Financials, Fundamentals)
- 📥 Automatically scrapes S&P 500 tickers (or lets you configure your own universe)
- 🧱 Creates and manages PostgreSQL database schema + tables
- 🗃️ Organized output directories, archiving logic and file handling
- ⚙️ Fully modular: update or extend segments easily
- 🔒 Secure `.env` config (example provided)

---

## 📁 Folder Structure

```text
yahooquery-etl-postgresql-prod/
├── archive/                     # Archived CSVs for version tracking
│   └── data/
├── archive_dir.py              # Archive logic
├── etl/                        # ETL scripts for each data segment
│   ├── _1_pricing/
│   ├── _2_financial_statements/
│   └── _3_fundamentals/                   
├── get_sp500_tickers.py        # Auto-download S&P 500 tickers
├── global_orchestrator.py      # Runs all segments in order
├── output/                     # Fetched raw data
│   ├── _1_pricing/
│   ├── _2_financials/
│   ├── _3_fundamentals/
│   └── merged                  # Merged outputs
├── requirements.txt
├── setup/                      # DB creation, schema, folder setup
│   ├── create_db.py
│   ├── init_schema_tables.py
│   └── create_dirs.py
├── sql_db_schema/              # CSV schema definition files
│   └── sql_schema.csv
├── utils/                      # Helper functions + shared paths
├── .env.example                # Template for local credentials
├── .gitignore                  # Excludes sensitive files
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Requirements

- Python 3.9+
- PostgreSQL (download [here](https://www.postgresql.org/download/))
- Libraries: see `requirements.txt`

### 2️⃣ Clone the Repo

```bash
git clone https://github.com/NPStraight2ThePoint/yahooquery-etl-postgresql-prod.git
cd yahooquery-etl-postgresql-prod
```

### 3️⃣ Set Up Environment

Create your .env file using the provided template:
```bash
cp .env.example .env
```
Edit .env with your local PostgreSQL credentials:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=yahooquery_db
```

### 🧱 Initial Setup (One-time)

```bash
python setup/create_db.py
python setup/init_schema_tables.py
python setup/create_dirs.py
```

### 📈 Run the ETL Pipeline

You can either:

1. Use the Global Orchestrator (recommended):
```bash
python global_orchestrator.py
```

Or:

2. Run each module manually (pricing, financials, fundamentals):

```bash
python etl/_1_pricing/pricing_orchestrator.py
python etl/_2_financial_statements/financials_statements_orchestrator.py
python etl/_3_fundamentals/fundamentals_orchestrator.py
```

📦 Archive Old Data (Optional)
After a run, clean up and archive raw data:

```bash
python archive_dir.py
```

📊 What's Included
```bash
📁 Historical pricing
📁 Option chains
📁 Technical insights
📁 Financial statements (IS, BS, CF) / (Annual/Quarterly)
📁 Company fundamentals
📁 Static profiles, summaries, and more
```

### 🛠️ Custom Universes

Want to analyze a different set of tickers beyond the S&P 500?

You have two options:

- 🔁 **Replace the default** `Tickers.csv` located in:  
  `output/Static Data/Tickers.csv`

- 🧩 **Customize the scraping logic** in:  
  `get_sp500_tickers.py` — adapt it for your own universe (ASX200, ETFs, custom watchlists, etc.)

---

### 🧪 Project Status & Roadmap

✅ Tested on 10–500 tickers  
📌 **Upcoming Enhancements**:
- Add automated testing
- GitHub Actions for CI/CD
- Additional Yahoo data modules

---

### 🆔 Project Info

**Author:** *Nicholas Papadimitris*  
**Created On:** *09 July 2025, 06:00 AM UTC*  
**Project ID:** `YF_YQ_ETL_09_Jul2025`

- 🐙 **GitHub:** [@NPStraight2ThePoint](https://github.com/NPStraight2ThePoint)  
- 💼 **LinkedIn:** [Nicholas Papadimitris](https://www.linkedin.com/in/nicholas-papadimitris/)  
- 📧 **Email:** nicholas.papadimitris@gmail.com  

---

### 📄 License
MIT License — free to use and modify.

### 🙏 Attribution Requirement
If you distribute or share this repository or its contents publicly, you must:

✅ Provide appropriate credit

✅ Include a link to the original repository:
https://github.com/NPStraight2ThePoint/yahooquery-etl-postgresql-prod

✅ Indicate if changes were made

You may do so in any reasonable manner, but not in any way that suggests the original author or this repository endorses you or your use.







