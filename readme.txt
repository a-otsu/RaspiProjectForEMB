配布する各ファイルについて説明します。
-config.yaml
    使用するユーザーの選択をはじめとする各種設定を行うファイルです。

-Python(.py)ファイル
    --post_sensor_data.py
        Arduinoにコマンドを送ってセンサーデータを取得します。
        さらに、そのデータをデータベースに登録します。

    --send_images.py
        カメラで画像を撮影し、指定したフォルダに保存します。
        さらに、保存した画像をサーバーにアップロードします。
        コンフィグでアップロード後にラズパイに保存されている画像を削除することができます。
        長期間稼働させる場合にはこの設定をしておくとよいかもしれません。

-run_scripts.sh
    一連の動作を自動で実行するシェルスクリプト

実行にあたっては以下のpythonパッケージがインストールされていることを確認してください。
pyserial (import serial)シリアル通信用
requests (import requests)httpリクエストの送信用
pyyaml (import yaml)設定ファイル(config.yaml)の読み込み用
cv2

コマンド(pip show "パッケージ名")でインストール状況の確認が行えます。
インストールされていない場合以下のコマンドを実行してください。
sudo pip install pyserial --break-system-packages
sudo pip install requests --break-system-packages
sudo pip install pyyaml --break-system-packages
sudo pip3 install opencv-python --break-system-packages --user pycoingecko

pipもない場合は次のコマンドを実行
sudo apt install pip
