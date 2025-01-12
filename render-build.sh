# # render-build.sh
# # ローカル
# #!/usr/bin/env bash
# # exit on error
# set -o errexit

# STORAGE_DIR=/opt/render/project/.render

# if [[ ! -d $STORAGE_DIR/chrome ]]; then
#     echo "...Downloading Chrome"
#     mkdir -p $STORAGE_DIR/chrome
#     cd $STORAGE_DIR/chrome
#     wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#     dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
#     rm ./google-chrome-stable_current_amd64.deb
# else
#     echo "...Using Chrome from cache"
# fi



# # 😭render用だけどできない
#!/usr/bin/env bash
set -o errexit  # 途中でエラーが出たら止める

echo "=== Start: Custom build script ==="

# 1. Python依存パッケージをインストール
pip install -r requirements.txt

# 2. システムを更新 & 必要ツールをインストール
apt-get update && apt-get install -y wget gnupg2 unzip

# 3. Google Chrome リポジトリを追加
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# 4. 改めて更新して、Google Chrome & ChromeDriver をインストール
apt-get update && apt-get install -y google-chrome-stable chromium-chromedriver

echo "=== Finished: Custom build script ==="
