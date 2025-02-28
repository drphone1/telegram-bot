from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import jdatetime
import json
import locale

# تنظیمات اولیه
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
chromedriver_path = "YOUR_CHROMEDRIVER_PATH"
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/133.0.0.0 Safari/537.36")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def login_to_telegram():
    driver.get("https://web.telegram.org/k/")
    print("لطفاً به صورت دستی لاگین کنید...")
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".bubbles-inner"))
    )
    print("لاگین موفقیت‌آمیز بود!")

def scroll_to_top():
    print("در حال اسکرول به بالای کانال...")
    bubbles_inner = driver.find_element(By.CSS_SELECTOR, ".bubbles-inner")
    last_height = driver.execute_script("return arguments[0].scrollHeight", bubbles_inner)
    
    while True:
        driver.execute_script("arguments[0].scrollTo(0, 0)", bubbles_inner)
        time.sleep(2)
        new_height = driver.execute_script("return arguments[0].scrollHeight", bubbles_inner)
        if new_height == last_height:
            break
        last_height = new_height
    print("اسکرول به بالای کانال کامل شد!")

def collect_posts():
    posts_data = []
    processed_ids = set()
    last_height = 0
    retries = 0
    
    while retries < 5:
        driver.execute_script(
            "document.querySelector('.bubbles-inner').scrollBy(0, 1000)"
        )
        time.sleep(3)
        
        # تشخیص پست‌های جدید
        posts = driver.find_elements(By.CSS_SELECTOR, ".bubble.channel-post")
        for post in posts:
            try:
                post_id = post.get_attribute("data-mid") or post.find_element(By.TAG_NAME, 'time').get_attribute("datetime")
                if post_id in processed_ids:
                    continue
                
                # استخراج اطلاعات پست
                caption = post.find_element(By.CSS_SELECTOR, ".translatable-message").text
                date_element = post.find_element(By.CSS_SELECTOR, ".time-inner")
                gregorian_date = date_element.get_attribute("title").split(",")[0].strip()
                
                # تبدیل تاریخ
                try:
                    date_obj = time.strptime(gregorian_date, "%d %B %Y")
                    persian_date = jdatetime.date.fromgregorian(
                        day=date_obj.tm_mday,
                        month=date_obj.tm_mon,
                        year=date_obj.tm_year
                    ).strftime("%Y/%m/%d")
                except:
                    persian_date = "نامشخص"
                
                posts_data.append({
                    "id": post_id,
                    "caption": caption,
                    "date": f"{gregorian_date} | {persian_date}"
                })
                processed_ids.add(post_id)
                
            except NoSuchElementException:
                continue
        
        # بررسی پایان اسکرول
        new_height = driver.execute_script(
            "return document.querySelector('.bubbles-inner').scrollHeight"
        )
        if new_height == last_height:
            retries += 1
        else:
            retries = 0
        last_height = new_height

    return posts_data

# اجرای اصلی
try:
    login_to_telegram()
    driver.get("https://web.telegram.org/k/#@ZXgasket")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".bubble.channel-post"))
    )
    
    scroll_to_top()
    all_posts = collect_posts()
    
    with open("telegram_posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=4)
    print(f"تعداد {len(all_posts)} پست ذخیره شد!")

finally:
    driver.quit()