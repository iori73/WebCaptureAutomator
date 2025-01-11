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

# ---
import logging
logging.basicConfig(level=logging.DEBUG)

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"エラーが発生しました: {str(e)}")
    return jsonify({'error': 'スクリーンショットの取得に失敗しました'}), 400
# ---

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
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-setuid-sandbox')  # 追加
    # options.add_argument('--single-process')  # 追加
    options.add_argument('--disable-extensions')  # 追加
    options.add_argument('--disable-software-rasterizer')


    # # Macの場合のChrome位置を指定
    # if os.path.exists('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'):
    #     options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    # else:
    #     # Render環境用の設定
    #     options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")
    
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "/opt/render/project/.render/chrome/opt/google/chrome/chrome")


    service = Service(ChromeDriverManager().install())
    
    screenshots = []
    for index, url in enumerate(urls, 1):
        try:
            driver = webdriver.Chrome(service=service, options=options)
            print(f"処理中 {index}/{len(urls)}: {url}")
            driver.get(url)
            time.sleep(10) 
            
            wait_time = 0
            while wait_time < 30:  # 最大30秒まで追加で待機
                if driver.execute_script("return document.readyState") == "complete":
                    break
                time.sleep(1)
                wait_time += 1
            
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
            
            max_height = 90000
            if total_height > max_height:
                print(f"高さを{max_height}pxに制限します（元の高さ: {total_height}px）")
                total_height = max_height
            
            print(f"取得した高さ: {total_height}")
            driver.set_window_size(1440, total_height)
            time.sleep(2)
            
            driver.execute_script("return document.readyState") == "complete"
            time.sleep(1)
            

            
            # ファイル名生成部分を修正
            url_parts = url.split('//')
            if len(url_parts) > 1:
                domain = url_parts[1].split('/')[0]  
                path_parts = url_parts[1].split('/', 1)  
                if len(path_parts) > 1:
                    filename = f"{domain}_{path_parts[1].replace('/', '_')}.png"
                else:
                    filename = f"{domain}_index.png"
            else:
                filename = f"index_{index}.png"

        
            img_binary = io.BytesIO()
            img_data = driver.get_screenshot_as_png()  
            img_binary.write(img_data)
            img_binary.seek(0)
            
            
            screenshots.append({
                'binary': img_binary,
                'filename': filename,
                'url': url,
                'status': 'success'
            })
            
            driver.quit()
            
        # except Exception as e:
        #     print(f"エラー発生 - URL: {url}")
        #     print(f"エラー内容: {str(e)}")
        #     try:
        #         driver.quit()
        #     except:
        #         pass
        except Exception as e:
            app.logger.error(f"Chrome起動エラー: {str(e)}")
            try:
                driver.quit()
            except:
                pass
            raise

    
    print(f"処理完了 - 成功: {len([s for s in screenshots if s['status'] == 'success'])}/{len(urls)}")
    
    # スクリーンショットの存在確認
    if not screenshots:
        return jsonify({'error': 'スクリーンショットの取得に失敗しました'}), 400
        
        
    # URLからドメイン名を抽出してZIPファイル名を作成
    first_url = urls[0]
    domain = first_url.split('//')[1].split('/')[0]
    zip_filename = f"{domain}.zip"

    # ZIPファイル作成部分のみ修正
    memory_file = io.BytesIO()
    with ZipFile(memory_file, 'w') as zf:
        for screenshot in screenshots:
            if screenshot.get('binary') and screenshot['binary'].getvalue():
                zf.writestr(screenshot['filename'], screenshot['binary'].getvalue())


    
    if memory_file.getvalue():
        memory_file.seek(0)
        response = send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename  # この行を追加
        )
        response.headers.update({
            'Content-Type': 'application/zip'
        })
        return response

    else:
        return jsonify({'error': '有効なスクリーンショットがありません'}), 400




if __name__ == '__main__':
    app.run(debug=True)
