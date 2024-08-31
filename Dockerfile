# 参考 https://qiita.com/casareal_user/items/f932c32517e0d6118809

FROM --platform=linux/amd64 python:3.11-slim

# wget, curl, unzipをインストール
RUN apt-get update && \
    apt-get install -y wget curl unzip && \
    apt-get -y clean && \
    rm -rf /var/lib/apt/lists/*

# Chromeをインストール
RUN wget "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    apt-get update && \
    dpkg -i ./google-chrome-stable_current_amd64.deb || apt-get install -f -y && \
    rm ./google-chrome-stable_current_amd64.deb && apt-get -y clean && \
    which google-chrome-stable

# ChromeDriverをインストール
RUN apt-get update && apt-get install -y unzip graphviz && \
    CHROME_VERSION=$(google-chrome-stable --version | cut -d" " -f3) && \
    echo "Chrome_Version: ${CHROME_VERSION}" && \
    echo "$(google-chrome-stable --version)" && \
    wget "https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.84/linux64/chromedriver-linux64.zip" &&\
    unzip chromedriver-linux64.zip -d /tmp/ && \
    rm chromedriver-linux64.zip && \
    chown root:root /tmp/chromedriver-linux64/chromedriver && \
    chmod 755 /tmp/chromedriver-linux64/chromedriver && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chromedriver --version || apt-get install -f -y

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピー
COPY ./app/requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# パスを通す
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/chrome

# アプリケーションのソースコードをコピー
COPY ./app .

# 環境変数を.envファイルから読み込む
COPY .env ./

# コンテナ起動時に実行するコマンドを指定
CMD ["python", "app.py"]