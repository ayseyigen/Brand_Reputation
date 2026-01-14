from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import csv
import time
import pyodbc
path = 'C://chromedriver.exe'

paths = webdriver.ChromeOptions()
paths.add_experimental_option("useAutomationExtension", False)
paths.add_experimental_option("excludeSwitches", ["enable-automation"])

browser = webdriver.Chrome(options=paths)
browser.maximize_window()
browser.delete_all_cookies()
browser.get("https://www.sikayetvar.com/bmw")
wait = WebDriverWait(browser, 10)

headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

try:
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']"))).click()
except:
    pass

commentlist = []
datelist=[]
count=0

while True:
    try:
        
        comments = browser.find_elements(By.CLASS_NAME, 'complaint-description')
        dates = browser.find_elements(By.CLASS_NAME, 'js-tooltip.time.tooltipstered')
        
        for comment, date in zip(comments, dates):
            commentlist.append(comment.text)
            datelist.append(date.text)
        
        next_button = WebDriverWait(browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='main-content']/div[1]/nav/ul/li/a[@class='page-link active']/i[@class='icomoon-paginate-next']"))
        )
        
        if next_button.is_enabled():
            next_button.click()
            time.sleep(10)
        else:
            break
       
        count += 1
        #if count >= 40:
        #    break
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        break
  #  //*[@id="ins-2e5e6f2b-186f-77d8-e4ca-af388b76a937"]/div[1]/div[1]/div[2]/a
"""
try:
    with open("şikayet1.csv", mode='w', newline='', encoding="utf-8") as csv_file:
        csvWriter = csv.writer(csv_file)
        csvWriter.writerow(["Date", "Comment"]) 
        for date, comment in zip(datelist, commentlist):
            csvWriter.writerow([date, comment])
    print("CSV dosyası başarıyla kaydedildi.")
except Exception as e:
    print(f"CSV dosyası kaydedilirken bir hata oluştu: {str(e)}")


try:
    df = pd.DataFrame({"Date": datelist, "Comment": commentlist})
    excel_file = "şikayet1.xlsx"
    df.to_excel(excel_file, index=False)
    print("Excel dosyası başarıyla kaydedildi.")
except Exception as e:
    print(f"Excel dosyası kaydedilirken bir hata oluştu: {str(e)}")
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
browser.quit()
