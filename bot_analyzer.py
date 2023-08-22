'''
bot_analyzer.py

音声認識で受け取ったコマンドを解析し、適切な応答を行う解析プログラムです。
ボイスアシスタントロボットの機能を制御するため、顔認識、時刻取得、モーター制御などの関数を呼び出します。
'''

from pathlib import Path
import json, datetime
from bot_face_track_recognizer import face_recognize
from bot_object_detecter import object_detection
from bot_wio_node import get_wio
from bot_motor_controller import pan_tilt_slow, neopixels_face, neopixels_off

# Jsonファイルからコマンドの配列を読み込む
with open(Path("data/command_data.json"), "rb") as f:
    data = json.load(f)

COMMAND = data["command"]

# コマンドを解析して適切な応答を行う関数
def analyze(user_input):
    try:
        for word, phrases in COMMAND.items():
            command = "unknown"  # 初期値を "unknown" に設定
            for phrase in phrases:
                if user_input in phrase:
                    command = word
                    break  # 一致した場合にループを終了
            if command != "unknown":
                break  # コマンドが一致した場合に外側のループも終了

        if command == "unknown":
            robot_reply =  "ごめんなさいよく分かりません"

        elif command == "greeting":
            robot_reply = "ゆっくり霊夢です ゆっくりしていってね"

        elif command == "day_now":
            # 現在時刻を取得して合成音声で出力
            day_now = datetime.datetime.today().strftime("%-Y年%-m月%-d日")
            robot_reply = "今日の日付は" + day_now + "です"

        elif command == "time_now":
            # 現在時刻を取得して合成音声で出力
            time_now = datetime.datetime.now().strftime("%-H時%-M分")
            robot_reply = "現在時刻は" + time_now + "です"

        elif command == "room_data":
            room_data = get_wio()
            robot_reply = "リビングの 気温は" + str(room_data[0]) + "度 湿度は" + str(room_data[1]) + "% 不快指数は" + str(room_data[2]) + " 明るさは" + str(room_data[3]) + "ルクス です"

        elif command == "pachira_data":
            room_data = get_wio()
            robot_reply = "パキラの水分は" + str(room_data[4]) + "% です"
        
        elif command == "user_info":
            # ユーザーIDをjsonファイルから読み込む
            with open(Path("data/user_data.json")) as file:
                load_user = json.load(file)
            
            # 顔認識を行いユーザー名を取得
            recognized_id = face_recognize()
            print("🖥️ SYSTEM: recognized_id: " + recognized_id )

            if recognized_id in load_user:
                user_name = load_user[recognized_id]["name"]
                user_category = load_user[recognized_id]["category"]
            else:
                recognized_id = "unknown"
                user_name = "ゲスト"
                user_category = "unknown"

            robot_reply = "ユーザーIDは" + str(recognized_id) + "ユーザーネームは" + str(user_name), "ユーザーカテゴリーは" + str(user_category) + "です"

        elif command == "look_around":
            # cocoデータセットの英語-日本語翻訳をjsonファイルから読み込む
            with open(Path("dnn_models/coco_en_ja.json")) as file:
                translation_dict = json.load(file)
            recognized_obj = object_detection()
            translated_words = [translation_dict.get(word, word) for word in recognized_obj]
            result_array = []
            for word in translated_words:
                result_array.append(word)
            robot_reply = "以下のものがみえます " + " ".join(str(item) for item in result_array) 

        elif command == "turn_right":
            neopixels_off()
            neopixels_face()
            pan_tilt_slow(-60, 0, 10)
            pan_tilt_slow(0, 0, 10)
            robot_reply = "はい 右を向きました"

        elif command == "turn_left":
            neopixels_off()
            neopixels_face()
            pan_tilt_slow(60, 0, 10)
            pan_tilt_slow(0, 0, 10)
            robot_reply = "はい 左を向きました"

        elif command == "look_up":
            neopixels_off()
            neopixels_face()
            pan_tilt_slow(0, -60, 10)
            pan_tilt_slow(0, 0 ,10)
            robot_reply = "はい 上を向きました"

        elif command == "look_down":
            neopixels_off()
            neopixels_face()
            pan_tilt_slow(0, 60, 10)
            pan_tilt_slow(0, 0, 10)
            robot_reply = "はい 下を向きました"

        elif command == "exit":
            robot_reply = "会話を終了しました"

        else:
            pass

        return robot_reply

    except TypeError:
        pass

if __name__ == "__main__":
    analyze("look_around")
    