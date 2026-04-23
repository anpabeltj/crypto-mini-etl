# 🪙 Crypto ETL Pipeline

An automated ETL pipeline that fetches live cryptocurrency market data, transforms it, and stores it in a PostgreSQL database, all orchestrated by Apache Airflow and visualized through Metabase.

---

## 🏗️ Architecture Overview

```
CoinGecko API
     ↓
  📥 Extract
     ↓
  🔄 Transform
     ↓
  📤 Load → PostgreSQL (crypto_db)
     ↓
  📊 Metabase Dashboard
```

The entire pipeline runs inside Docker and is scheduled to execute **daily** via Airflow.

---

## 🔁 ETL Workflow

### 1. 📥 Extract (`scripts/extract.py`)

Calls the **CoinGecko public API** and fetches the top 10 cryptocurrencies by market cap in USD.

Fields retrieved per coin:

- `id`, `name`, `current_price`, `market_cap`, `market_cap_rank`
- `total_volume`, `high_24h`, `low_24h`, `price_change_percentage_24h`, `last_updated`

### 2. 🔄 Transform (`scripts/transform.py`)

Uses **pandas** to clean and reshape the raw JSON response:

- Selects and renames relevant columns with descriptive `_usd` suffixes
- Parses `last_updated` into a proper date field
- Rounds `price_change_percentage_24h` to 2 decimal places

### 3. 📤 Load (`scripts/load.py`)

Connects to the **PostgreSQL** (`crypto_db`) database via SQLAlchemy and writes the transformed DataFrame into a table called `crypto_data`, replacing existing data on each run.

Credentials are loaded from the `.env` file using `python-dotenv`.

---

## ⚙️ Airflow DAG (`dags/crypto_dag.py`)

**DAG ID:** `crypto_etl_pipeline`
**Schedule:** `@daily`
**Retries:** 1

Task flow:

```
extract_crypto → transform_crypto → load_crypto
```

Data is passed between tasks using Airflow **XCom**.

---

## 🐳 Services (`docker-compose.yml`)

| Service            | Image                | Port     | Purpose                   |
| ------------------ | -------------------- | -------- | ------------------------- |
| `postgres-airflow` | postgres:15          | internal | Airflow metadata database |
| `postgres-crypto`  | postgres:15          | 5434     | Stores crypto ETL output  |
| `airflow`          | apache/airflow:2.8.1 | 8080     | Scheduler + Webserver     |
| `metabase`         | metabase/metabase    | 3000     | Data visualization        |

---

## 🚀 Getting Started

### Prerequisites

- 🐳 Docker and Docker Compose installed

### Setup

**1.** Clone the repository and navigate into it.

**2.** Copy the environment file and fill in your database credentials:

```bash
cp .env.example .env
```

```env
DB_USER=crypto_user
DB_PASS=crypto_pass
DB_HOST=postgres-crypto
DB_PORT=5432
DB_NAME=crypto_db
```

**3.** Start all services:

```bash
docker compose up -d
```

**4.** Access the Airflow UI at [http://localhost:8080](http://localhost:8080)

- Username: `admin`
- Password: `admin`

**5.** Enable and trigger the `crypto_etl_pipeline` DAG.

**6.** Access Metabase at [http://localhost:3000](http://localhost:3000) to explore the loaded data.

---

## 📁 Project Structure

```
crypto-etl/
├── dags/
│   └── crypto_dag.py       # Airflow DAG definition
├── scripts/
│   ├── extract.py          # Fetches data from CoinGecko API
│   ├── transform.py        # Cleans and reshapes data with pandas
│   └── load.py             # Loads data into PostgreSQL
├── logs/                   # Airflow task logs (auto-generated)
├── docker-compose.yml      # Multi-service Docker setup
├── .env.example            # Environment variable template
└── README.md
```

---

## 🛠️ Tech Stack

| Tool              | Role                      |
| ----------------- | ------------------------- |
| 🐍 Python         | ETL scripting             |
| 🌬️ Apache Airflow | Workflow orchestration    |
| 🐘 PostgreSQL     | Data storage              |
| 🐼 pandas         | Data transformation       |
| 🐳 Docker         | Containerization          |
| 📊 Metabase       | Data visualization        |
| 🦎 CoinGecko API  | Crypto market data source |
