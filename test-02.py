import cv2
import mediapipe as mp

# カメラからビデオキャプチャを開始
cap = cv2.VideoCapture(1)

# 手を検出するモデルを作成する
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

#ファイルに書き込み
f = open('test.txt', 'w')

# 前のフレームの指の位置を保持する変数
prev_finger_positions = None

while True:
    success, img = cap.read()

    if not success:
        print("カメラからのビデオキャプチャに失敗しました。")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # モデルで手を検出する
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:  # 手が検出された場合
        for hand_lms in results.multi_hand_landmarks:
            landmarks = []
            for landmark in hand_lms.landmark:
                # 手のランドマークの座標を画像のサイズにスケーリングして保存
                h, w, _ = img.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                landmarks.append((x, y))

            # 現在のフレームの指の位置を描画
            for i, landmark in enumerate(landmarks[1:]):  # 最初の指を除外
                cv2.circle(img, landmark, 5, (255, 0, 0), -1)  # 指の位置を円で可視化

            # 前のフレームの指の位置が存在する場合、指の移動量を計算して可視化
            if prev_finger_positions is not None:
                for i, (prev, curr) in enumerate(zip(prev_finger_positions, landmarks[1:]), start=1):
                    dx, dy = curr[0] - prev[0], curr[1] - prev[1]
                    print(img, f'Finger {i}: ({dx}, {dy})', (10, 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    f.write(str(img, f'Finger {i}: ({dx}, {dy})', (10, 30 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA))

            # 現在のフレームの指の位置を前のフレームの位置として保存
            prev_finger_positions = landmarks[1:]

    cv2.imshow("Live Video", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
f.close()