import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import jdatetime
import json
import locale

# تنظیم لوکال برای تاریخ
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# مسیر ChromeDriver
chromedriver_path = "E:/1-python/8-telegram-bot/1-telegram-scraper/chromedriver.exe"

# تنظیمات کروم
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/133.0.0.0 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# تنظیم Service
service = Service(executable_path=chromedriver_path)

# باز کردن مرورگر
driver = webdriver.Chrome(service=service, options=chrome_options)
print("کروم باز شد!")

# رفتن به تلگرام وب و لاگین
for attempt in range(3):
    try:
        driver.get("https://web.telegram.org/k/")
        print("تلگرام وب باز شد! لطفاً لاگین کن.")
        break
    except Exception as e:
        print(f"خطا در اتصال (تلاش {attempt + 1}): {e}")
        time.sleep(5)
else:
    print("اتصال به تلگرام وب ممکن نشد!")
    driver.quit()
    exit()

time.sleep(30)  # 30 ثانیه برای لاگین

# رفتن به اولین پیام
for attempt in range(3):
    try:
        driver.get("https://t.me/ZXgasket/2")
        print("رفتیم به اولین پیام چنل!")
        break
    except Exception as e:
        print(f"خطا در رفتن به پیام اول (تلاش {attempt + 1}): {e}")
        time.sleep(5)
else:
    print("نشد به پیام اول وصل بشیم!")
    driver.quit()
    exit()

time.sleep(20)  # صبر برای لود

# موقعیت موس رو به وسط صفحه می‌برم
pyautogui.moveTo(960, 540)  # رزولوشن 1920x1080 فرض شده

# قالب جدید کپشن
new_caption_template = """ارتباط با کارشناسان فروش:
خانم ایمانی:
آقای یاوری:
خانم خلیل زاده:
اینستاگرام: https://instagram.com/hscogroup
کانال تلگرام:
سایت: http://www.hsarico.com
آدرس: خیابان ملت - پاساژ ملت -طبقه اول - پلاک 65
تاریخ انتشار: {gregorian_date} | {persian_date}"""

# جمع‌آوری پست‌ها با اسکرول به پایین
posts_data = []
last_height = 0
post_count = 0

while True:
    posts = driver.find_elements(By.CSS_SELECTOR, ".bubble.channel-post")
    for post in posts[post_count:]:
        post_count += 1
        try:
            # گرفتن متن کپشن
            try:
                caption_elem = post.find_element(By.CSS_SELECTOR, ".translatable-message")
                old_caption = caption_elem.text
            except:
                old_caption = "بدون کپشن"

            # گرفتن تاریخ میلادی
            time_elem = post.find_element(By.CSS_SELECTOR, ".time-inner")
            gregorian_date = time_elem.get_attribute("title").split(",")[0].strip()

            # تبدیل به شمسی
            try:
                date_obj = time.strptime(gregorian_date, "%d %B %Y")
                persian_date = jdatetime.date.fromgregorian(day=date_obj.tm_mday, month=date_obj.tm_mon, year=date_obj.tm_year).strftime("%Y/%m/%d")
            except ValueError as e:
                print(f"خطا در تبدیل تاریخ پست {post_count}: {e}")
                persian_date = "نامشخص"

            # ساخت کپشن جدید
            new_caption = new_caption_template.format(gregorian_date=gregorian_date, persian_date=persian_date)

            # گرفتن مدیا
            media_url = ""
            media_path = ""
            try:
                img = post.find_element(By.CSS_SELECTOR, ".media-photo")
                media_url = img.get_attribute("src")
                media_path = f"media_{post_count}.jpg"
            except:
                try:
                    video = post.find_element(By.CSS_SELECTOR, ".media-video")
                    media_url = video.get_attribute("src")
                    media_path = f"media_{post_count}.mp4"
                except:
                    print(f"پست {post_count}: مدیا پیدا نشد.")

            print(f"پست {post_count}: {old_caption[:50]}... - تاریخ: {gregorian_date} | {persian_date}")
            posts_data.append({
                "id": post_count,
                "old_caption": old_caption,
                "new_caption": new_caption,
                "gregorian_date": gregorian_date,
                "persian_date": persian_date,
                "media_url": media_url,
                "media_path": media_path
            })
        except Exception as e:
            print(f"خطا در پست {post_count}: {e}")

    # اسکرول به پایین
    print("اسکرول به پایین...")
    pyautogui.scroll(-500)  # 500 واحد به پایین
    time.sleep(3)

    # چک کردن پایان
    new_height = driver.execute_script("return document.querySelector('.bubbles-inner').scrollHeight;")
    current_position = driver.execute_script("return document.querySelector('.bubbles-inner').scrollTop + document.querySelector('.bubbles-inner').clientHeight;")
    if current_position >= new_height - 100:
        print(f"تموم شد! {post_count} پست پیدا شد.")
        break
    last_height = new_height

# ذخیره اطلاعات
with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=4)
print("اطلاعات توی posts.json ذخیره شد!")

# بستن مرورگر
driver.quit()