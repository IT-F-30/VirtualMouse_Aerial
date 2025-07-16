import open3d as o3d
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

for _ in range(50):
    # 視点を連続的に変更
    move_viewpoint(vis, x_rotation, y_rotation, zoom)
    
    # イベントループを更新して視点を反映
    vis.poll_events()
    vis.update_renderer()

    # 視点を更新
    x_rotation += 10
    y_rotation += 10
    zoom = 1
    time.sleep(0.1)

for _ in range(50):
    # 視点を連続的に変更
    move_viewpoint(vis, x_rotation, y_rotation, zoom)
    
    # イベントループを更新して視点を反映
    vis.poll_events()
    vis.update_renderer()

    # 視点を更新
    x_rotation = 0
    y_rotation += 10
    zoom = 1
    time.sleep(0.1)  

vis.destroy_window()
