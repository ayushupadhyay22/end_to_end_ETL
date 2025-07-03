# Warehouse and Retail Sales ETL Pipeline

## Overview
This project implements an end-to-end ETL pipeline for the [Warehouse and Retail Sales dataset](https://catalog.data.gov/dataset/warehouse-and-retail-sales) using Python, Airflow, and PostgreSQL.

---

## Project Structure

- **config/**: Configuration files (YAML)
- **etl/**: ETL modules (`extract.py`, `transform.py`, `load.py`)
- **dags/**: Airflow DAGs for orchestration
- **data/**: (gitignored) Raw and cleaned data files
- **README.md**: Project documentation
- **requirements.txt**: Python dependencies

---

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd end_to_end_ETL
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Apache Airflow**
   Set the Airflow and Python version variables, then install Airflow with the appropriate constraints:
   ```bash
   export AIRFLOW_VERSION=3.0.2
   export PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
   export CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

   pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
   ```

4. **Verify Airflow installation**
   ```bash
   airflow version
   ```
   This should print the installed Airflow version (expected: 3.0.2).

5. **Set the AIRFLOW_HOME environment variable**
   Ensure the `AIRFLOW_HOME` environment variable is set to an absolute path. For example:
   ```bash
   export AIRFLOW_HOME=~/airflow
   ```

6. **Install other dependencies**
   ```bash
   pip install -r requirements.txt
   ```

7. **Configure your settings**
   - Edit `config/config.yaml` as needed (see below for details).

8. **Set up PostgreSQL locally**
   - See "Setting up PostgreSQL" below for instructions on installing and configuring PostgreSQL and creating a database.
     ```

9. **Start Airflow services**
   ```bash
   airflow standalone
   ```
   - Access the Airflow UI at [http://localhost:8080](http://localhost:8080).
   - **Note:** If you are running Airflow for the first time and have not created a username and password, the terminal will provide them during the first run of `airflow standalone`.

---

## Running the Pipeline

You can run the ETL pipeline using Apache Airflow in two ways:

### 1. Using the Airflow Web UI

1. Open your browser and go to [http://localhost:8080](http://localhost:8080).
2. Log in with the credentials you set up (default: admin/admin).
3. Find the DAG named **`warehouse_sales_etl`** in the list.
4. Toggle the switch to "On" if it's not already enabled.
5. Click the "Play" (Trigger DAG) button to run the pipeline immediately.
6. Monitor the progress and logs from the UI.

### 2. Using the Airflow CLI

You can also trigger the pipeline directly from the command line:

```bash
airflow dags trigger warehouse_sales_etl
```

- To check the status of the run:
  ```bash
  airflow dags list-runs -d warehouse_sales_etl
  ```
- To view logs for a specific run, use the Airflow UI or:
  ```bash
  airflow tasks logs run_etl <dag_run_id>
  ```
  Replace `<dag_run_id>` with the actual run ID from the previous command.

---

## Configuration

Edit `config/config.yaml` to match your environment. Example:

```yaml
data_url: "https://data.montgomerycountymd.gov/api/views/v76h-r7br/rows.csv?accessType=DOWNLOAD"
raw_data_path: "/absolute/path/to/data/warehouse_and_retail_sales.csv"
clean_data_path: "/absolute/path/to/data/warehouse_and_retail_sales_cleaned.csv"
postgres:
  user: "" #Add username
  password: ""         # Add your password if needed
  host: "localhost"
  port: 5432
  dbname: "" #database name of your postgres
  table: "" #table name 
```

**Field explanations:**
- `data_url`: Source URL for the dataset.
- `raw_data_path`: Where to save the downloaded raw CSV.
- `clean_data_path`: Where to save the cleaned CSV.
- `postgres`: Connection details for your local PostgreSQL instance.

---

## ETL Flow

- **Extract**: Downloads the dataset from the provided URL.
- **Transform**: Cleans and processes the raw data.
- **Load**: Loads the cleaned data into a PostgreSQL table.

Each step is implemented in the `etl/` directory as a separate Python module.

---

## Setting up PostgreSQL

1. **Install PostgreSQL** (if not already installed)
   - [Download pgAdmin](https://www.pgadmin.org/download/) for a GUI.

2. **Create a new server in pgAdmin**
   - Open pgAdmin.
   - Right-click "Servers" → Create → Server...
   - **General Tab**: Name your server (e.g., "Local Postgres").
   - **Connection Tab**:  
     - Host: `localhost`  
     - Port: `5432`  
     - Username: your local username  
     - Password: (leave blank if not set, or enter your password)

3. **Create a new database**
   - In pgAdmin, expand:  
     `Servers > Local Postgres > Databases`
   - Right-click "Databases" → Create → Database...
   - Enter a name (e.g., `your_db`) and owner (your username).
   - Click Save.

4. **Update `config/config.yaml`** with your database details.

---

## Troubleshooting

- **Airflow not found**: Make sure your virtual environment is activated.
- **Database connection errors**: Double-check your `config.yaml` and that PostgreSQL is running.
- **Permission denied**: Ensure your user has the right permissions in PostgreSQL.

---