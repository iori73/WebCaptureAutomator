# md対応
from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


def create_site_directory(url):
    # URLからドメイン名を抽出してフォルダ名として使用
    domain = url.split('//')[1].split('/')[0]
    site_dir = os.path.join('static', 'screenshots', domain)
    
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(site_dir):
        os.makedirs(site_dir)
    return site_dir




# @app.route('/screenshot', methods=['POST'])
# def take_screenshots():
#     urls = request.json.get('urls', [])
    
#     options = Options()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--start-maximized')
#     options.add_argument('--window-size=1440,900')
    
#     chromedriver_path = os.path.join("chromedriver-mac-arm64", "chromedriver")
#     service = Service(executable_path=chromedriver_path)
#     driver = webdriver.Chrome(service=service, options=options)
    
#     results = []
#     for url in urls:
#         try:
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
#                 # 他のサイトの場合は通常の高さ取得
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
            
#             # ウィンドウサイズを設定
#             driver.set_window_size(1440, total_height)
#             time.sleep(2)
            
#             # filename = f"{url.split('//')[-1].replace('/', '_').replace(':', '_')}.png"
#             # filepath = os.path.join('static', 'screenshots', filename)
#             site_dir = create_site_directory(url)
#             filename = f"{url.split('/')[-1] if url.split('/')[-1] else 'index'}.png"
#             filepath = os.path.join(site_dir, filename)
            
        
#             # スクロール処理を追加
#             driver.execute_script("window.scrollTo(0, 0);")
#             time.sleep(1)
            
#             driver.save_screenshot(filepath)
            
#             results.append({
#                 'url': url,
#                 'status': 'success',
#                 'filename': os.path.join(os.path.basename(site_dir), filename)
#             })
#         except Exception as e:
#             results.append({
#                 'url': url,
#                 'status': 'error',
#                 'message': str(e)
#             })
    
#     driver.quit()
#     return jsonify(results)

@app.route('/screenshot', methods=['POST'])
def take_screenshots():
    urls = request.json.get('urls', [])
    print(f"受け取ったURL数: {len(urls)}")
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    
    # ブラウザのデフォルトダウンロード設定を使用
    options.add_experimental_option('prefs', {
        "download.prompt_for_download": True,  # ダウンロードダイアログを表示
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1440,900')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    chromedriver_path = os.path.join("chromedriver-mac-arm64", "chromedriver")
    service = Service(executable_path=chromedriver_path)
    
    results = []
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
            
            site_dir = create_site_directory(url)
            filename = f"{url.split('/')[-1] if url.split('/')[-1] else 'index'}.png"
            filepath = os.path.join(site_dir, filename)
            
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            
            driver.save_screenshot(filepath)
            print(f"スクリーンショット保存完了: {filepath}")
            
            results.append({
                'url': url,
                'status': 'success',
                'filename': os.path.join(os.path.basename(site_dir), filename)
            })
            
            # 各URL処理後にドライバーを終了
            driver.quit()
            
        except Exception as e:
            print(f"エラー発生 - URL: {url}")
            print(f"エラー内容: {str(e)}")
            results.append({
                'url': url,
                'status': 'error',
                'message': str(e)
            })
            try:
                driver.quit()
            except:
                pass
    
    print(f"処理完了 - 成功: {len([r for r in results if r['status'] == 'success'])}/{len(urls)}")
    return jsonify(results)







if __name__ == '__main__':
    app.run(debug=True)
