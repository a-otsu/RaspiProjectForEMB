---
marp: false
---

# 環境計測基板用のRaspberry Pi セットアップガイド

## 配布ファイルについて
- **Python(.py)**
  - send_data.py
    Arduinoにコマンドを送ってセンサーデータを受け取り、サーバーにアップロードするプログラムです。
  - send_images.py
    カメラを使って画像を撮影し、サーバーにアップロードするプログラムです。

- **シェルスクリプト(.sh)**
  - run_scripts.sh
    Pythonファイルを適切なタイミングで実行するためのシェルスクリプトです。

- **コンフィグファイル(.yaml)**
  - config.yaml
    各種設定を行うことができます。
    設定項目はyamlファイルにコメントで残しているのでそちらを見てください。

- **.service**
  - script_sequence.service
    シェルスクリプトを起動時に実行できるようにする設定ファイルです。
## Pythonモジュールのインストール
実行には以下のモジュールが必要です。
- pyserial
    Arduinoとのシリアル通信に使います。
- requests
    サーバーへのHTTPリクエストに使います。
- pyyaml
    コンフィグファイルの読み込みに使います。
- cv2
    カメラでの画像撮影に使います。

インストールするにはターミナルで次のコマンド群を実行してください。
一部依存関係があるので上から順に実行するのが無難です。
```bash
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo pip3 install opencv-python --break-system-packages
sudo pip install pyserial --break-system-packages
sudo pip install requests --break-system-packages
sudo pip install pyyaml --break-system-packages
```
Raspberry Pi OSのセットアップによってはpipがインストールされていない場合があるようです。この場合は次のコマンドを実行してからパッケージをインストールしてください。
```bash
sudo apt install pip
```

## 自動実行設定
systemctlのタイマーを使って起動時に自動で実行されるようにします。
`/etc/systemd/system`に次のファイルを配置してください。

"script_sequence.service"
```INI
[UNIT]
Description=アップロード処理
After=network-online.target
Wants=network-online.target

[Service]
;このシェルスクリプトのパスはユーザー名などの影響で
;人によって異なる場合があるので確認して変更してください。
ExecStart=/home/pi/run_scripts.sh 
Type=oneshot
;あなたのRaspberry Pi のユーザー名に変更してください。
User=pi
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

追加後は次のコマンドを実行してサービスを有効化してください
```bash
sudo systemctl enable script_sequence.service
```

## UART通信の有効化
シリアル通信にUARTピンを使う場合、デフォルトの設定では無効化されていることが多いので有効化する必要があります。
USBを使って通信する場合には必要ありませんが、ハード的な都合でUART通信を採用しています。
### GUIで設定する場合
1. 「スタートメニュー」-「設定」-「Raspberry Piの設定」を開く
2. 「インターフェイス」タブの「シリアルポート」を有効化
    「シリアルコンソール」を無効化

