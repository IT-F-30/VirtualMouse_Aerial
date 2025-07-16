import open3d as o3d

x_rotation = float(0)
y_rotation = float(0)
zoom = float(0)

# OBJファイルの読み込み
mesh = o3d.io.read_triangle_mesh("dog.obj")

# メッシュを表示
o3d.visualization.draw_geometries([mesh],mesh_show_back_face=True)

# 視点を移動する関数
def move_viewpoint(x_rotation, y_rotation, zoom):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    render_option = vis.get_render_option()
    render_option.load_from_json("renderoption.json")  # レンダリングオプションの設定ファイルを読み込む

    # 視点を移動
    ctr = vis.get_view_control()
    ctr.rotate(x_rotation, y_rotation)
    ctr.scale(zoom)
    vis.run()


# 数値入力に基づいて視点を移動
for _ in range(100):
    x_rotation = 0
    y_rotation += 100
    zoom = 0
    
    move_viewpoint(x_rotation, y_rotation, zoom)