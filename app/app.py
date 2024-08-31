import os
from time import sleep
import requests
import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
USER_ID = os.environ.get("USER_ID", "")
PASSWORD = os.environ.get("PASSWORD", "")
URL = os.environ.get("URL", "")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")


def main():
    try:
        # データの取得・成型
        chromedriver_bin = "/usr/bin/chromedriver"
        service = Service(executable_path=chromedriver_bin)

        # Chromeオプションを設定
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(service=service, options=options)

        driver.get(URL)

        # ページの読み込みが完了するまで待機
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        driver.find_element(By.ID, "id_user_id").send_keys(USER_ID)
        driver.find_element(By.ID, "next").click()

        # nextボタンを押してから次のページが表示されるまで待機
        sleep(1)

        driver.find_element(By.ID, "id_pw").send_keys(PASSWORD)
        driver.find_element(By.ID, "login").click()

        # ログイン後のページが表示されるまで待機
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # ページのソースを取得
        page_source = driver.page_source

        # BeautifulSoupで解析
        soup = BeautifulSoup(page_source, "html.parser")

        # ニフティの使用権を取得
        element = soup.find(class_="list_def_total_carried").find("dd")
        nifty_dibs = element.get_text(strip=True)
        print(nifty_dibs)

        driver.quit()

        # 現在時刻から翌月をyyyymmm形式で取得
        today = datetime.date.today()
        one_month_after = today + relativedelta(months=1)
        one_month_after_str = one_month_after.strftime("%Y年%m月")

        # wehbookで通知
        payload = {"text": f"もうすぐ *{one_month_after_str}* の請求確定です。\n現在のニフティの使用権: *{nifty_dibs}* \n足りない場合は、以下のサイドから使用権変換をしましょう。\nhttps://lifemedia.jp/exchange/giftstart/nifty"}
        requests.post(WEBHOOK_URL, json=payload)

    except Exception as e:
        print(e)
        raise e

    return


if __name__ == "__main__":
    main()
