# #!/usr/bin/env bash
# # Chrome のインストール
# curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# apt-get update
# apt-get install -y ./google-chrome-stable_current_amd64.deb
# rm google-chrome-stable_current_amd64.deb


#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project/.render

if [[ ! -d $STORAGE_DIR/chrome ]]; then
    echo "...Downloading Chrome"
    mkdir -p $STORAGE_DIR/chrome
    cd $STORAGE_DIR/chrome
    wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
    rm ./google-chrome-stable_current_amd64.deb
else
    echo "...Using Chrome from cache"
fi
