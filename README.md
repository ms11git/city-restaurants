# SF Restaurants Data Pipeline

This project is designed to scrape SF Department of Health Inspections data for businesses, use API For **Google Places** ratings, and API for datasf.org's registered business statuses/dates and load the data into **Google BigQuery** for further analysis and visualization. The project uses Python, Airflow for orchestration, and dbt for data transformations. 

The project will eventually leverage **Google Cloud Storage (GCS)** for cloud-based storage, but currently, data is directly written into BigQuery.

## Project Structure

```
project-name/
├── analysis/                          # Analysis files here
│   └── health_ratings_eda.ipynb         # EDA of health ratings data  
├── dags/                              # Airflow DAGs for orchestrating tasks
│   └── data_pipeline_dag.py             # Airflow DAG to manage scraping and BigQuery loading
├── scraper/                           # Directory for scraping and data-fetching scripts
│   └── api_fetch_business.py            # Main script for scraping health inspection data
    └── api_fetch_ratings.py             # Main script for api ratings from Google Places
    └── scraper.py                       # Main script for scraping health inspection data
├── dbt/                               # Directory for dbt project (data transformations)
│   ├── models/
│   │   └── staging/
│   │   └── marts/
│   ├── dbt_project.yml                  # dbt project configuration
│   └── profiles.yml                     # dbt connection profile for BigQuery
├── requirements.txt                   # Project dependencies
└── README.md                          # This README file
```
## Features
Web Scraping: Scrapes health inspection data from a target website.
BigQuery Integration: Data is uploaded directly to Google BigQuery for storage and analysis.
Airflow Orchestration: Automates the daily scraping and BigQuery upload process.
dbt Transformations: Data is cleaned and transformed into analysis-ready tables using dbt.

## Technologies
Python: For the web scraper and data processing.
Google BigQuery: Data warehouse for storing scraped data.
Airflow: Task scheduler and orchestrator for scraping and loading data into BigQuery.
dbt (Data Build Tool): For transforming raw data into analysis-ready formats.
Google Cloud Storage (Future): Will be used for cloud-based storage of raw data files.

## Current Workflow
Scraping: The Python script (scraper.py) scrapes health inspection data (e.g., business names, addresses, inspection details) from a website.
Direct Write to BigQuery: The scraped data is directly written into BigQuery tables.
Airflow DAG: Airflow is used to schedule the scraping process on a daily basis and handle the data loading pipeline.
Data Transformation with dbt: dbt is used to clean and transform the data within BigQuery.
### BigQuery Table: health_inspections
business_name (STRING): The name of the business.
address (STRING): The business address.
inspection_date (DATE): The date of the inspection.
facility_rating_status (STRING): The rating/status of the inspection.
purpose (STRING): The purpose of the inspection (e.g., routine, follow-up).
## Getting Started

### Prerequisites
Google Cloud Account: Set up Google Cloud and create a BigQuery project.
Python 3.x: Install Python and set up a virtual environment.
BigQuery Client Library: Install the Google Cloud BigQuery Python library.
Airflow: Install Airflow for orchestration.

### Installation
1. Clone the repository:
```
git clone https://github.com/yourusername/city-restaurants.git
cd city-restaurants
```
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
Create a Service Account on Google Cloud and download the service account key (JSON).
Set the environment variable:
```
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-file.json"
```
4. Configure BigQuery:
Ensure your BigQuery dataset is created (e.g., location_health_analysis).
Create the health_inspections table using this schema:
```
CREATE TABLE `your-project-id.location_health_analysis.health_inspections` (
  business_name STRING,
  address STRING,
  inspection_date DATE,
  facility_rating_status STRING,
  purpose STRING
);
```

5. Set up Airflow:
Install Airflow and configure your DAG in dags/data_pipeline_dag.py.
Start the Airflow scheduler:
```
airflow scheduler
```
Start the Airflow webserver to view your DAG:
```
airflow webserver
```

6. Run the dbt models:
```
dbt run
```

## Future Plans
Google Cloud Storage (GCS) Integration: In the future, data will be stored in Google Cloud Storage as CSV files before loading into BigQuery.
Dashboarding: The transformed data will be visualized using a tool like Tableau or Google Data Studio.

## License
This project is licensed under the MIT License.
