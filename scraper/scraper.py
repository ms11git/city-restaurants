from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

# Set up Chrome for Testing (replace with your actual path)
chrome_path = "/Applications/Google Chrome for Testing.app/Contents/MacOS/chrome"
chrome_options = Options()
chrome_options.binary_location = chrome_path

# Initialize Chrome WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the restaurant inspection website
url = 'https://inspections.myhealthdepartment.com/san-francisco'
try:
    driver.get(url)
    print("Website loaded successfully.")
except Exception as e:
    print(f"Error loading website: {e}")

# Load existing data if the CSV exists and find the latest inspection date
file_path = 'san_francisco_health_inspections.csv'
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
    # Convert the 'Inspection Date' to datetime for comparison
    existing_df['Inspection Date'] = pd.to_datetime(existing_df['Inspection Date'], errors='coerce')
    # Get the most recent inspection date from the existing data
    latest_existing_date = existing_df['Inspection Date'].max()
    print(f"Latest existing inspection date: {latest_existing_date}")
else:
    existing_df = pd.DataFrame()
    latest_existing_date = None  # No data exists yet, so no latest date

# Initialize an empty list to hold the scraped data
data = []

def load_and_process_businesses():
    """Scrapes the currently loaded businesses and returns whether more businesses need to be loaded."""
    # Wait for the business rows to be present
    try:
        business_rows = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.flex-row'))
        )
        print(f"Found {len(business_rows)} businesses.")
    except Exception as e:
        print("Error finding business rows. Printing page source for debugging:")
        print(driver.page_source)
        print(f"Error: {e}")
        driver.quit()
        raise  # Stop execution if we can't find business rows

    # Process each business row
    for index, row in enumerate(business_rows):
        try:
            # Extract the business name
            business_name = row.find_element(By.CSS_SELECTOR, 'h4.establishment-list-name').text
            print(f"Business {index + 1} Name: {business_name}")
        except Exception as e:
            print(f"Error extracting business name: {e}")
            business_name = "N/A"  # Default value

        try:
            # Extract the business address
            business_address = row.find_element(By.CSS_SELECTOR, 'div.establishment-list-address').text
            print(f"Business {index + 1} Address: {business_address}")
        except Exception as e:
            print(f"Error extracting business address: {e}")
            business_address = "N/A"  # Default value

        try:
            # Click the "View Inspection" button
            view_inspection_button = row.find_element(By.XPATH, ".//following-sibling::div[contains(@class, 'establishment-list-button-column')]//a[contains(text(), 'View Inspection')]")
            view_inspection_button.click()
            time.sleep(5)  # Allow time for the inspection details page to load
            print(f"Clicked 'View Inspection' for {business_name}.")
        except Exception as e:
            print(f"Error clicking 'View Inspection' button: {e}")
            continue  # Skip to the next business if the button can't be clicked

        try:
            # Use BeautifulSoup to parse the inspection details
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract Purpose
            try:
                purpose_div = soup.find('p', text='Purpose').find_next('p')
                purpose = purpose_div.text.strip()
                print(f"Purpose: {purpose}")
            except Exception as e:
                print(f"Error extracting purpose: {e}")
                purpose = "N/A"  # Default value

            # Extract Inspection Date
            try:
                inspection_date_div = soup.find('p', text='Inspection Date').find_next('p')
                inspection_date = inspection_date_div.text.strip()
                print(f"Inspection Date: {inspection_date}")
            except Exception as e:
                print(f"Error extracting inspection date: {e}")
                inspection_date = "N/A"  # Default value

            # Skip entries that are older than the latest existing inspection date
            if latest_existing_date and pd.to_datetime(inspection_date) <= latest_existing_date:
                print(f"Skipping {business_name} as it has an older inspection date: {inspection_date}")
                driver.back()
                continue

            # Extract Facility Rating Status
            try:
                rating_status_div = soup.find('p', text='Facility Rating Status').find_next('p')
                rating_status = rating_status_div.text.strip()
                print(f"Facility Rating Status: {rating_status}")
            except Exception as e:
                print(f"Error extracting facility rating status: {e}")
                rating_status = "N/A"  # Default value

            # Append the data for this business to the list
            data.append({
                'Business Name': business_name,
                'Address': business_address,
                'Purpose': purpose,
                'Inspection Date': inspection_date,
                'Facility Rating Status': rating_status
            })
            print(f"Data for {business_name} collected.")

        except Exception as e:
            print(f"Error collecting data for {business_name}: {e}")

        try:
            # Go back to the main page
            driver.back()
            time.sleep(5)  # Allow time for the main page to reload
            print(f"Returned to main page after scraping {business_name}.")
        except Exception as e:
            print(f"Error going back to the main page: {e}")

    # Check if there's a "Load More" button and click it if it's present
    try:
        load_more_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.load-more-results-button'))
        )
        load_more_button.click()
        print("Clicked 'Load More Results' button.")
        time.sleep(5)  # Wait for the new businesses to load
        return True  # More businesses need to be loaded
    except Exception as e:
        print("No 'Load More Results' button found or unable to click it. Assuming all results loaded.")
        return False  # No more businesses to load

# Keep loading and processing until no more results are available
while load_and_process_businesses():
    pass

# Close the browser after scraping is done
try:
    driver.quit()
    print("Browser closed successfully.")
except Exception as e:
    print(f"Error closing browser: {e}")
