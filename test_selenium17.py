from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
import time
import jdatetime
import json
import locale
import os
import requests

# تنظیم لوکال برای تاریخ
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'English_United States.1252')
    except:
        print("نمی‌توان لوکال را تنظیم کرد، تاریخ شمسی ممکن است درست نباشد.")

# مسیر ChromeDriver
chromedriver_path = "E:/1-python/8-telegram-bot/1-telegram-scraper/chromedriver.exe"

# تنظیمات کروم
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/133.0.0.0 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# افزایش حافظه برای بارگذاری بهتر
chrome_options.add_argument("--js-flags=--max_old_space_size=4096")

# ایجاد پوشه برای ذخیره مدیا
media_dir = "telegram_media"
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# تنظیم Service
service = Service(executable_path=chromedriver_path)

# باز کردن مرورگر
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()  # بزرگ کردن پنجره برای دید بهتر
print("کروم باز شد!")

# رفتن به تلگرام وب و لاگین
driver.get("https://web.telegram.org/k/")
print("تلگرام وب باز شد! لطفاً لاگین کن.")
time.sleep(30)  # 30 ثانیه برای لاگین دستی

# رفتن به کانال
channel_username = "ZXgasket"
driver.get(f"https://web.telegram.org/k/#@{channel_username}")
print(f"رفتیم به کانال @{channel_username}! در حال لود...")

# انتظار برای لود کامل کانال
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".bubbles-inner"))
    )
    time.sleep(5)  # صبر اضافی برای اطمینان از بارگذاری کامل
    print("کانال با موفقیت بارگذاری شد.")
except TimeoutException:
    print("خطا: کانال درست بارگذاری نشد!")

# روش‌های مختلف اسکرول به بالای کانال
print("در حال اسکرول به بالای کانال...")

def scroll_to_top():
    """ترکیب چند روش برای اسکرول به بالای کانال"""
    try:
        # روش 1: با استفاده از کلیک روی دکمه «مشاهده پیام‌های قبلی»
        try:
            earlier_btn = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".load-more"))
            )
            earlier_btn.click()
            print("دکمه 'مشاهده پیام‌های قبلی' پیدا و کلیک شد.")
            time.sleep(3)
        except:
            print("دکمه 'مشاهده پیام‌های قبلی' پیدا نشد.")
        
        # روش 2: اسکرول با جاوااسکریپت
        bubbles_inner = driver.find_element(By.CSS_SELECTOR, ".bubbles-inner")
        for i in range(10):  # 10 بار تلاش
            driver.execute_script("arguments[0].scrollTop = 0;", bubbles_inner)
            time.sleep(1)
            current_scroll = driver.execute_script("return arguments[0].scrollTop;", bubbles_inner)
            if current_scroll < 100:  # اگر تقریبا به بالا رسیدیم
                print(f"اسکرول با جاوااسکریپت موفق بود (scrollTop: {current_scroll})")
                return True
        
        # روش 3: با استفاده از کلید Home
        scrollable = driver.find_element(By.CSS_SELECTOR, ".scrollable.scrollable-y")
        for i in range(5):
            scrollable.send_keys(Keys.HOME)
            time.sleep(1)
        
        # روش 4: اسکرول متوالی به بالا
        last_height = driver.execute_script("return document.querySelector('.bubbles-inner').scrollHeight;")
        for i in range(20):  # 20 بار تلاش برای اسکرول به بالا
            driver.execute_script("document.querySelector('.bubbles-inner').scrollBy(0, -1000);")
            time.sleep(1)
            current_scroll = driver.execute_script("return document.querySelector('.bubbles-inner').scrollTop;")
            if current_scroll < 100:  # اگر تقریبا به بالا رسیدیم
                print(f"اسکرول متوالی موفق بود (scrollTop: {current_scroll})")
                return True
        
        # اسکرول اضطراری به بالا
        print("در حال تلاش نهایی برای اسکرول به بالا...")
        driver.execute_script("""
        var bubbles = document.querySelector('.bubbles-inner');
        bubbles.scrollTop = 0;
        """)
        time.sleep(3)
        
        return True
    except Exception as e:
        print(f"خطا در اسکرول به بالا: {e}")
        return False

# اجرای اسکرول به بالا
if scroll_to_top():
    print("اسکرول به بالای کانال با موفقیت انجام شد.")
else:
    print("مشکلی در اسکرول به بالای کانال وجود داشت اما ادامه می‌دهیم.")

# قالب کپشن جدید
new_caption_template = """ارتباط با کارشناسان فروش:
خانم ایمانی:
آقای یاوری:
خانم خلیل زاده:
اینستاگرام: https://instagram.com/hscogroup
کانال تلگرام:
سایت: http://www.hsarico.com
آدرس: خیابان ملت - پاساژ ملت -طبقه اول - پلاک 65
تاریخ انتشار: {gregorian_date} | {persian_date}"""

# جمع‌آوری پست‌ها
posts_data = []
processed_posts = set()  # برای جلوگیری از تکرار پست‌ها
last_height = 0
post_count = 0
retry_count = 0
max_retries = 5
no_new_posts_counter = 0

# تابع دانلود فایل 
def download_media(url, filename):
    if not url or url.startswith("blob:"):  # بلاب URLها معمولا به طور مستقیم دانلود نمی‌شوند
        print(f"URL مدیا نامعتبر یا بلاب است: {url}")
        return False
    
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"فایل با موفقیت دانلود شد: {filename}")
            return True
        else:
            print(f"خطا در دانلود فایل - کد: {response.status_code}")
            return False
    except Exception as e:
        print(f"خطا در دانلود فایل: {e}")
        return False

# تابع پردازش پست
def process_post(post, post_number):
    try:
        # تعیین ID منحصر به فرد (از URL یا ویژگی‌های دیگر)
        try:
            post_id = post.get_attribute("data-mid") or post.get_attribute("id") or str(post_number)
        except:
            post_id = str(post_number)
            
        # اگر قبلا پردازش شده، رد شود
        if post_id in processed_posts:
            return None
            
        processed_posts.add(post_id)
        
        # گرفتن متن کپشن
        try:
            caption_elem = post.find_element(By.CSS_SELECTOR, ".translatable-message")
            old_caption = caption_elem.text
        except NoSuchElementException:
            old_caption = "بدون کپشن"

        # گرفتن تاریخ میلادی
        try:
            time_elem = post.find_element(By.CSS_SELECTOR, ".time-inner")
            gregorian_date = time_elem.get_attribute("title").split(",")[0].strip()
        except:
            gregorian_date = "نامشخص"

        # تبدیل به شمسی
        try:
            # تبدیل تاریخ به شمسی
            date_obj = time.strptime(gregorian_date, "%d %B %Y")
            persian_date = jdatetime.date.fromgregorian(
                day=date_obj.tm_mday, 
                month=date_obj.tm_mon, 
                year=date_obj.tm_year
            ).strftime("%Y/%m/%d")
        except Exception as e:
            print(f"خطا در تبدیل تاریخ: {e}")
            persian_date = "نامشخص"

        # ساخت کپشن جدید
        new_caption = new_caption_template.format(
            gregorian_date=gregorian_date, 
            persian_date=persian_date
        )

        # گرفتن مدیا (عکس یا ویدیو)
        media_url = ""
        media_path = ""
        media_type = "none"
        
        try:
            # امتحان برای یافتن عکس
            img = post.find_element(By.CSS_SELECTOR, ".media-photo")
            media_url = img.get_attribute("src")
            media_path = os.path.join(media_dir, f"photo_{post_id}.jpg")
            media_type = "photo"
        except NoSuchElementException:
            try:
                # امتحان برای یافتن ویدیو
                video = post.find_element(By.CSS_SELECTOR, ".media-video")
                media_url = video.get_attribute("src")
                media_path = os.path.join(media_dir, f"video_{post_id}.mp4")
                media_type = "video"
            except NoSuchElementException:
                # تلاش برای یافتن تصویر بندانگشتی ویدیو
                try:
                    thumb = post.find_element(By.CSS_SELECTOR, ".video-thumb")
                    media_url = thumb.get_attribute("src")
                    media_path = os.path.join(media_dir, f"thumbnail_{post_id}.jpg")
                    media_type = "video_thumb"
                except:
                    pass

        # دانلود مدیا
        if media_url and media_path:
            download_success = download_media(media_url, media_path)
            if not download_success:
                media_path = f"دانلود ناموفق - URL: {media_url}"

        # اطلاعات پست
        post_data = {
            "id": post_id,
            "number": post_number,
            "old_caption": old_caption,
            "new_caption": new_caption,
            "gregorian_date": gregorian_date,
            "persian_date": persian_date,
            "media_url": media_url,
            "media_path": media_path,
            "media_type": media_type
        }
        
        print(f"پست {post_number} (ID: {post_id}): {old_caption[:50]}... - تاریخ: {gregorian_date} | {persian_date}")
        return post_data
    
    except StaleElementReferenceException:
        print(f"خطا: المنت پست {post_number} از DOM حذف شده")
        return None
    except Exception as e:
        print(f"خطا در پردازش پست {post_number}: {e}")
        return None

# حلقه اصلی برای اسکرول و جمع‌آوری پست‌ها
print("در حال جمع‌آوری پست‌ها...")
while True:
    try:
        # پیدا کردن همه پست‌های فعلی در صفحه
        posts = driver.find_elements(By.CSS_SELECTOR, ".bubble.channel-post")
        
        # پردازش پست‌های جدید
        new_posts_count = 0
        for post in posts:
            post_count += 1
            post_data = process_post(post, post_count)
            if post_data:
                posts_data.append(post_data)
                new_posts_count += 1
                
                # ذخیره تدریجی داده‌ها بعد از هر 10 پست
                if len(posts_data) % 10 == 0:
                    with open("posts.json", "w", encoding="utf-8") as f:
                        json.dump(posts_data, f, ensure_ascii=False, indent=4)
                    print(f"داده‌های {len(posts_data)} پست ذخیره شدند")
        
        # اگر پست جدیدی پیدا نشد، شمارنده را افزایش بده
        if new_posts_count == 0:
            no_new_posts_counter += 1
        else:
            no_new_posts_counter = 0  # اگر پست جدید پیدا شد، شمارنده را ریست کن
            
        # اگر چندین بار پست جدیدی پیدا نشود، ممکن است به انتهای کانال رسیده باشیم
        if no_new_posts_counter >= 5:
            print("پنج بار هیچ پست جدیدی پیدا نشد. احتمالاً به انتهای کانال رسیده‌ایم.")
            break

        # اسکرول به پایین
        current_height = driver.execute_script("return document.querySelector('.bubbles-inner').scrollHeight;")
        driver.execute_script("document.querySelector('.bubbles-inner').scrollBy(0, 800);")
        time.sleep(3)  # کمی صبر کن تا محتوای جدید لود شود
        
        # بررسی پایان اسکرول
        new_height = driver.execute_script("return document.querySelector('.bubbles-inner').scrollHeight;")
        current_position = driver.execute_script(
            "return document.querySelector('.bubbles-inner').scrollTop + document.querySelector('.bubbles-inner').clientHeight;"
        )
        
        # اگر به انتهای صفحه رسیدیم یا ارتفاع تغییر نکرده
        if current_position >= new_height - 100 or current_height == new_height:
            retry_count += 1
            if retry_count >= max_retries:
                print(f"به انتهای کانال رسیدیم! {len(posts_data)} پست پیدا شد.")
                break
            else:
                print(f"به انتها رسیده‌ایم، تلاش {retry_count}/{max_retries} برای اطمینان...")
                time.sleep(2)  # کمی صبر کن و دوباره تلاش کن
        else:
            retry_count = 0  # اگر هنوز مشغول اسکرول هستیم، شمارنده‌ی تلاش‌ها را ریست کن
            
    except Exception as e:
        print(f"خطا در حلقه‌ی اصلی اسکرول: {e}")
        break

# ذخیره نهایی داده‌ها
if posts_data:
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=4)
    print(f"اطلاعات {len(posts_data)} پست با موفقیت در فایل posts.json ذخیره شد!")
else:
    print("هیچ داده‌ای برای ذخیره پیدا نشد!")

# بستن مرورگر
driver.quit()
print("عملیات به پایان رسید.")
