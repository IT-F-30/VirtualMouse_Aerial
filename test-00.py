import cv2
import mediapipe as mp

# 画像ファイルのパスを指定します
image_file_path = '/Users/vreba/Library/CloudStorage/GoogleDrive-jarodbruce414@gmail.com/マイドライブ/Program/Gescher/te.JPG'  # 画像ファイルのパスを指定します

# 画像ファイルを読み込む
img = cv2.imread(image_file_path)

# 手を検出するモデルを作成する
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# 前のフレームの指の位置を保持する変数
prev_finger_positions = None
if img is not None:
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # モデルで手を検出する
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:  # 手が検出された場合
        for hand_lms in results.multi_hand_landmarks:
            landmarks = []
            for landmark in hand_lms.landmark:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                # 手のランドマークの座標を画像のサイズにスケーリングして保存
                h, w, _ = img.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                landmarks.append((x, y))

            # 現在のフレームの指の位置を描画
            for i, landmark in enumerate(landmarks[::]):  # 最初の指を除外
                cv2.circle(img, landmark, 40, (0, 0, 255), -100)  # 指の位置を円で可視化

    cv2.imshow("Image", img)

    # 画像を保存
    output_image_path = '/Users/vreba/Library/CloudStorage/GoogleDrive-jarodbruce414@gmail.com/マイドライブ/Program/Gescher/output_image.jpg'
    cv2.imwrite(output_image_path, img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"出力画像を {output_image_path} に保存しました。")
else:
    print("画像ファイルの読み取りに失敗しました。")
