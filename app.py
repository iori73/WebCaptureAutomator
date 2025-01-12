# # app.py
from flask import Flask, render_template, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import io
from zipfile import ZipFile
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ロギング設定
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"エラーが発生しました: {str(e)}")
    return jsonify({"error": "スクリーンショットの取得に失敗しました"}), 400

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/")
def index():
    return render_template("index.html")

def get_scrollable_height(driver):
    return driver.execute_script("""
        // スクロール可能な要素を探す
        const scrollableElements = Array.from(document.querySelectorAll('*')).filter(el => {
            const style = window.getComputedStyle(el);
            return (style.overflow === 'auto' || style.overflow === 'scroll' ||
                   style.overflowY === 'auto' || style.overflowY === 'scroll') &&
                   el.scrollHeight > el.clientHeight;
        });

        // 通常のページ高さも考慮
        const normalHeight = Math.max(
            document.body.scrollHeight,
            document.documentElement.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.offsetHeight,
            document.body.clientHeight,
            document.documentElement.clientHeight
        );

        // スクロール可能要素の高さと通常の高さを比較して最大値を返す
        return Math.max(...scrollableElements.map(el => el.scrollHeight), normalHeight);
    """)
    
    
def wait_for_element(driver, css_selector, timeout=30):
    """
    指定したCSSセレクタが現れるまで待機する。最大 timeout 秒待って無ければTimeoutException。
    """
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    )


@app.route("/screenshot", methods=["POST"])
def take_screenshots():
    try:
        app.logger.debug(f"受信したリクエスト: {request.json}")
        urls = request.json.get("urls", [])
        
        if not urls:
            return jsonify({"error": "URLが提供されていません"}), 400

        app.logger.debug(f"受け取ったURL数: {len(urls)}")

        CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
        CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"

        options = Options()
        options.binary_location = CHROME_BIN
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        service = Service(CHROMEDRIVER_PATH)
        
        screenshots = []
        # for index, url in enumerate(urls, 1):
        #     driver = None
        #     try:
        #         app.logger.debug(f"Processing URL {index}/{len(urls)}: {url}")
        #         driver = webdriver.Chrome(service=service, options=options)
                
        #         driver.get(url)
        #         time.sleep(10)

        #         # ページの読み込み完了を待機（最大30秒）
        #         wait_time = 0
        #         while wait_time < 30:
        #             if driver.execute_script("return document.readyState") == "complete":
        #                 break
        #             time.sleep(1)
        #             wait_time += 1

        #         total_height = get_scrollable_height(driver)

        #         max_height = 90000
        #         if total_height > max_height:
        #             app.logger.debug(f"高さを{max_height}pxに制限します（元の高さ: {total_height}px）")
        #             total_height = max_height

        #         app.logger.debug(f"取得した高さ: {total_height}")
        #         driver.set_window_size(1440, total_height)
        #         time.sleep(2)

        #         # ページが確実に描画されるまで待つ
        #         driver.execute_script("return document.readyState") == "complete"
        #         time.sleep(1)
        for index, url in enumerate(urls, 1):
            driver = None
            try:
                app.logger.debug(f"Processing URL {index}/{len(urls)}: {url}")
                driver = webdriver.Chrome(service=service, options=options)

                driver.get(url)
                time.sleep(10)

                # 1) ページ読み込み完了を待機 (最大30秒)
                wait_time = 0
                while wait_time < 30:
                    if driver.execute_script("return document.readyState") == "complete":
                        break
                    time.sleep(1)
                    wait_time += 1
                
                # 2) さらにサイト固有の要素を待機 (例: ledix.jpなら .index-root が表示されるまで)
                #    適切なCSSセレクタは各サイトに合わせて調整してください
                try:
                    wait_for_element(driver, ".index-root", timeout=30)
                    time.sleep(2)  # 念のため少し追加待機
                except Exception as e:
                    app.logger.debug(f"指定要素が見つかりません: {e}")
                
                # 3) スクロール可能な最大高さを取得し、ウィンドウサイズをセット
                total_height = get_scrollable_height(driver)
                max_height = 90000
                if total_height > max_height:
                    app.logger.debug(f"高さを{max_height}pxに制限します（元の高さ: {total_height}px）")
                    total_height = max_height

                app.logger.debug(f"取得した高さ: {total_height}")
                driver.set_window_size(1440, total_height)
                time.sleep(2)

                # ページが確実に描画されるまで待つ
                driver.execute_script("return document.readyState") == "complete"
                time.sleep(1)
                        

                # ファイル名生成部分
                url_parts = url.split("//")
                if len(url_parts) > 1:
                    domain = url_parts[1].split("/")[0]
                    path_parts = url_parts[1].split("/", 1)
                    if len(path_parts) > 1:
                        filename = f"{domain}_{path_parts[1].replace('/', '_')}.png"
                    else:
                        filename = f"{domain}_index.png"
                else:
                    filename = f"index_{index}.png"

                # スクリーンショットをバイナリで取得
                img_binary = io.BytesIO()
                img_data = driver.get_screenshot_as_png()
                img_binary.write(img_data)
                img_binary.seek(0)

                screenshots.append({
                    "binary": img_binary,
                    "filename": filename,
                    "url": url,
                    "status": "success",
                })

            except Exception as e:
                app.logger.error(f"URL処理エラー: {url} - {str(e)}")
            finally:
                if driver:
                    driver.quit()
                    
                    

        app.logger.debug(
            f"処理完了 - 成功: {len([s for s in screenshots if s['status'] == 'success'])}/{len(urls)}"
        )

        if not screenshots:
            return jsonify({"error": "スクリーンショットの取得に失敗しました"}), 400

        # URLからドメイン名を抽出してZIPファイル名を作成
        first_url = urls[0]
        domain = first_url.split("//")[1].split("/")[0]
        zip_filename = f"{domain}.zip"

        # ZIPファイル作成
        memory_file = io.BytesIO()
        with ZipFile(memory_file, "w") as zf:
            for screenshot in screenshots:
                if screenshot.get("binary") and screenshot["binary"].getvalue():
                    zf.writestr(screenshot["filename"], screenshot["binary"].getvalue())

        if memory_file.getvalue():
            memory_file.seek(0)
            response = send_file(
                memory_file,
                mimetype="application/zip",
                as_attachment=True,
                download_name=zip_filename,
            )
            response.headers.update({
                "Content-Type": "application/zip",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            })
            return response
        else:
            return jsonify({"error": "有効なスクリーンショットがありません"}), 400

    except Exception as e:
        app.logger.error(f"予期せぬエラー: {str(e)}")
        return jsonify({"error": "予期せぬエラーが発生しました"}), 500

if __name__ == "__main__":
    app.run(debug=True)
