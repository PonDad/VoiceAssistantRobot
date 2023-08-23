# VoiceAssistantBot
![img1]()

## ハードウェア
- 本体: [RaspberryPi4 ModelB 4GB](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
- パンチルトハット: [Pimoroni Pan-Tilt HAT](https://shop.pimoroni.com/products/pan-tilt-hat?variant=22408353287)
- カラーLEDスティック: [Adafruit NeoPixel Stick 8](https://shop.pimoroni.com/products/neopixel-stick-8-x-5050-rgbw-leds?variant=17436712071)
- 熱対策(オプション) [GeeekPi Fan Hat for Raspberry Pi 4 Model B](https://wiki.52pi.com/index.php?title=EP-0152) 

## ソフトウェア
- OS: [Raspberry Pi OS (64-bit)](https://www.raspberrypi.com/software/operating-systems/)
- 音声認識: [Vosk](https://pypi.org/project/vosk/) / [vosk-model-small-ja-0.22](https://alphacephei.com/vosk/models)
- 音声発話: [Aques Talk Pi](https://www.a-quest.com/products/aquestalkpi.html)
- 画像処理: [OpenCV 64bit 4.5.4~](https://qengineering.eu/install-opencv-on-raspberry-64-os.html)
  - 顔認識モデル: [yunet_n_320_320.onnx](https://github.com/ShiqiYu/libfacedetection.train/tree/master/onnx)
  - 顔識別モデル: [face_recognizer_fast.onnx](https://drive.google.com/file/d/1ClK9WiB492c5OZFKveF3XiHCejoOxINW/view)
  - 性別識別モデル: [gender_net.caffemodel](https://github.com/eveningglow/age-and-gender-classification/blob/master/model/gender_net.caffemodel) / [gender_deploy.prototxt](https://github.com/eveningglow/age-and-gender-classification/blob/master/model/deploy_gender2.prototxt)
  - 年令識別モデル: [age_net.caffemodel](https://github.com/eveningglow/age-and-gender-classification/blob/master/model/age_net.caffemodel) / [age_deploy.prototxt](https://github.com/eveningglow/age-and-gender-classification/blob/master/model/deploy_age2.prototxt)
  - 物体識別モデル: [frozen_inference_graph.pb](https://www.dropbox.com/s/ardvflqmwwe8uzl/frozen_inference_graph.pb?dl=1) / [ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt](https://www.dropbox.com/s/dfn0sb43ovb8pr0/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt?dl=1) / [coco.names](https://github.com/pjreddie/darknet/blob/master/data/coco.names)
- モーター制御・LED制御: [pantilthat](https://pypi.org/project/pantilthat/)

## 仕組み
![img2]()

音声発話（ユーザー） --> 音声認識（Vosk） --> テキスト化 --> コマンド実行（analyzeファイル） --> 音声合成（Aques Talk Pi）--> 合成音声発話（ロボット）

## 使い方
必要なモデルをダウンロードし、各ディレクトリに配置します。ユーザー情報の登録は
```bash
python bot_face_data_creator.py
```
を実行し、ユーザーID、ユーザー名、興味のあることを登録し、顔認証用の写真を撮影してください。年令・性別は自動で判別されますがかけ離れている場合は`data/user_data.json`を手動で修正することも可能です。

`data/command_data.json`でウェイクワードを設定できますので、好みのものに変更可能です。同様に終了ワードやコマンドワードも自由に変更できます。

```bash
python main.py
```
で実行してください。
