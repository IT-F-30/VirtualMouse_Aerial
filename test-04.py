import os
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

# .objファイルを読み込む関数
def load_obj(file_name):
    vertices = []
    faces = []

    with open(file_name, "r", encoding="utf-8") as obj_file:
        for line in obj_file:
            if line.startswith("v "):
                vertices.append(list(map(float, line[2:].split())))
            elif line.startswith("f "):
                faces.append([list(map(int, face.split("/"))) for face in line[2:].split()])

    return vertices, faces

# グラフィックス設定
def set_graphics():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glMaterial(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 1.0, 1.0))  # マテリアルの色を設定

# 3Dモデルの表示
def display(vertices, faces, x_translate, y_translate, rotate_x, rotate_y):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glTranslatef(0.0, 0.0, -5.0)
    glTranslatef(x_translate, y_translate, 0.0)  # X.Y座標の移動
    glRotatef(rotate_x, 1, 0, 0)  # X軸の回転
    glRotatef(rotate_y, 0, 1, 0)  # Y軸の回転
    
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex[0] - 1])
    glEnd()
    
    pygame.display.flip()

# メイン関数
def main():
    global x_translate, y_translate, rotate_x, rotate_y
    x_translate = 0
    y_translate = 0
    rotate_x = 0
    rotate_y = 0
    
    pygame.init()
    display_mode = (800, 600)
    pygame.display.set_mode(display_mode, DOUBLEBUF | OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display_mode[0] / display_mode[1]), 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # .obj ファイルを読み込み（ファイルパスを変更）
    vertices, faces = load_obj(r"c:\Users\Vreba\googleDrive\Program\Gescher\マウス.obj")  # .objファイルのパスを指定
    
    set_graphics()  # グラフィックス設定を追加
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 数値を逐一入力してモデルを調整
        ws = float(input("WS: "))
        ad = float(input("AD: "))
        up_down_angle = float(input("上下角: "))
        left_right_angle = float(input("左右角: "))
        x_translate += ws
        y_translate += ad
        rotate_x += up_down_angle
        rotate_y += left_right_angle
        
        display(vertices, faces, x_translate, y_translate, rotate_x, rotate_y)

if __name__ == "__main__":
    main()
