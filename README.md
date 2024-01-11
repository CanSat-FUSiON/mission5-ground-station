# FUSiON-OBC地上局

## 使い方
サーバーをWSL2で動かし，USBのCOMポート関連のクライアントをWindowsのローカルで動かす．

### 環境構築
1. Dockerをインストール
https://qiita.com/ryotaro76/items/305d4d61dfd82e3f2bfa
1. WSL2上にこのリポジトリをクローン
1. Windows上にこのリポジトリをクローン
### 起動
1. (サーバーの起動) WSL2上で以下のコマンドを実行
    ```
    mission5-ground-station$ docker-compose up -d
    ```
1. (地上局テレメ画面の起動) Windows上で`http://localhost:8085/dashboards`にアクセス
    
    今のところユーザー名はadminでパスワードもadmin
1. (地上局コマンド画面の起動) Windows上で以下のコマンドを実行
    ```
    mission5-ground-station$ python3 esp32_client.py
    ```
### 終了
1. WSL2上で以下のコマンドを実行
    ```
    mission5-ground-station$ docker-compose down
    ```
1. Windows上でCtrl+Cを押す

## ファイル・ディレクトリ構成
- docker : Dockerのvolume用フォルダ  
- compose.yml : Dockerのコンテナ設定ファイル 
- esp32_client.py : ESP32からJSONを受信し，コマンドを送信するプログラム
- write_db.py : esp32_client.pyから受信したJSONをDBに書き込むプログラム
