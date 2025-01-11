# #!/usr/bin/env bash
# # Chrome のインストール
# curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt-get update
# sudo apt-get install -y ./google-chrome-stable_current_amd64.deb
# rm google-chrome-stable_current_amd64.deb

#!/usr/bin/env bash
# Chrome のインストール
curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update
apt-get install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
