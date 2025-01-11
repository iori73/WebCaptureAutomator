# # md対応
# from flask import Flask, render_template, request, jsonify
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import time
# import os

# from webdriver_manager.chrome import ChromeDriverManager
# from flask import send_file
# import io
# from zipfile import ZipFile


# app = Flask(__name__)



# @app.route('/')
# def index():
#     return render_template('index.html')


# def create_site_directory(url):
#     # URLからドメイン名を抽出してフォルダ名として使用
#     domain = url.split('//')[1].split('/')[0]
#     site_dir = os.path.join('static', 'screenshots', domain)
    
#     # ディレクトリが存在しない場合は作成
#     if not os.path.exists(site_dir):
#         os.makedirs(site_dir)
#     return site_dir



# @app.route('/screenshot', methods=['POST'])
# def take_screenshots():
#     urls = request.json.get('urls', [])
#     print(f"受け取ったURL数: {len(urls)}")
    
#     # options = Options()
#     # options.add_argument('--headless')
#     # options.add_argument('--disable-gpu')
    
#     # # ブラウザのデフォルトダウンロード設定を使用
#     # options.add_experimental_option('prefs', {
#     #     "download.prompt_for_download": True,  # ダウンロードダイアログを表示
#     #     "download.directory_upgrade": True,
#     #     "safebrowsing.enabled": True
#     # })
    
#     # options.add_argument('--start-maximized')
#     # options.add_argument('--window-size=1440,900')
#     # options.add_argument('--no-sandbox')
#     # options.add_argument('--disable-dev-shm-usage')
    
#     # chromedriver_path = os.path.join("chromedriver-mac-arm64", "chromedriver")
#     # service = Service(executable_path=chromedriver_path)
    
#     # ChromeDriverの設定を変更
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")

#     service = Service(ChromeDriverManager().install())
    
    
    
    
#     # results = []
#     # for index, url in enumerate(urls, 1):
#     screenshots = []
#     for url in urls:
#         try:
#             # 各URLごとに新しいドライバーインスタンスを作成
#             driver = webdriver.Chrome(service=service, options=options)
#             print(f"処理中 {index}/{len(urls)}: {url}")
#             driver.get(url)
#             time.sleep(3)
            
#             # Material.ioサイトの場合は特別な処理を行う
#             if "m3.material.io" in url:
#                 total_height = driver.execute_script("""
#                     const container = document.querySelector('.page-content.page-content-height.ng-tns-c33-0');
#                     if (container) {
#                         return Math.max(
#                             container.scrollHeight,
#                             container.offsetHeight,
#                             container.clientHeight
#                         );
#                     } else {
#                         return Math.max(
#                             document.body.scrollHeight,
#                             document.documentElement.scrollHeight,
#                             document.body.offsetHeight,
#                             document.documentElement.offsetHeight,
#                             document.body.clientHeight,
#                             document.documentElement.clientHeight
#                         );
#                     }
#                 """)
#             else:
#                 total_height = driver.execute_script("""
#                     return Math.max(
#                         document.body.scrollHeight,
#                         document.documentElement.scrollHeight,
#                         document.body.offsetHeight,
#                         document.documentElement.offsetHeight,
#                         document.body.clientHeight,
#                         document.documentElement.clientHeight
#                     );
#                 """)
            
#             # 高さが32000px以上の場合は制限する
#             max_height = 32000
#             if total_height > max_height:
#                 print(f"高さを{max_height}pxに制限します（元の高さ: {total_height}px）")
#                 total_height = max_height
            
#             print(f"取得した高さ: {total_height}")
#             driver.set_window_size(1440, total_height)
#             time.sleep(2)
            
            
            
            
            
#         #     site_dir = create_site_directory(url)
#         #     filename = f"{url.split('/')[-1] if url.split('/')[-1] else 'index'}.png"
#         #     filepath = os.path.join(site_dir, filename)
            
#         #     driver.execute_script("window.scrollTo(0, 0);")
#         #     time.sleep(1)
            
#         #     driver.save_screenshot(filepath)
#         #     print(f"スクリーンショット保存完了: {filepath}")
            
#         #     results.append({
#         #         'url': url,
#         #         'status': 'success',
#         #         'filename': os.path.join(os.path.basename(site_dir), filename)
#         #     })
            
#         #     # 各URL処理後にドライバーを終了
#         #     driver.quit()
            
#         # except Exception as e:
#         #     print(f"エラー発生 - URL: {url}")
#         #     print(f"エラー内容: {str(e)}")
#         #     results.append({
#         #         'url': url,
#         #         'status': 'error',
#         #         'message': str(e)
#         #     })
#         #     try:
#         #         driver.quit()
#         #     except:
#         #         pass
        
#         # スクリーンショットをメモリ上で保持
#         screenshots = []
#         for url in urls:
#             # ... スクリーンショット取得のコード ...
            
#             # メモリ上にバイナリとして保存
#             img_binary = io.BytesIO()
#             driver.save_screenshot(img_binary)
#             img_binary.seek(0)
#             screenshots.append({
#                 'binary': img_binary,
#                 'filename': filename
#             })
#             driver.quit()
            
#         except Exception as e:
#             print(f"エラー発生 - URL: {url}")
#             print(f"エラー内容: {str(e)}")
#             try:
#                 driver.quit()
#             except:
#                 pass
        
#         # ZIPファイルとしてまとめる
#         memory_file = io.BytesIO()
#         with ZipFile(memory_file, 'w') as zf:
#             for screenshot in screenshots:
#                 zf.writestr(screenshot['filename'], screenshot['binary'].getvalue())
        
#         memory_file.seek(0)
#         return send_file(
#             memory_file,
#             mimetype='application/zip',
#             as_attachment=True,
#             download_name='screenshots.zip'
#         )
            
    
#     print(f"処理完了 - 成功: {len([r for r in screenshots if r['status'] == 'success'])}/{len(urls)}")
#     return jsonify(screenshots)


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import io
from zipfile import ZipFile

app = Flask(__name__)


@app.route('/healthz')
def healthz():
    return 'ok', 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/screenshot', methods=['POST'])
def take_screenshots():
    urls = request.json.get('urls', [])
    print(f"受け取ったURL数: {len(urls)}")
    
    # ChromeDriverの設定
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1440,900')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")

    service = Service(ChromeDriverManager().install())
    
    screenshots = []
    for index, url in enumerate(urls, 1):
        try:
            # 各URLごとに新しいドライバーインスタンスを作成
            driver = webdriver.Chrome(service=service, options=options)
            print(f"処理中 {index}/{len(urls)}: {url}")
            driver.get(url)
            time.sleep(3)
            
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
                total_height = driver.execute_script("""
                    return Math.max(
                        document.body.scrollHeight,
                        document.documentElement.scrollHeight,
                        document.body.offsetHeight,
                        document.documentElement.offsetHeight,
                        document.body.clientHeight,
                        document.documentElement.clientHeight
                    );
                """)
            
            # 高さが32000px以上の場合は制限する
            max_height = 32000
            if total_height > max_height:
                print(f"高さを{max_height}pxに制限します（元の高さ: {total_height}px）")
                total_height = max_height
            
            print(f"取得した高さ: {total_height}")
            driver.set_window_size(1440, total_height)
            time.sleep(2)
            
            # スクロール処理を追加
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            # メモリ上にスクリーンショットを保存
            img_binary = io.BytesIO()
            driver.save_screenshot(img_binary)
            img_binary.seek(0)
            
            filename = f"{url.split('/')[-1] if url.split('/')[-1] else 'index'}.png"
            screenshots.append({
                'binary': img_binary,
                'filename': filename,
                'url': url,
                'status': 'success'
            })
            
            driver.quit()
            
        except Exception as e:
            print(f"エラー発生 - URL: {url}")
            print(f"エラー内容: {str(e)}")
            try:
                driver.quit()
            except:
                pass
    
    print(f"処理完了 - 成功: {len([s for s in screenshots if s['status'] == 'success'])}/{len(urls)}")
    
    # ZIPファイルとしてまとめる
    memory_file = io.BytesIO()
    with ZipFile(memory_file, 'w') as zf:
        for screenshot in screenshots:
            if screenshot.get('binary'):
                zf.writestr(screenshot['filename'], screenshot['binary'].getvalue())
    
    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name='screenshots.zip'
    )

if __name__ == '__main__':
    app.run(debug=True)
