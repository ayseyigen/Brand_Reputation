import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import pyodbc


def calculate_post_date(collected_date, collected_time, comment_date):
    collected_datetime = datetime.strptime(collected_date + ' ' + collected_time, '%x %X')
    
    if comment_date[-1] == 's':
        hours_ago = int(comment_date[:-1])
        comment_datetime = collected_datetime - timedelta(hours=hours_ago)
    elif comment_date[-1] == 'g':
        days_ago = int(comment_date[:-1])
        comment_datetime = collected_datetime - timedelta(days=days_ago)
    elif comment_date[-1] == 'h':
        weeks_ago = int(comment_date[:-1])
        comment_datetime = collected_datetime - timedelta(weeks=weeks_ago)
    else:
        comment_datetime='n/A'
    
    # Check if the resulting datetime is before 00:00:00, then subtract one day
    if comment_datetime != 'n/A' and comment_datetime.time() < datetime.strptime("00:00:00", "%H:%M:%S").time():
        comment_datetime -= timedelta(days=1)
    
    return comment_datetime



def calculate_comment_date(collected_date, collected_time, comment_date):
    collected_datetime = datetime.strptime(collected_date + ' ' + collected_time, '%m/%d/%Y %H:%M:%S')
    
    if comment_date[-1] == 's':
        hours_ago = int(comment_date[:-1])
        comment_datetime = collected_datetime - timedelta(hours=hours_ago)
    elif comment_date[-1] == 'g':
        days_ago = int(comment_date[:-1])
        comment_datetime = collected_datetime - timedelta(days=days_ago)
    elif comment_date[-1] == 'h':
        weeks_ago = int(comment_date[:-1])
        comment_datetime = collected_datetime - timedelta(weeks=weeks_ago)
    else:
        comment_datetime = None  # Return None if comment date format is not recognized
    
    # Check if the resulting datetime is before 00:00:00, then subtract one day
    if comment_datetime and comment_datetime.time() < datetime.strptime("00:00:00", "%H:%M:%S").time():
        comment_datetime -= timedelta(days=1)
    
    return comment_datetime






def collect_from_instagram(browser,brand):
    
    columns_for_instagram=['Brand_Name','Post_Amount','Followers(K)','Follows','Likes','Post_Sent_Date','Post_Description','Post_Comment',"Comment_Date",'Data_Collected','Time_Collected']

    

    post_amount = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span')))
    post_amount = post_amount.text.strip()
    
    #followers
    followers = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span')))
    followers = followers.text.strip()
    
    if followers[-2:]=="Mn":
        followers=followers[:-2]
        if (',' in followers):  
            followers = followers.replace(',', '')
            followers = int(followers)
            followers *= 100000
        else:
            followers = int(followers)
            followers *= 1000000
    elif followers[-1:]=="B":
        followers=followers[:-1]
        if (',' in followers):    
            followers = followers.replace(',', '')
            followers = int(followers)
            followers*=100
        else:
            followers = int(followers)
            followers *= 1000
    else:
        followers = followers.replace('.', '')
        

    #follows
    try:
        follows = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span/span')))
        follows = follows.text.strip()
    except:
        follows=0


    for k in range(1,20):
        for j in range(1,4):
            #open post
            try:
               
                open_post = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]/div/div[{k}]/div[{j}]/a/div[1]/div[2]')))
                open_post.click()
            except:
                print(k,j,"iteration haven't finished")
                continue
            

            #post likes
            try:
                likes = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span")))
                likes = likes.text.strip()
                
            except:
                try:     
                    likes = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/span/a/span/span")))
                    likes = likes.text.strip()
                except:
                    likes='n/A'
                
            ay_isimleri = {
                    "Ocak": "01",
                    "Şubat": "02",
                    "Mart": "03",
                    "Nisan": "04",
                    "Mayıs": "05",
                    "Haziran": "06",
                    "Temmuz": "07",
                    "Ağustos": "08",
                    "Eylül": "09",
                    "Ekim": "10",
                    "Kasım": "11",
                    "Aralık": "12"
            }
            try :
                #sent date   
                try:
                    sent_date = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/span/time")))
                    sent_date = sent_date.text.strip()
                    
                except:
                    sent_date = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[2]/div/div/a/span/time")))
                    sent_date = sent_date.text.strip()

                if ("gün önce" in sent_date):
                    sent_date=sent_date[:-9]
                    sent_date=sent_date+'g'

                    postime = datetime.now()
                    postdate = postime.strftime("%x")
                    posttime = postime.strftime("%X")
                    post_sent_date=calculate_post_date(postdate,posttime,sent_date)
                    post_sent_date=post_sent_date.strftime("%m-%d-%Y")

                elif ("saat önce" in sent_date):
                    sent_date=sent_date[:-10]
                    sent_date=sent_date+'s'
                    postime = datetime.now()
                    postdate = postime.strftime("%x")
                    posttime = postime.strftime("%X")
                    post_sent_date=calculate_post_date(postdate,posttime,sent_date)
                    post_sent_date=post_sent_date.strftime("%m-%d-%Y")

                
                
                elif ("202" not in sent_date):
                
                    for ay, ay_numarasi in ay_isimleri.items():
                        if ay in sent_date:
                            sent_date = sent_date.replace(ay, ay_numarasi)
                            break

                    sent_date_split = sent_date.split()
                    post_sent_date=f"{sent_date_split[1]}/{sent_date_split[0]}/2024"


                elif("202" in sent_date):
                    for ay, ay_numarasi in ay_isimleri.items():
                        if ay in sent_date:
                            sent_date = sent_date.replace(ay, ay_numarasi)
                            break

                    # Gün ve yılın sırasını düzenle
                    sent_date_split = sent_date.split()
                    post_sent_date=f"{sent_date_split[1]}/{sent_date_split[0]}/{sent_date_split[2]}"
            except:
                post_sent_date='n/A'

            #post description
            try:
                post_description = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[1]/h1")))
                post_description = post_description.text.strip()
                
            except:
                try:
                    post_description = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[1]/li/div/div/div[2]/div[1]/h1")))
                    post_description = post_description.text.strip()
                except:
                    post_description='n/A'
                


            #take all comments to start iteration
            try:
                all_post_comment = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div')))
                all_post_comment = all_post_comment.text.strip()
            #alt of all commnets
            except:
                try:
                    all_post_comment = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div')))
                    all_post_comment = all_post_comment.text.strip()
                except:
                    try:
                        all_post_comment = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[2]/div/div')))
                        all_post_comment = all_post_comment.text.strip()
                    except:
                        all_post_comment = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[2]/div/div')))
                        all_post_comment = all_post_comment.text.strip()
                    


            #upper for starts from 1 so total is 2
            #approximate comment size
            app_comment_size=(len(all_post_comment.split('\n'))//5)+2

            new_df=pd.DataFrame(columns=columns_for_instagram)

            if app_comment_size>=2:
                for i in range(1,app_comment_size):
                    #get comment and comment date
                    try:
                        comment=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,f'/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[{i}]/ul/div/li/div/div/div[2]/div[1]/span')))
                        comment=comment.text.strip()

                        comment_date=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,f'/html/body/div[8]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[{i}]/ul/div/li/div/div/div[2]/div[2]/span/a/time')))
                        comment_date=comment_date.text.strip()

                    except:
                        #get comment and comment date alternatve
                        try:
                            comment=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,f'/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[{i}]/ul/div/li/div/div/div[2]/div[1]/span')))
                            comment=comment.text.strip()
                            
                            comment_date=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH,f'/html/body/div[7]/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div[3]/div/div/div[{i}]/ul/div/li/div/div/div[2]/div[2]/span/a/time')))
                            comment_date=comment_date.text.strip()
                        #comment and comment date with n/A
                        except:
                            comment='n/A'
                            comment_date='n/A'

                    dtime = datetime.now()
                    log_date = dtime.strftime("%m/%d/%Y")
                    log_time = dtime.strftime("%H:%M:%S")

                    
                    comment_date=calculate_comment_date(log_date,log_time,comment_date)
                    if comment_date==None:
                        comment_date='n/A'
                    else:
                        comment_date=comment_date.strftime("%m-%d-%Y")


                        log_list = [brand,post_amount,followers,follows,likes,post_sent_date,post_description,comment,comment_date,log_date,log_time]        
                        length = len(new_df)
                        new_df.loc[length] = log_list
            
            #closing post   
            try:
                close_post = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/div/div[2]/div/div')))
                close_post.click()
            except:
                try:
                    close_post = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[1]/div/div[2]/div/div')))
                    close_post.click()
                except:
                    close_post = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[1]/div/div[2]/div/div/svg')))
                    close_post.click()
                sleep(3)                
    
            # Replace these values with your actual connection details
            server = ''
            database = 'BrandReputation'
            username = ''
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
                table_name = 'instagramdata'

                # Insert data from DataFrame into the SQL Server table
                # Iterate over each row in the DataFrame and insert data into the SQL Server table
                for index, row in df.iterrows():
                    # Construct the SQL query with parameterized values
                    sql_query = f"""
                        INSERT INTO {table_name} 
                        (BrandName, Post_Amount, Followers, Follows, Likes, Post_Send_Date, Post_Description, Post_Comment, Comment_Date, Data_Collected_Date, Data_Collected_Time) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)
                    """
                    
                    # Execute the SQL query with the values from the current row of the DataFrame
                    cursor.execute(sql_query, 
                                row['BrandName'], 
                                row['Post_Amount'], 
                                row['Followers'], 
                                row['Follows'], 
                                row['Likes'], 
                                row['Post_Send_Date'], 
                                row['Post_Description'], 
                                row['Post_Comment'], 
                                row['Comment_Date'], 
                                row['Data_Collected_Date'], 
                                row['Data_Collected_Time'],
                            
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


    
































path = 'C://chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

browser = webdriver.Chrome(options=options)
browser.maximize_window()
browser.get("https://www.instagram.com/")


username_=""
password_=""


username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))


enter_button = browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')

username.send_keys(username_)
password.send_keys(password_)
enter_button.click()


brand=[
    "Aston Martin Türkiye",
    "Suzuki Türkiye",
    "Alfa Romeo Türkiye",
    "Maserati Türkiye",
    "Pirelli Türkiye",
    "ING Türkiye",
    "BMW Türkiye",    
    "Scoda Türkiye",
    "Toyota Türkiye",
    "Audi Türkiye",
    "Eczacıbaşı Topluluğu",
    "İstanbul Sanayi Odası",
    "Yapı Kredi",
     "Kale Grubu",
    "Hepsiburada",
    "Trendyol",
    "turkishairlines", 
    "bekotürkiye",
    "QNB Finansbank",
    "Aselsan",
    "Adidas Türkiye",
    "Emlak Konut GYO",
    "Enerjisa",
    "Pegasus Hava Yolları",
    "Türk Traktör",
    "Borusan Holding",
    "Zorlu Holding",
    "DenizBank", 
     "LC Waikiki",
    "Nestle Türkiye",
    "Burger King tr",
    "turktelekom", 
    "isbankasi", 
    "Sabancı Holding", 
    "Turkcell",
    "Ford Otosan", 
    "BİM Turkiye",
    "Ziraat Bankası",
    "Boyner",
     "Akbank",
    "Vestel", 
    "Koç Holding",
    "cococola tr",
    "Migros Tr",
    "Garanti BBVA",
    "İDO",
    "TEİAŞ",
    "TEDAŞ",
    "İstanbul Ulaşım A.Ş.",
    "Tekfen Holding", 
    "Türkiye İş Bankası",
    "İstanbul Altın Rafinerisi", 
    "Çalık Holding", 
    "Türkiye Halk Bankası", 
    "Ülker",
     "Anadolu Sigorta",
    "Anadolu Isuzu",
    "İzocam",
     "Aygaz",
    "İş Yatırım", 
    "Petrol Ofisi", 
    "İETT",
    "Anadolu Efes TR", 
    "Anadolu Hayat Emeklilik", 
    "Akkök Holding",
    "Doğuş Otomotiv",
    "Doğuş Grubu",
    "Türkiye Finans Katılım Bankası",
    "Türkiye Sigorta", 
    "Alarko Holding",  
    "arçelik",
]

for br in brand:
    sleep(1)
    search_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div/div[1]/div/div')))
    search_button.click()

    search_brand=browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input')

    search_brand.send_keys(br)
    sleep(4)
    brand = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[3]/div/a[1]/div[1]/div/div/div[2]/div/div/div/span')))
    sleep(4)
    brand.click()
    sleep(2)
    collect_from_instagram(browser,br)
