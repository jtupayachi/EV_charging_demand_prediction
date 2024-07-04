from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from functools import reduce
import time
from selenium.webdriver.support.ui import WebDriverWait, Select

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# venv-metal
# (base) ➜  ~ xattr -d com.apple.quarantine chromedriver
# (base) ➜  ~ spctl --add --label 'Approved' chromedriver

"""_summary_: Main Data Scrapper
"""

def render_page(url,d,postal_code,city):
    string_d=d.split(" ")
    print(string_d)
    year=str(string_d[0])
    
    day=str(string_d[2])
    if day[0] == '0':
        day = str(day[1:])
    
        
        
    
    
    month=str(string_d[1])
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service('/Users/user/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    time.sleep(3)
    try:
        # Check if the button is within an iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                accept_button = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@title='Accept all' and @aria-label='Accept all']"))
                )
                break
            except:
                driver.switch_to.default_content()

        # Locate and click the "Accept all" button
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='Accept all' and @aria-label='Accept all']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", accept_button)
        accept_button.click()
        time.sleep(3)  # Wait for any potential page load or changes after the click
        
        # Switch back to the main content if in an iframe
        driver.switch_to.default_content()
        
        # Locate and click the "History" element
        history_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'History') and contains(@class, 'ng-star-inserted')]"))
        )
        history_element.click()
        time.sleep(3)  # Wait for any potential page load or changes after the click
        
        
        
        # YEAR DROP DOWN
        # Switch back to the main content if in an iframe
        driver.switch_to.default_content()
        
        # Locate and click the "History" element
        history_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'History') and contains(@class, 'ng-star-inserted')]"))
        )
        history_element.click()
        time.sleep(3)  # Wait for any potential page load or changes after the click
        


        # Locate and click the year dropdown
        year_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='yearSelection']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", year_dropdown)
        year_dropdown.click()
        time.sleep(1)  # Wait for the dropdown options to appear

        # Select the desired year
        desired_year = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.XPATH, "//select[@id='yearSelection']/option[text()='2021']"))
             EC.element_to_be_clickable((By.XPATH, f"//select[@id='yearSelection']/option[text()='{year}']"))
        )
        desired_year.click()
        time.sleep(3)  # Wait for any potential page load or changes after the click


        
        #day dropdown
        # Locate the day dropdown
        day_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='daySelection']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", day_dropdown)

        # Create a Select object for the day dropdown
        day_select = Select(day_dropdown)

        # Select the desired day
        day_select.select_by_visible_text(day)  # Change '15' to the desired day
        time.sleep(3)  # Wait for any potential page load or changes after the click

        
        #month dropdown
        # Locate the month dropdown
        month_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@id='monthSelection']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", month_dropdown)

        # Create a Select object for the month dropdown
        month_select = Select(month_dropdown)

        # Select the desired month
        month_select.select_by_visible_text( month)  # Change 'February' to the desired month
        time.sleep(3)  # Wait for any potential page load or changes after the click


        # Locate and click the "View" button
        view_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='dateSubmit' and @type='submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", view_button)
        view_button.click()
        time.sleep(5)  # Wait for the page to load after clicking "View"




        r = driver.page_source
    except Exception as e:
        print(f"An error occurred: {e}")
        r = None
    # print(r)
    # input()
    driver.quit()
    return r

def scraper(page, dates,postal_code,city):
    output = pd.DataFrame()

    for d in dates:
        url = f"{page}{d}"
        r = render_page(url,d,postal_code,city)

        soup = BS(r, "html.parser")
        
        
        # print("before table")
        # input()
        # Find table based on aria-labelledby attribute
        table = soup.find('table', attrs={'aria-labelledby': 'History observation'})
        # print(table)
        if table:
            df = pd.read_html(str(table))[0]  # Convert HTML table to DataFrame
            df['date_collector']=str(d)
            df['postal_code']=str(postal_code)
            df['city']=str(city)
            df.dropna(subset=['Time'],inplace=True)
            
            output = pd.concat([output, df], ignore_index=True)

        
        # container = soup.find('lib-city-history-observation')
        # check = container.find('tbody')

        # data = []

    #     for c in check.find_all('tr', class_='ng-star-inserted'):
    #         for i in c.find_all('td', class_='ng-star-inserted'):
    #             trial = i.text.strip()
    #             data.append(trial)

    #     row_length = len(data) // 17 - 1

    #     if row_length in {28, 29, 30, 31}:
    #         temp_start = 31 - row_length + 1
    #         col_intervals = [3] * 5 + [1]

    #         Temperature = pd.DataFrame([data[temp_start + i * 3: temp_start + (i + 1) * 3] for i in range(row_length)], columns=['Temp_max', 'Temp_avg', 'Temp_min'])
    #         Dew_Point = pd.DataFrame([data[temp_start + row_length * 3 + i * 3: temp_start + row_length * 3 + (i + 1) * 3] for i in range(row_length)], columns=['Dew_max', 'Dew_avg', 'Dew_min'])
    #         Humidity = pd.DataFrame([data[temp_start + row_length * 6 + i * 3: temp_start + row_length * 6 + (i + 1) * 3] for i in range(row_length)], columns=['Hum_max', 'Hum_avg', 'Hum_min'])
    #         Wind = pd.DataFrame([data[temp_start + row_length * 9 + i * 3: temp_start + row_length * 9 + (i + 1) * 3] for i in range(row_length)], columns=['Wind_max', 'Wind_avg', 'Wind_min'])
    #         Pressure = pd.DataFrame([data[temp_start + row_length * 12 + i * 3: temp_start + row_length * 12 + (i + 1) * 3] for i in range(row_length)], columns=['Pres_max', 'Pres_avg', 'Pres_min'])
    #         Date = pd.DataFrame(data[:temp_start - 1], columns=['Date'])
    #         Precipitation = pd.DataFrame(data[temp_start + row_length * 15:], columns=['Precipitation'])
            
    #         print(f"{d} finished!")
    #     else:
    #         print('Data not in normal length')
    #         continue

    #     dfs = [Date, Temperature, Dew_Point, Humidity, Wind, Pressure, Precipitation]
    #     df_final = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
    #     df_final['Date'] = f"{d}-{df_final['Date'].astype(str)}"
    #     print(df_final)
    #     output = pd.concat([output, df_final], ignore_index=True)
    #     # print(output)

    # print('Scraper done!')

    # output = output[['Temp_avg', 'Temp_min', 'Dew_max', 'Dew_avg', 'Dew_min', 'Hum_max',
    #                  'Hum_avg', 'Hum_min', 'Wind_max', 'Wind_avg', 'Wind_min', 'Pres_max',
    #                  'Pres_avg', 'Pres_min', 'Precipitation', 'Date']]
    # print(output)
    return output


data=pd.read_csv('/Users/user/EV_charging_demand_prediction/simplified/california.csv')


# Function to evaluate string representation of list to actual list
# Function to parse date strings in the list
from datetime import datetime


# Function to parse date strings in the list
def parse_date_list(date_list_str):
    # Remove surrounding brackets
    date_list_str = date_list_str.strip("[]")
    if not date_list_str:  # Check if the string is empty after stripping brackets
        return []
    
    # Split by ', datetime.date(' to get individual date strings
    date_strs = date_list_str.split(", datetime.date(")
    
    # Remove 'datetime.date(' from the first element if present
    date_strs[0] = date_strs[0].replace("datetime.date(", "")
    
    # Parse each date string to datetime.date object, ensuring no empty strings or NaNs
    dates = []
    for date_str in date_strs:
        date_str = date_str.strip(")")
        
        # Handle case for 'nan' or empty strings
        if date_str.strip() == 'nan' or date_str.strip() == '':
            continue
        
        try:
            date = datetime.strptime(date_str, "%Y, %m, %d").strftime("%Y %B %d")
            dates.append(date)
        except ValueError:
            # Handle cases where date_str is not in expected format
            continue
    
    return dates


# Apply the function to the 'Date List' column
data['Date List'] = data['Date List'].apply(parse_date_list)
# Replace whitespace with '%20' in the 'City' column
data['City'] = data['City'].str.replace(' ', '%20')

# dates = ['2019-4', '2019-5']
# for index,row in data.iterrows():
#     # for date in :
        
#         # print(date)
#     print(row['Postal Code'])
#     print(row['City'])
    
    
#     # https://www.wunderground.com/history/daily/us/tn/knoxville/KTYS/date/2019-4-1
#     # page = 'https://www.wunderground.com/history/monthly/pt/lisbon/LPPT/date/2019-4'
#     page_1 = 'https://www.wunderground.com/weather/us/'
#     page_2= 'ca/'+str(row['City'])
#     page_3= '/'+str(row['Postal Code'])
#     page_4= '/date/'
#     # page_5=str(date)
#     page=page_1+page_2+str(page_3)+str(page_4)
    
#     df_output = scraper(page, row['Date List'],row['Postal Code'],row['City'])
    
#     print(page)

# Initialize a counter to track rows processed
counter = 0

# Initialize an empty list to store all DataFrames
all_dfs = []

for index, row in data.iterrows():
    # Construct URL or page details based on row data
    page_1 = 'https://www.wunderground.com/weather/us/'
    page_2 = 'ca/' + str(row['City'])
    page_3 = '/' + str(row['Postal Code'])
    page_4 = '/date/'
    page = page_1 + page_2 + str(page_3) + str(page_4)

    # Assuming scraper() returns a DataFrame
    df_output = scraper(page, row['Date List'], row['Postal Code'], row['City'])

    # Append the DataFrame to the list of all DataFrames
    all_dfs.append(df_output)

    # Print or do other operations as needed
    # print(page)
    # print(row['Postal Code'])
    # print(row['City'])

    # Increment the counter
    counter += 1

    # Check if 100 rows have been processed
    if counter % 10 == 0:
        # If 100 rows have been processed, create a new file or append to existing file
        filename = f'output_{counter // 10}.csv'
        # Concatenate all DataFrames so far
        concatenated_df = pd.concat(all_dfs, ignore_index=True)
        # Save concatenated DataFrame to CSV
        concatenated_df.to_csv(filename, index=False)
        # Clear the list of DataFrames to free up memory
        all_dfs = []

# After the loop, save any remaining DataFrames
if all_dfs:
    filename = f'output_{counter // 10 + 1}.csv'
    concatenated_df = pd.concat(all_dfs, ignore_index=True)
    concatenated_df.to_csv(filename, index=False)
