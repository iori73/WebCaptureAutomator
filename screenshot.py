# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time
# import os

# # スクリーンショットを保存するディレクトリ名
# screenshot_dir = "SS"

# # ディレクトリが存在しない場合は作成
# if not os.path.exists(screenshot_dir):
#     os.makedirs(screenshot_dir)

# # オプション設定
# options = Options()
# options.add_argument("--headless")  # ヘッドレスモード
# options.add_argument("--disable-gpu")  # GPUを無効化（ヘッドレスで必要な場合がある）
# options.binary_location = (
#     "/Users/i_kawano/Documents/WebCaptureAutomator/chrome-mac-arm64/chromedriver"
# )
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# # この行を削除または修正
# options.binary_location = "/Users/i_kawano/Documents/WebCaptureAutomator/chromedriver-mac-arm64/chromedriver"


# # ChromeDriverのServiceオブジェクトを作成
# service = Service("/opt/homebrew/bin/chromedriver")  # ここに適切なChromeDriverのパスを指定

# # WebDriverのセットアップ
# driver = webdriver.Chrome(service=service, options=options)

# # URLリストを更新
# urls = [
#     "https://design.digital.go.jp//introduction",
#     "https://design.digital.go.jp//guidance",
#     "https://design.digital.go.jp//foundations",
#     "https://design.digital.go.jp//components",
#     "https://design.digital.go.jp//resources",
#     "https://design.digital.go.jp//webaccessibility",
# ]

# for url in urls:
#     driver.get(url)
#     time.sleep(2)  # ページが完全にロードされるまで待機

#     # ページの全高さを取得
#     total_height = driver.execute_script("return document.body.scrollHeight")

#     # ウィンドウサイズをページの全高さに調整
#     driver.set_window_size(1440, total_height)
#     time.sleep(2)  # サイズ調整後に少し待機

#     # スクリーンショットのファイル名を生成
#     screenshot_file = os.path.join(
#         screenshot_dir, f"{url.split('//')[-1].replace('/', '_').replace(':', '_')}.png"
#     )

#     # スクリーンショットの取得
#     driver.save_screenshot(screenshot_file)

# # 終了
# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# スクリーンショットを保存するディレクトリ名
screenshot_dir = "SS"

# ディレクトリが存在しない場合は作成
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# オプション設定
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# ChromeDriverのパスを正しく設定（プロジェクトフォルダからの相対パス）
chromedriver_path = os.path.join("chromedriver-mac-arm64", "chromedriver")

# ChromeDriverのServiceオブジェクトを作成
service = Service(executable_path=chromedriver_path)

# WebDriverのセットアップ
driver = webdriver.Chrome(service=service, options=options)

# # URLリストを更新
# urls = [
#     "https://design.digital.go.jp/introduction",
#     "https://design.digital.go.jp/guidance",
#     "https://design.digital.go.jp/foundations",
#     "https://design.digital.go.jp/components",
#     "https://design.digital.go.jp/resources",
#     "https://design.digital.go.jp/webaccessibility",
# ]
urls = [
    "https://m3.material.io/",
    "https://m3.material.io/blog/",
    "https://m3.material.io/components/",
    "https://m3.material.io/develop/",
    "https://m3.material.io/foundations/",
]



for url in urls:
    driver.get(url)
    time.sleep(2)  # ページが完全にロードされるまで待機

    # Material.ioサイトの場合は特別な処理を行う
    if "m3.material.io" in url:
        total_height = driver.execute_script("""
            const container = document.querySelector('.page-content.page-content-height.ng-tns-c33-0');
            if (container) {
                return Math.max(
                    container.scrollHeight,
                    container.offsetHeight,
                    container.clientHeight
                );
            } else {
                return Math.max(
                    document.body.scrollHeight,
                    document.documentElement.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.offsetHeight,
                    document.body.clientHeight,
                    document.documentElement.clientHeight
                );
            }
        """)
    else:
        # 他のサイトの場合は通常の高さ取得
        total_height = driver.execute_script("return document.body.scrollHeight")

    # ウィンドウサイズをページの全高さに調整
    driver.set_window_size(1440, total_height)
    time.sleep(2)  # サイズ調整後に少し待機

    # スクリーンショットのファイル名を生成
    screenshot_file = os.path.join(
        screenshot_dir, f"{url.split('//')[-1].replace('/', '_').replace(':', '_')}.png"
    )

    # スクリーンショットの取得
    driver.save_screenshot(screenshot_file)


# 終了
driver.quit()
