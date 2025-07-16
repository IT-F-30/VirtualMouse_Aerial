import cv2
import mediapipe as mp

kando = 10
bai_a = 0.5

# Webカメラから入力を開始
cap = cv2.VideoCapture(1)

# MediaPipeの手の検出モデルを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# 前のフレームの手のランドマーク位置を保存する変数
prev_finger_positions_left = None
prev_finger_positions_right = None

def process_hand(landmarks, prev_finger_positions):
    """
    手のランドマークを処理し、マウス操作やz軸情報を出力する関数
    """
    if prev_finger_positions is None:
        return

    count_d = []
    count_c = []
    for prev, curr in zip(prev_finger_positions, landmarks[1:]):
        dx, dy = curr[0] - prev[0], curr[1] - prev[1]
        count_d.append((dx, dy))
        count_c.append(curr)

    # 移動量の平均を計算
    if not count_d:
        return
    
    print(landmarks[0])

    dx_ave = sum(d[0] for d in count_d) / len(count_d)
    dy_ave = sum(d[1] for d in count_d) / len(count_d)

    # マウスカーソルを移動
    print(f"py.move {-1 * dx_ave * bai_a}, {dy_ave * bai_a}")

    # # z座標のリストと平均
    # z_list = [lm[2] for lm in landmarks]
    # z_ave = sum(z_list) / len(z_list)
    # print(f"z_ave: {z_ave:.4f}")

    # 指の距離に基づいてクリック操作を判定
    # count_cの要素は(x, y, z)
    is_middle_finger_click = abs(count_c[3][0] - count_c[11][0]) <= kando and abs(count_c[3][1] - count_c[11][1]) <= kando
    is_ring_finger_click = abs(count_c[3][0] - count_c[15][0]) <= kando and abs(count_c[3][1] - count_c[15][1]) <= kando

    if is_middle_finger_click and is_ring_finger_click:
        print("py.doubleClick")
    elif is_middle_finger_click:
        print("py.click")
    elif is_ring_finger_click:
        print("py.rightClick")

while True:
    success, img = cap.read()
    if not success:
        print("ビデオフレームの読み込みに失敗しました。")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for hand_lms, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            landmarks = []
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

            for landmark in hand_lms.landmark:
                h, w, _ = img.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                z = landmark.z
                landmarks.append((x, y, z))

            # hand_info.classification[0].label を使って左右の手を判断
            hand_label = hand_info.classification[0].label
            if hand_label == "Left":
                process_hand(landmarks, prev_finger_positions_left)
                prev_finger_positions_left = landmarks[1:]
            elif hand_label == "Right":
                process_hand(landmarks, prev_finger_positions_right)
                prev_finger_positions_right = landmarks[1:]

    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()