import open3d as o3d
import numpy as np

# PLYファイルの読み込み
pcd = o3d.io.read_point_cloud("mous.ply")

# 初期座標
initial_translation = np.array([0.0, 0.0, 0.0])

# 3Dビューアの初期化
o3d.visualization.draw_geometries([pcd])

while True:
    try:
        # 移動量を入力
        translation_x = float(input("X方向の移動量を入力 (0で終了): "))
        if translation_x == 0:
            break
        translation_y = float(input("Y方向の移動量を入力 (0で終了): "))
        if translation_y == 0:
            break
        translation_z = float(input("Z方向の移動量を入力 (0で終了): "))
        if translation_z == 0:
            break

        # 移動ベクトルを計算
        translation = np.array([translation_x, translation_y, translation_z])

        # 点群を移動
        pcd.translate(translation - initial_translation)
        initial_translation = translation

        # 移動後の点群を再描画
        o3d.visualization.draw_geometries([pcd])
    except ValueError:
        print("数値を入力してください。")
