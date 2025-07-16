import cv2
import mediapipe as mp
import pyautogui

# ビデオファイルのパスを指定します
video_file_path = 'IMG_1633.MOV'

# ビデオファイルをキャプチャ
cap = cv2.VideoCapture(2)

# 手を検出するモデルを作成する
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# 左手と右手の指の位置を保持する変数
prev_finger_positions_left = None
prev_finger_positions_right = None

# フレーム間隔（2倍速）
frame_interval = 2

# 文字列
s = [
    [0, 0, 160],[0, 0, 190], [0, 0, 220], [0, 0, 250], [160, 0, 160], [190, 0, 190],
    [222, 0, 220], [250, 0, 250], [0, 160, 160], [0, 190, 190], [0, 220, 220],
    [0, 250, 250], [0, 160, 0], [0, 190, 0], [0, 220, 0], [0, 250, 0],
    [160, 160, 0], [190, 190, 0], [220, 220, 0], [250, 250, 0]
]
# Define finger and hand labels as regular lists of strings
f = ["親指:第四","親指:第三","親指:第二","親指:第一","人指:第四","人指:第三","人指:第二","人指:第一","中指:第四","中指:第三","中指:第二","中指:第一","薬指:第四","薬指:第三","薬指:第二","薬指:第一","小指:第四","小指:第三","小指:第二","小指:第一"]


# ビデオの再生状態を管理する変数
playing = True

while True:
    if playing:
        # フレーム間隔ごとにビデオフレームを読み取る
        for _ in range(frame_interval - 1):
            cap.read()
        success, img = cap.read()

        if not success:
            print("ビデオファイルの読み取りに失敗しました。")
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 手を検出
        results = mp_hands.Hands().process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                landmarks = []
                for landmark in hand_lms.landmark:
                    h, w, _ = img.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    landmarks.append((x, y))

                for i, landmark in enumerate(landmarks[1:]):
                    cv2.circle(img, landmark, 15, s[i], -1)  # すべての指に青い点を描画

                if landmarks[0][0] < landmarks[9][0]:  # 左手の場合（0番目の指のx座標が9番目の指より小さい）
                    if prev_finger_positions_left is not None:
                        for i, (prev, curr) in enumerate(zip(prev_finger_positions_left, landmarks[1:]), start=1):
                            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
                            if i == 8:
                                pyautogui.moveTo(curr[0]*2, curr[1]*2)
                            else:
                                print('左手 Finger', f[i-1],':' ,(dx, dy), (curr[0], curr[1]))
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    prev_finger_positions_left = landmarks[1:]
                else:  # 右手の場合
                    if prev_finger_positions_right is not None:
                        for i, (prev, curr) in enumerate(zip(prev_finger_positions_right, landmarks[1:]), start=1):
                            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
                            if i == 8:
                                pyautogui.moveTo(curr[0]*2, curr[1]*2)
                            else:
                                print('左手 Finger', f[i-1],':' ,(dx, dy), (curr[0], curr[1]))
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    prev_finger_positions_right = landmarks[1:]

        # 指定座標に点を描画
        #cv2.circle(img,(1003, 1079), 15, (255, 255, 255), -1)
        #cv2.circle(img,(1013, 941), 15, (200,200,200), -1)
        #cv2.circle(img,(995, 844), 15, (100,100,100), -1)
        #cv2.circle(img,(996, 777), 15, (50,50,50), -1)

        cv2.imshow("Video", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):  # スペースキーで再生と停止を切り替え
        playing = not playing

# 解放
cap.release()
cv2.destroyAllWindows()
