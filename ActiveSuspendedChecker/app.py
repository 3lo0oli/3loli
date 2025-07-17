
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import time

st.set_page_config(page_title="حالة حسابات Reddit", page_icon="🔍")
st.title("🔎 أداة التحقق من حالة الحسابات على Reddit")
st.markdown("تحقق من حالة الحسابات: نشطة ✅ - موقوفة 🚫 - محذوفة ❌")

user_input = st.text_area("✏️ أدخل روابط حسابات Reddit (رابط في كل سطر):")

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")
    return webdriver.Chrome(options=chrome_options)

def check_reddit_status(url):
    try:
        driver = get_driver()
        driver.set_page_load_timeout(15)
        driver.get(url)
        time.sleep(5)
        page = driver.page_source.lower()
        driver.quit()

        if "this account has been suspended" in page:
            return "🚫 موقوف"
        elif "sorry, nobody on reddit goes by that name" in page:
            return "❌ غير موجود"
        else:
            return "✅ نشط"
    except (TimeoutException, WebDriverException) as e:
        return f"❌ خطأ: {e}"

if st.button("تحقق الآن"):
    if user_input.strip():
        st.subheader("📊 النتائج:")
        links = [line.strip() for line in user_input.strip().splitlines() if line.strip()]
        for url in links:
            if not url.startswith("https://www.reddit.com/user/"):
                st.warning(f"❗ الرابط غير صحيح: {url}")
                continue
            status = check_reddit_status(url)
            st.write(f"🔗 [{url}]({url}) → {status}")
    else:
        st.warning("يرجى إدخال روابط أولًا.")
