from google.cloud import storage
from google.cloud import bigquery
import requests
from bs4 import BeautifulSoup

# Create GCS client
storage_client = storage.Client()

# Create BigQuery client
bq_client = bigquery.Client()

# Create datasets and tables in BQ
reg_dataset = bq_client.create_dataset('ecommerce_regs') 
regs_table = reg_dataset.table('regulations')
reqs_table = reg_dataset.table('requirements')

# Define schemas for BQ tables
reg_schema = [
  bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),
  bigquery.SchemaField('name', 'STRING', mode='REQUIRED'),
  bigquery.SchemaField('category', 'STRING', mode='REQUIRED'),
  bigquery.SchemaField('issuing_authority', 'STRING', mode='NULLABLE'),
  bigquery.SchemaField('issuing_date', 'DATE', mode='NULLABLE'),
  bigquery.SchemaField('link', 'STRING', mode='REQUIRED')
]

req_schema = [
  bigquery.SchemaField('id', 'INTEGER', mode='REQUIRED'),  
  bigquery.SchemaField('regulation_id', 'INTEGER', mode='REQUIRED'),
  bigquery.SchemaField('requirement', 'STRING', mode='REQUIRED')  
]

regs_table.schema = reg_schema
reqs_table.schema = req_schema

# The code to scrape sites

# Function to scrape site and extract regulation data
def get_regs(site):

  page = requests.get(site)
  soup = BeautifulSoup(page.content, 'html.parser')
  
  regulations = []
  
  for reg in soup.find_all('div', class_='regulation'):
  
    name = reg.h2.text
    category = reg.find('span', class_='category').text
    
    
    link = reg.a['href']
    
    reg_data = {
      'name': name,
      'category': category,
      'link': link
    }
    
    regulations.append(reg_data)

  return regulations

# To write rows to BQ
errors = bq_client.insert_rows(regs_table, regulation_rows) 
errors = bq_client.insert_rows(reqs_table, requirements_rows)

# Can also batch write to GCS and load into BQ
bucket = storage_client.bucket('my-bucket')
blobs = bucket.list_blobs(prefix='ecommerce-regs/') 

for blob in blobs:
  data = blob.download_as_string()
  blob.upload_from_string(data, content_type='text/csv')

# Then load CSVs from GCS into BQ  
job = bq_client.load_table_from_uri(
  'gs://my-bucket/ecommerce-regs/*.csv',
  reg_dataset.table('regulations')
)