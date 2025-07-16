import open3d as o3d

# OBJファイルのパスを指定
obj_file_path = "mous.ply"

# OBJファイルを読み込む
mesh = o3d.io.read_triangle_mesh(obj_file_path)

# 3Dビューアを作成して、OBJファイルを表示
o3d.visualization.draw_geometries([mesh],mesh_show_back_face=True)
