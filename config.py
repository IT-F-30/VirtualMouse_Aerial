"""
Virtual Mouse 設定ファイル
"""

# マウス操作の設定
CLICK_THRESHOLD = 10  # クリック判定の閾値（ピクセル）
MOUSE_SENSITIVITY = 10  # マウス感度（値が大きいほど敏感）

# カメラの設定
CAMERA_INDEX = 0  # 使用するカメラのインデックス
CAMERA_WIDTH = 640  # カメラ映像の幅
CAMERA_HEIGHT = 360  # カメラ映像の高さ

# MediaPipeの設定
MAX_NUM_HANDS = 1  # 検出する手の最大数
MIN_DETECTION_CONFIDENCE = 0.7  # 検出信頼度の閾値
MIN_TRACKING_CONFIDENCE = 0.5  # トラッキング信頼度の閾値

# 手のランドマークインデックス
THUMB_TIP = 4  # 親指の先端
INDEX_FINGER_TIP = 8  # 人差し指の先端
MIDDLE_FINGER_TIP = 12  # 中指の先端
RING_FINGER_TIP = 16  # 薬指の先端
PINKY_TIP = 20  # 小指の先端

# デバッグ設定
DEBUG_MODE = False  # デバッグモード（Trueで詳細なログを出力）
SHOW_FPS = False  # FPSを表示するか
