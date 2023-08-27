# VoiceAssistantRobot
![header](https://github.com/PonDad/VoiceAssistantRobot/blob/main/image/image_1.jpg)

## ハードウェア
- 本体: [RaspberryPi4 ModelB 4GB](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- パンチルトハット: [Pimoroni Pan-Tilt HAT](https://shop.pimoroni.com/products/pan-tilt-hat?variant=22408353287)
- カラーLEDスティック: [Adafruit NeoPixel Stick 8](https://shop.pimoroni.com/products/neopixel-stick-8-x-5050-rgbw-leds?variant=17436712071)
- 熱対策(オプション) [GeeekPi Fan Hat for Raspberry Pi 4 Model B](https://wiki.52pi.com/index.php?title=EP-0152) 
- 気温・湿度・照度・水分計測（オプション）: [WioNode](https://www.seeedstudio.com/Wio-Node.html)
- USBマイク・USBスピーカー: RaspberryPiで使用可能なものを適宜使用してください

## ソフトウェア
- OS: [Raspberry Pi OS (64-bit)](https://www.raspberrypi.com/software/operating-systems/) / [Raspberry Pi 設定チートシート](https://gist.github.com/PonDad/3415837db6db0ce22352eda8babb7622)
- Python3.9.2: [requirements](https://github.com/PonDad/VoiceAssistantRobot/blob/main/requirements.txt)
- 音声認識: [Vosk](https://pypi.org/project/vosk/) / [vosk-model-small-ja-0.22](https://alphacephei.com/vosk/models)
- 音声発話: [Aques Talk Pi](https://www.a-quest.com/products/aquestalkpi.html) / [AquesTalk Installer](https://github.com/noraworld/aquestalk-installer)
- 画像処理: [OpenCV 64bit 4.5.5](https://opencv.org/releases/) / [Install OpenCV on Raspberry 64 OS](https://qengineering.eu/install-opencv-on-raspberry-64-os.html)
  - 顔認識モデル: [yunet.onnx](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)
  - 顔識別モデル: [face_recognizer_fast.onnx](https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view)
  - 性別識別モデル: [gender_net.caffemodel](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master) / [gender_deploy.prototxt](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master)
  - 年令識別モデル: [age_net.caffemodel](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master) / [age_deploy.prototxt](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master)
  - 物体識別モデル: [frozen_inference_graph.pb](https://www.kaggle.com/code/chienhsianghung/object-detection-using-opencv-inference) / [ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt](https://www.kaggle.com/code/chienhsianghung/object-detection-using-opencv-inference) / [coco.names](https://gist.github.com/tersekmatija/9d00c4683d52d94cf348acae29e8db1a)
- モーター制御・LED制御: [pantilt-hat](https://github.com/pimoroni/pantilt-hat)

> **Note**
> Voskモデルはリンク先よりダウンロードしてください。
>
> AquesTalkPiは利用許諾を確認の上ダウンロードしてください。
>
> OpenCVは`yunet.onnx`を使用する場合、バージョン4.5.4以上が必要です。また4.8以降は別のモデルが必要になります。
>
> Raspberry Pi OSにOpenCVを入れる際、ソースからビルドが必要です。リンク先のサイトに行き、指示に従って進めてください。サイトの運営者がインストール用のスクリプトを提供しているので、そちらを活用してください。
>
> 画像認識用のDNNモデルは各リンク先よりダウンロードしたものです。
>
> リビングの気温・湿度・照度・鉢植えの水分データの取得にはSeeed日本法人が用意した日本のサーバーを使用しています（[日本にWioサーバーを設置しました](https://lab.seeed.co.jp/entry/2022/01/25/120000)）。サーバーのアクセストークンは`.env`ファイルに記述しています。

## 仕組み
![chart1](https://github.com/PonDad/VoiceAssistantRobot/blob/main/image/chart_1.png)

#### 音声発話（ユーザー）
ユーザーの音声発話は、RaspberryPiに接続したUSBマイクから得た音声をPythonのオーディオライブラリPyAudioを使ってストリーミングします。

#### 音声認識（Vosk）
ストリーミングデータを音声認識エンジンVoskを使いテキストに変換します。
 
#### コマンド実行（analyze関数）
独自関数`analize()`により、入力されたテキストが事前に登録されたコマンドと一致するか、条件分岐により振り分けを行います。

実験用に登録した実行コマンドは以下の通りです

- 日時データ取得（`datetime`モジュール）
- WioNodeからのデータ取得(`requests`モジュールを利用したGETメソッド)
- 顔認証・物体認識（OpenCVとDNNモデルを使ったリアルタイム顔認識、物体認識）
- サーボモーター・LEDライト制御（PanTiltHATライブラリを使用）

コマンドの実行と合わせて、ロボットの回答は事前に記述しておきます。

#### 音声合成（Aques Talk Pi）
各コマンドの回答テキストはAques Talk Piを使って音声合成を行います。Pythonの`subprocess`を使い、合成音声されたwavファイルをパイプでつなぎ`aplay`で再生出来るようになっており、記述がシンプルに行えます。

#### 合成音声発話（ロボット）
`aplay`で再生されたwavファイルをスピーカーで再生します。

## 使い方
各ライブラリをインポート後、必要なモデルをダウンロードしディレクトリに配置します。ユーザー情報の登録は
```bash
python bot_face_data_creator.py
```
を実行し、ユーザーID、ユーザー名、興味のあることを登録し、顔認証用の写真を撮影してください。年令・性別は自動で判別されますが、かけ離れている場合は`data/user_data.json`を手動で修正することも可能です。

`data/command_data.json`でウェイクワードを設定できますので、好みのものに変更可能です。同様に終了ワードやコマンドワードも自由に変更できます。

```bash
python main.py
```
で実行してください。`ctrl + c`でウェイクワード待機のループが終了します。
