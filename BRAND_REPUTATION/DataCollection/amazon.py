import datetime
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pyodbc


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_product_info(browser, catalog):
    columns_for_amazon = [catalog, "Brand Name", "Product Name", "Price", "ProductStar", "NumberOfReviews","CommentTitle", "CommentDate","Comment", "Date_Collected", "Time_Collected"]
    
    page_count=1
    count=0
    while (page_count<=1):   
        for i in range(3,53):
            try:
                # Web siteleri genellikle dinamik oldukları için veri çekme işleminde ürünler listelenmeden sıralama yapılmıyor. Bu yüzden beklemek gerekli
                product_link = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/span/div/div/div[2]/div[1]/h2/a/span'))
                )
                product_link.click()
            except:
                try:
                    product_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/div/div/span/div/div/div[2]/div[1]/h2/a/span')))
                    product_link.click()
                except:
                    try:
                        product_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/div/div/span/div/div/div[2]/div[2]/h2/a/span')))
                        product_link.click()
                    except:
                        try:
                            product_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/span/div/div/div[2]/div[1]/h2/a/span')))
                            product_link.click()
                        except:
                            try:
                                product_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, f' //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/span/div/div/div[2]/div[2]/h2/a/span')))
                                product_link.click()
                            except:
                                try:
                                    product_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, f'  //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[{i}]/div/div/span/div/div/div[3]/div[2]/h2/a/span')))
                                    product_link.click()
                                except:
                                    print(f"Timeout: Element {i} not found or not clickable")
                                    continue

            headers={ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

            try:
                brand_name_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "bylineInfo")))
                brand_name = brand_name_element.text.strip()
            except:
                brand_name="n/A"
            if brand_name.startswith('M'):
                brand_name=brand_name[6:]
            else:
                brand_name=brand_name[:-21]

                
            try:
                product_name_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "productTitle")))
                product_name = product_name_element.text.strip()
            except:
                product_name='n/A'

            try:
                star_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="acrPopover"]/span[1]/a/span')))
                star=star_element.text.split()[0]
            except:
                star=0

            try:
                price_element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole")))
                price = price_element.text.strip()
            except:
                price=0

            try:
                noreviews_element = WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.ID, "acrCustomerReviewText")))
                no_reviews = noreviews_element.text.strip()
                no_reviews=no_reviews[:-13]
            except:
                no_reviews=0
            

            try:
                comment_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "cm-cr-dp-review-list")))
                comments = comment_element.text.strip()
                filtered_comments=[]
                comments=comments.split("\n")


                for com in comments:
                    if not com.startswith("Faydalı") and not com.startswith("Bildir") and ("Doğrulanmış Alışveriş" not in com) and ("bunu faydalı buldu" not in com) :
                        filtered_comments.append(com)    




                indexler = [i for i, send_date in enumerate(filtered_comments) if 'tarihinde değerlendirildi' in send_date]
                #delete names of people
                personname_index=[i-2 for i in indexler]

                for index in sorted(personname_index, reverse=True):
                    del filtered_comments[index]
                


                indexler = [i for i, send_date in enumerate(filtered_comments) if 'tarihinde değerlendirildi' in send_date]

                title_index=[i-1 for i in indexler]
                comment_title_array=[]
                for i in title_index:
                    comment_title_array.append(filtered_comments[i])
                for index in sorted(title_index, reverse=True):
                    del filtered_comments[index]
                




                indexler = [i for i, send_date in enumerate(filtered_comments) if 'tarihinde değerlendirildi' in send_date]
                comment_array = []
                comment = ""  
                for i, comment_text in enumerate(filtered_comments):
                    if i not in indexler:
                        comment += comment_text + " "  
                    else:
                        if comment.strip():  
                            comment_array.append(comment.strip())  
                        comment = "" 
                if comment.strip(): 
                    comment_array.append(comment.strip())

                        



                comment_date_array = [filtered_comments[i] for i, send_date in enumerate(filtered_comments) if 'tarihinde değerlendirildi' in send_date]
                for comment_date_element in comment_date_array:
                    comment_date_element=comment_date_element[:-26]
                    comment_date_element=comment_date_element[11:]

            except:
                comment_title_array=['n/A']
                comment_date_array=['n/A']
                comment_array=['n/A']

            
            new_df = pd.DataFrame(columns=columns_for_amazon)
            if len(comment_date_array)==len(comment_array) and len(comment_array)==len(comment_title_array):
                for t in range(len(comment_date_array)):
                    dtime = datetime.datetime.now()
                    log_date = dtime.strftime("%x")
                    log_time = dtime.strftime("%X")

                    comment_date=comment_date_array[t]
                    if len(comment_date)>3:
                        comment_date=comment_date[:-26]
                        comment_date=comment_date[11:]
                    else:
                        comment_date='n/A'

                    if comment_array[t]!=comment_date and comment_date!=comment_title_array[t]:
                        log_list = [catalog,brand_name, product_name, price, star, no_reviews, comment_title_array[t],comment_date,comment_array[t],log_date, log_time]
                        length = len(new_df)
                        new_df.loc[length] = log_list
                    else:
                        continue
                    

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
            try:
                # Establish a connection to the database
                conn = pyodbc.connect(conn_str)
                
                # Create a cursor object to execute SQL queries
                cursor = conn.cursor()

                # Specify the table name you want to insert the data into
                table_name = 'amazonsingledata'

                # Insert data from DataFrame into the SQL Server table
                # Iterate over each row in the DataFrame and insert data into the SQL Server table
                for index, row in new_df.iterrows():
                    # Construct the SQL query with parameterized values
                    sql_query = f"""
                        INSERT INTO {table_name} 
                        (Catalog_Name, Brand_Name, Product_Name, Price, Star, NOReviews, Comment_Title, Comment_Date, Comment, Date_Collected, Time_Collected) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    # Execute the SQL query with the values from the current row of the DataFrame
                    cursor.execute(sql_query, 
                                row['Catalog_Name'], 
                                row['Brand_Name'], 
                                row['Product_Name'], 
                                row['Price'], 
                                row['Star'], 
                                row['NOReviews'], 
                                row['Comment_Title'], 
                                row['Comment_Date'], 
                                row['Comment'], 
                                row['Date_Collected'], 
                                row['Time_Collected'],
                                )

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

            browser.back()

        try:
            next_page = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, f'Sonraki')))
            next_page.click()
        except:
            page_count=6
        
        page_count+=1
        
    print(count)
    return new_df


path = 'C://chromedriver.exe'


catalog = [
    "Yüzme Gözlüğü",
    "Kask",
    "Ayakkabı",
    "Şort",
    "Şapka",
    "Fitness Bandı",
    "Cüzdan",
    "Yastık",
    "Battaniye",
    "Saklama Kabı",
    "İlaç Kutusu",
    "Yatak",
    "Koltuk",
    "Masa",
    "Halı",
    "Fırça",
    "Robot Süpürge",
    "Termostat",
    "Oyun Konsolu",
    "Kahve Makinesi",
    "Blender",
    "Müzik Çalar",
    "Lamba",
    "Güneş Gözlüğü",
    "Yoga Matı",
    "Egzersiz Aleti",
    "Masa Saati",
    "Kamera",
    "Ses Sistemi",
    "Terlik",
    "Diş Fırçası",
    "Diş Macunu",
    "Diş İpi",
    "Tıraş Makinesi",
    "Yazıcı",
    "Kalem",
    "Silgi",
    "Kalemtıraş",
    "Kupa",
    "Fırın",
    "Saksı",
    "Makas",
    "Cetvel",
    "Güvenlik Kamerası",
    "Güneş kremi",
    "Duvar Saati",
    "Tencere",
    "Tava",
    "Tabak",
     "Çatal Bıçak Seti",
    "Oyuncu Koltuğu",
    "USB Flash Bellek",
    "Fare",
    "Telefon Kılıfı",
    "Telefon",
    "Bluetooth Kulaklık",
    "Powerbank",
    "HDMI Kablosu",
    "Taşınabilir Harici Hard Disk",
    "Klavye",
    "Ampul",
    "Priz",
    "Mini Projektör",
    "Bluetooth Hoparlör",
    "Kol Saati"
    ]



options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
browser = webdriver.Chrome(options=options)
browser.maximize_window()
browser.get("https://www.amazon.com.tr/")





for cat in catalog: 
    sleep(2)
    input_search = browser.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
    search_button = browser.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]')
    input_search.clear()
    sleep(1)
    input_search.send_keys(cat)
    search_button.click()

    df = scrape_product_info(browser, cat)


