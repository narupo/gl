import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
import random
import math
# https://www.youtube.com/watch?v=fJFb28y8drM
# https://gist.github.com/krzygorz/bd5c7fc5bfa5b50c6cbd

class GLFrame(OpenGLFrame):
    def initgl(self):
        self.vertices = [
            [-0.5, -0.5, -0.5],  # 0
            [0.5, -0.5, -0.5],  # 1
            [0.5, 0.5, -0.5],  # 2
            [-0.5, 0.5, -0.5],  # 3
            [-0.5, -0.5, 0.5],  # 4
            [0.5, -0.5, 0.5],  # 5
            [0.5, 0.5, 0.5],  # 6
            [-0.5, 0.5, 0.5],  # 7
        ]
        self.faces = [
            [4, 5, 6, 7],
            [0, 3, 2, 1],
            [5, 1, 2, 6],
            [0, 4, 7, 3],
            [7, 6, 2, 3],
            [0, 1, 5, 4],
        ]
        self.normals = [
          [0.0, 0.0, 1.0],
          [0.0, 0.0, -1.0],
          [1.0, 0.0, 0.0],
          [-1.0, 0.0, 0.0],
          [0.0, 1.0, 0.0],
          [0.0, -1.0, 0.],
        ]
        self.camera = [0.0, 1.0, 0.0]
        self.v = [0.0, 0.0, 0.0]
        self.speed = 0.1
        self.angle = 0

        rad = self.torad(self.angle)
        self.v[0] = math.cos(rad)
        self.v[2] = math.sin(rad)

        self.object_positions = []
        for i in range(64):
            x = random.randint(-30, 30)
            y = 0
            z = random.randint(-30, 30)
            self.object_positions.append((x, y, z))

        glViewport(0, 0, self.width, self.height)
        glClearColor(0.5, 0.5, 0.5, 1.0)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

    def torad(self, deg):
        return deg * (math.pi / 180)

    def keypress(self, ev):
        if ev.keysym == 'a':
            self.angle -= 1 
            rad = self.torad(self.angle)
            self.v[0] = math.cos(rad)
            self.v[2] = math.sin(rad)
        elif ev.keysym == 'd':
            self.angle += 1
            rad = self.torad(self.angle)
            self.v[0] = math.cos(rad)
            self.v[2] = math.sin(rad)
        elif ev.keysym == 'w':
            self.camera[0] += self.v[0] * self.speed
            self.camera[2] += self.v[2] * self.speed
        elif ev.keysym == 's':
            self.camera[0] -= self.v[0] * self.speed
            self.camera[2] -= self.v[2] * self.speed

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30, self.width/self.height, 0.1, 100)
        gluLookAt(
            self.camera[0], self.camera[1], self.camera[2],
            self.camera[0] + self.v[0], self.camera[1] + self.v[1], self.camera[2] + self.v[2],
            0.0, 1.0, 0.0,
        )
        # glLightfv(GL_LIGHT0, GL_AMBIENT, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.5, 0.4, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [3.0, 5.0, 3.0])

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.draw_objects()
        self.draw_player()

    def draw_objects(self):
        for v in self.object_positions:
            glPushMatrix()
            glTranslated(v[0], v[1], v[2])
            glBegin(GL_QUADS)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.6, 0.9])
            for i, face in enumerate(self.faces):
                glNormal3dv(self.normals[i])
                for fi in face:
                    v = self.vertices[fi]
                    glVertex3dv(v)
            glEnd()
            glPopMatrix()

    def draw_player(self):
        glPushMatrix()

        x = self.camera[0] + self.v[0] * 5
        z = self.camera[2] + self.v[2] * 5
        glTranslated(x, 0, z)
        glRotated(-self.angle, 0.0, 1.0, 0.0)

        glBegin(GL_QUADS)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0])
        for i, face in enumerate(self.faces):
            glNormal3dv(self.normals[i])
            for fi in face:
                v = self.vertices[fi]
                glVertex3dv(v)
        glEnd()
        glPopMatrix()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('OpenGL App')

        self.glframe = GLFrame(self, width=960, height=640)
        self.glframe.pack(expand=True, fill=tk.BOTH)
        self.glframe.animate = True

        self.bind('<KeyPress>', self.keypress)

    def keypress(self, ev):
        self.glframe.keypress(ev)


App().mainloop()
