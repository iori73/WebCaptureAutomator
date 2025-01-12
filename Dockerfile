# # --- Dockerfile ---

# # (1) Python 3.9-slim イメージをベースにする (他のバージョンでもOK)
# FROM python:3.9-slim

# # (2) 必要なツールを apt-get でインストール
# RUN apt-get update && apt-get install -y \
#     wget gnupg2 unzip \
#     && rm -rf /var/lib/apt/lists/*

# # (3) Google Chrome のリポジトリ鍵登録 & リポジトリ追加
# RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" \
#     > /etc/apt/sources.list.d/google-chrome.list

# # (4) Chrome 本体 & ChromeDriver をインストール
# RUN apt-get update && apt-get install -y google-chrome-stable chromium-chromedriver

# # (5) 作業ディレクトリを /app にする
# WORKDIR /app

# # (6) プロジェクト内のファイルをコピー
# #     (パスの指定ミスがないよう注意。requirements.txt や app.py を含む全ファイルをコピー)
# COPY . /app

# # (7) Pythonライブラリをインストール
# RUN pip install --no-cache-dir -r requirements.txt

# # (8) Flaskはデフォルト5000番ポートを使うが、Render側で適宜ルーティングするので一応EXPOSE
# EXPOSE 5000

# # (9) gunicornで起動 (app.py 内の app を実行)
# CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]




FROM --platform=linux/amd64 python:3.9-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    curl \
    --no-install-recommends

# Chromeリポジトリの設定
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | \
    gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/google.gpg --import && \
    chmod 644 /etc/apt/trusted.gpg.d/google.gpg && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Chrome本体のインストール
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends


# ChromeDriverのインストール部分を修正
RUN CHROMEDRIVER_VERSION=$(curl -sS "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE") && \
    wget -q --continue -P /tmp "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver*


WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
# CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

# CMD ["gunicorn", "--worker-class=gevent", "--worker-connections=1000", "--workers=3", "--timeout=300", "app:app", "--bind", "0.0.0.0:5000"]

CMD ["gunicorn", "--timeout", "300", "--workers", "2", "app:app", "--bind", "0.0.0.0:5000"]
