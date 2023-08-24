# VoiceAssistantBot
![img1](https://github.com/PonDad/VoiceAssistantBot/blob/main/image/vagpt1.JPG)

## 仕組み
![img2](https://github.com/PonDad/VoiceAssistantBot/blob/main/image/chart_1.png)

音声発話（ユーザー） --> 音声認識（Vosk） --> テキスト化 --> コマンド実行（`analyze`関数） --> 音声合成（Aques Talk Pi）--> 合成音声発話（ロボット）

の様に動作します。各コマンドは登録されたワードに一致すれば実行、という処理になります。

## ハードウェア
- 本体: [RaspberryPi4 ModelB 4GB](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- パンチルトハット: [Pimoroni Pan-Tilt HAT](https://shop.pimoroni.com/products/pan-tilt-hat?variant=22408353287)
- カラーLEDスティック: [Adafruit NeoPixel Stick 8](https://shop.pimoroni.com/products/neopixel-stick-8-x-5050-rgbw-leds?variant=17436712071)
- 熱対策(オプション) [GeeekPi Fan Hat for Raspberry Pi 4 Model B](https://wiki.52pi.com/index.php?title=EP-0152) 
- 気温・湿度・照度・水分計測（オプション）: [WioNode](https://www.seeedstudio.com/Wio-Node.html)

## ソフトウェア
- OS: [Raspberry Pi OS (64-bit)](https://www.raspberrypi.com/software/operating-systems/)
- Python3.9.2: [requirements](https://github.com/PonDad/VoiceAssistantBot/blob/main/requirements.txt)
- 音声認識: [Vosk](https://pypi.org/project/vosk/) / [vosk-model-small-ja-0.22](https://alphacephei.com/vosk/models)
- 音声発話: [Aques Talk Pi](https://www.a-quest.com/products/aquestalkpi.html) / [AquesTalk Installer](https://github.com/noraworld/aquestalk-installer)
- 画像処理: [OpenCV 64bit 4.5.5](https://opencv.org/releases/) / [Install OpenCV on Raspberry 64 OS](https://qengineering.eu/install-opencv-on-raspberry-64-os.html)
  - 顔認識モデル: [yunet.onnx](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)
  - 顔識別モデル: [face_recognizer_fast.onnx](https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view)
  - 性別識別モデル: [gender_net.caffemodel](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master) / [gender_deploy.prototxt](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master)
  - 年令識別モデル: [age_net.caffemodel](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master) / [age_deploy.prototxt](https://github.com/smahesh29/Gender-and-Age-Detection/tree/master)
  - 物体識別モデル: [frozen_inference_graph.pb](https://www.kaggle.com/code/chienhsianghung/object-detection-using-opencv-inference) / [ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt](https://www.kaggle.com/code/chienhsianghung/object-detection-using-opencv-inference) / [coco.names](https://www.kaggle.com/code/chienhsianghung/object-detection-using-opencv-inference)
- モーター制御・LED制御: [pantilt-hat](https://github.com/pimoroni/pantilt-hat)

> **Note**
> Voskモデルはリンク先よりダウンロードしてください。
>
> AquesTalkPiは利用許諾を確認の上ダウンロードしてください。
>
> OpenCVは`yunet.onnx`を使用する場合、バージョン4.5.4以上が必要です。また4.8以降は別のモデルが必要になります。
>
> Raspberry Pi OSにOpenCVを入れる際、ソースからビルドしなければなりません。リンクからサイトに行き手順通りおこなってください。サイトの運営の方がインストール用のスクリプトをつくってくれていますので活用してください。
>
> 画像認識用のDNNモデルは各リンク先よりダウンロードしたものです。
>
> リビングの気温・湿度・照度・鉢植えの水分は日本のサーバーをSeeed日本法人が用意してくれたので（[日本にWioサーバーを設置しました](https://lab.seeed.co.jp/entry/2022/01/25/120000)）そちらを利用しています。サーバーのアクセストークンは`.env`に記載しています。

## 使い方
各ライブラリをインポート後、必要なモデルをダウンロードしディレクトリに配置します。ユーザー情報の登録は
```bash
python bot_face_data_creator.py
```
を実行し、ユーザーID、ユーザー名、興味のあることを登録し、顔認証用の写真を撮影してください。年令・性別は自動で判別されますがかけ離れている場合は`data/user_data.json`を手動で修正することも可能です。

`data/command_data.json`でウェイクワードを設定できますので、好みのものに変更可能です。同様に終了ワードやコマンドワードも自由に変更できます。

```bash
python main.py
```
で実行してください。
