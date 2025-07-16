import cv2
import mediapipe as mp

# カメラデバイスの選択
camera_device_index = 2  # 0番目のカメラを使用しますが、必要に応じて他の値に変更できます

cap = cv2.VideoCapture(camera_device_index)

# 手を検出するモデルを作成する
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

while True:
    success, img = cap.read()

    if not success:
        print("カメラからのフレームの読み取りに失敗しました。")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # モデルで手を検出する
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:  # 手が検出された場合
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)  # 手のランドマークを描画する

    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
