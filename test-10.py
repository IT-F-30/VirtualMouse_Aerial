import cv2
import mediapipe as mp
import open3d as o3d
import pyautogui
import time

# OBJファイルの読み込み
mesh = o3d.io.read_triangle_mesh("mous.ply")

# 視点を移動する関数
def move_viewpoint(vis, x_rotation, y_rotation, zoom):
    # 視点を移動
    ctr = vis.get_view_control()
    ctr.rotate(x_rotation, y_rotation)
    ctr.scale(zoom)

# エッジを生成
lines = []
for f in mesh.triangles:
    lines.append([f[0], f[1]])
    lines.append([f[1], f[2]])
    lines.append([f[2], f[0]])

edge_lines = o3d.geometry.LineSet()
edge_lines.points = mesh.vertices
edge_lines.lines = o3d.utility.Vector2iVector(lines)

# エッジを表示
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(mesh)
vis.add_geometry(edge_lines)

# 初期の視点設定
x_rotation = 0
y_rotation = 0
zoom = 1

move_viewpoint(vis, x_rotation, y_rotation, zoom)
#vis.destroy_window()

# ビデオファイルをキャプチャ
cap = cv2.VideoCapture(1)

# 手を検出するモデルを作成する
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# 左手と右手の指の位置を保持する変数
prev_finger_positions_left = None
prev_finger_positions_right = None

# フレーム間隔（2倍速）
frame_interval = 2

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

                if landmarks[0][0] < landmarks[9][0]:  # 左手の場合（0番目の指のx座標が9番目の指より小さい）
                    if prev_finger_positions_left is not None:
                        count_left_d = []
                        count_left_c = []
                        for i, (prev, curr) in enumerate(zip(prev_finger_positions_left, landmarks[1:]), start=1):
                            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
                            count_left_d.append([dx,dy])
                            count_left_c.append([curr[0],curr[1]])

                        if abs(count_left_c[3][0] - count_left_c[7][0]) <= 50 and abs(count_left_c[3][1] - count_left_c[7][1]) <= 50:
                            move_viewpoint(vis, -1*count_left_d[7][0], count_left_d[7][1], 0)
                                
                            # イベントループを更新して視点を反映
                            vis.poll_events()
                            vis.update_renderer()
                            time.sleep(0.1) 
                            pyautogui.move(-1*count_left_d[7][0], count_left_d[7][1])
                    prev_finger_positions_left = landmarks[1:]
                else:  # 右手の場合
                    if prev_finger_positions_right is not None:
                        count_right_d = []
                        count_right_c = []
                        for i, (prev, curr) in enumerate(zip(prev_finger_positions_right, landmarks[1:]), start=1):
                            dx, dy = curr[0] - prev[0], curr[1] - prev[1]
                            count_right_d.append([dx,dy])
                            count_right_c.append([curr[0],curr[1]])
                        if abs(count_right_c[3][0] - count_right_c[7][0]) <= 50 and abs(count_right_c[3][1] - count_right_c[7][1]) <= 50:
                            move_viewpoint(vis, -1*count_right_d[7][0], count_right_d[7][1], 0)
                                
                            # イベントループを更新して視点を反映
                            vis.poll_events()
                            vis.update_renderer()
                            time.sleep(0.1)  
                            pyautogui.move(-1*count_right_d[7][0], count_right_d[7][1])
                    prev_finger_positions_right = landmarks[1:]

        cv2.imshow("Video", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):  # スペースキーで再生と停止を切り替え
        playing = not playing

# 解放
cap.release()
cv2.destroyAllWindows()
vis.destroy_window()
