from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import csv
from datetime import datetime
import pyodbc
path = 'C://chromedriver.exe'

paths = webdriver.ChromeOptions()
paths.add_experimental_option("useAutomationExtension", False)
paths.add_experimental_option("excludeSwitches", ["enable-automation"])

browser = webdriver.Chrome(options=paths)
browser.maximize_window()
browser.get("https://x.com/PhilipsTurkiye/status/12119954754376622091")
wait = WebDriverWait(browser, 20)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

username_= "......"
password_="......"
username_control_="....."

# Log in to Twitter
login_button = browser.find_element(By.XPATH, '//*[@id="layers"]/div/div[1]/div/div/div/div/div/div/div/div[1]/a/div/span/span')
login_button.click()

username = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')))
username.send_keys(username_)
next_button = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')
next_button.click()

username_control =WebDriverWait(browser, 18).until(EC.presence_of_element_located((By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')))
username_control.send_keys(username_control_)
next_button2 = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div')
next_button2.click()

password = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
password.send_keys(password_)
enter_button = browser.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div')
enter_button.click()

commentlist = []
datelist = []
count = 0
last = browser.execute_script("return document.documentElement.scrollHeight")

while True:
    try:
        if count > 100:
            break
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(5)
        yeni = browser.execute_script("return document.documentElement.scrollHeight")
        if last == yeni:
            break
        last = yeni
        count += 1

        comments = browser.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        dates = browser.find_elements(By.XPATH, '//time')

        for comment, date in zip(comments, dates):
            commentlist.append(comment.text)
            datelist.append(date.get_attribute("datetime"))

        time.sleep(2)

    except NoSuchElementException:
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

browser.quit()

formatted_dates = [datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %B %Y") for date in datelist]
"""
#excel and csv saved
try:
    with open("Twitter.csv", mode='w', newline='', encoding="utf-8") as csv_file:
        csvWriter = csv.writer(csv_file)
        csvWriter.writerow(["Date", "Comment"])
        for date, comment in zip(formatted_dates, commentlist):
            csvWriter.writerow([date, comment])
    print("CSV file successfully saved.")
except Exception as e:
    print(f"Error saving CSV file: {str(e)}")

df = pd.DataFrame({"Date": formatted_dates, "Comment": commentlist})

excel_file = "Twitter.xlsx"
df.to_excel(excel_file, index=False)
print("Excel file successfully saved.")

"""
# Replace these values with your actual connection details
server = ''
database = 'BrandReputation'
username = 'sa'
password = ''

# Construct the connection string
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

# Assuming you have a DataFrame 'df' already created with the appropriate data
df = pd.DataFrame({
    'Brand': ['Brand1', 'Brand2'],
    'Date': ['2024-05-19', '2024-05-20'],
    'Comment': ['Comment1', 'Comment2']
})

try:
    # Establish a connection to the database
    conn = pyodbc.connect(conn_str)

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Specify the table name you want to insert the data into
    table_name = 'twittersingledata'

    # Insert data from DataFrame into the SQL Server table
    for index, row in df.iterrows():
        # Construct the SQL query with parameterized values
        sql_query = f"""
            INSERT INTO {table_name} 
            (Brand, Date, Comment) 
            VALUES (?, ?, ?)
        """
        
        # Execute the SQL query with the values from the current row of the DataFrame
        cursor.execute(sql_query, 
                       row['Brand'], 
                       row['Date'], 
                       row['Comment'])
                       

    # Commit the transaction
    conn.commit()
    print("Data successfully inserted into the database.")

except pyodbc.Error as e:
    if 'String or binary data would be truncated' in str(e):
        print('Warning: Some data exceeds column width. Skipping insertion of that row.')
    else:
        print('Error:', e)

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
