# FUSiON-OBC地上局

## 使い方
サーバーをDocker(WindowsのDocker Desktopで，内部のエンジンはWSL2)で動かし，USBのCOMポート関連のクライアントをWindowsのローカルで動かす．

(以下2つのQiita記事も参考にしていただけますと幸いです。Issues/Pull eequestes/記事へのコメント等でご指摘等いただけますと幸いです。)

- [Grafana + InfluxDBでリアルタイム可視化しよう！【とりあえずやってみる】](https://qiita.com/Attitudecontro3/items/79382643fdec8fe19ad7)
- [Grafana + InfluxDBでリアルタイム可視化しよう！【自分好みに作りたい】](https://qiita.com/Attitudecontro3/items/9b30a47ec5ac9dc62d8b)

### 環境構築
1. Dockerをインストール
    https://qiita.com/ryotaro76/items/305d4d61dfd82e3f2bfa
1. Windows上にこのリポジトリをクローン
1. 以下のコマンドを実行
    ```
    $ pip install pyserial
    $ pip install influxdb-client
    ```
### 起動
1. (サーバーの起動) 以下のコマンドを実行
    ```
    mission5-ground-station$ docker compose up -d
    ```
1. (地上局テレメ画面の起動) `http://localhost:8085/dashboards`にアクセス
    
    今のところユーザー名はadminでパスワードもadmin
1. (地上局コマンド画面の起動) 以下のコマンドを実行
    ```
    mission5-ground-station/client$ python3 esp32_client.py
    ```
### 終了
1. `esp32_client.py`を実行しているターミナルでCtrl+Cを押す
1. 以下のコマンドを実行
    ```
    mission5-ground-station$ docker compose down
    ```

## ファイル・ディレクトリ構成
- docker : Dockerのvolume用フォルダ  
- compose.yml : Dockerのコンテナ設定ファイル 
- client : InfluxDBにデータをアップロードするクライアントプログラム
    - write_db.py : ***_client.pyから受信したJSONをDBに書き込むプログラム
    - esp32_client.py : ESP32からJSONを受信し，コマンドを送信するプログラム
    - dummy_client.py : dummy.jsonを読み込むプログラム
    - debug_rand_dummy_client.py : Debug用
    - rand_dummy_client.py : ランダムなテレメトリ値を持つJSONをDBに書き込むプログラム
    - create_json.py : ランダムなテレメトリ値を持つJSONを作成するプログラム
