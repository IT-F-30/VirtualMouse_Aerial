import cv2
import mediapipe as mp
import mous_rs
from config import (
    CLICK_THRESHOLD,
    MOUSE_SENSITIVITY,
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    MAX_NUM_HANDS,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    INDEX_FINGER_TIP,
    THUMB_TIP,
    MIDDLE_FINGER_TIP,
    DEBUG_MODE,
    SHOW_FPS
)
import time

# Webカメラから入力を開始
cap = cv2.VideoCapture(CAMERA_INDEX)

# MediaPipeの手の検出モデルを初期化
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=MAX_NUM_HANDS,
    min_detection_confidence=MIN_DETECTION_CONFIDENCE,
    min_tracking_confidence=MIN_TRACKING_CONFIDENCE
)
mp_draw = mp.solutions.drawing_utils

# 前のフレームの手のランドマーク位置を保存する変数
prev_landmarks = None

# FPS計測用
prev_time = 0
click_cooldown = 0  # クリック連打防止用のクールダウン

def process_hand(current_landmarks, prev_landmarks, current_time):
    """
    手のランドマークを処理し、マウス操作を実行する関数
    
    Args:
        current_landmarks: 現在のフレームのランドマーク座標リスト
        prev_landmarks: 前のフレームのランドマーク座標リスト
        current_time: 現在の時刻
    """
    global click_cooldown
    
    if prev_landmarks is None:
        return
    
    # 人差し指の移動量を計算
    index_finger_current = current_landmarks[INDEX_FINGER_TIP]
    index_finger_prev = prev_landmarks[INDEX_FINGER_TIP]
    
    dx = index_finger_current[0] - index_finger_prev[0]
    dy = index_finger_current[1] - index_finger_prev[1]
    
    # マウスを移動（映像が左右反転しているので、x軸はそのまま、y軸はそのまま）
    mous_rs.rsmove(int(dx * MOUSE_SENSITIVITY), int(dy * MOUSE_SENSITIVITY))
    
    # クリック判定：親指と中指が近づいているかチェック（クールダウン付き）
    if current_time > click_cooldown:
        thumb = current_landmarks[THUMB_TIP]
        middle_finger = current_landmarks[MIDDLE_FINGER_TIP]
        
        distance = ((thumb[0] - middle_finger[0]) ** 2 + (thumb[1] - middle_finger[1]) ** 2) ** 0.5
        
        if distance <= CLICK_THRESHOLD:
            if DEBUG_MODE:
                print(f"Click detected (distance: {distance:.2f})")
            mous_rs.rsclick()
            click_cooldown = current_time + 0.3  # 300ms のクールダウン

while True:
    success, img = cap.read()
    if not success:
        print("ビデオフレームの読み込みに失敗しました。")
        break

    # 左右反転して画像を小さくする
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (CAMERA_WIDTH, CAMERA_HEIGHT))

    # RGB変換して手を検出
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # FPS計算
    current_time = time.time()
    if SHOW_FPS:
        fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
        prev_time = current_time
        cv2.putText(img, f"FPS: {int(fps)}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if results.multi_hand_landmarks:
        # 最初の手のみ処理
        hand_lms = results.multi_hand_landmarks[0]
        
        # ランドマークを描画
        mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
        
        # ランドマーク座標を取得
        h, w, _ = img.shape
        landmarks = [(int(lm.x * w), int(lm.y * h), lm.z) for lm in hand_lms.landmark]
        
        # マウス操作を処理
        process_hand(landmarks, prev_landmarks, current_time)
        prev_landmarks = landmarks
    else:
        # 手が検出されない場合は前のランドマークをクリア
        prev_landmarks = None

    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
