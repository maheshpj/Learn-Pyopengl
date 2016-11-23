#! /usr/bin/env python

__author__ = 'maheshjadhav'

# OpenGLContext is a testing and learning environment for PyOpenGL. http://pyopengl.sourceforge.net/context/
from OpenGLContext import testingcontext

BaseContext = testingcontext.getInteractive()
from OpenGL.GL import *


class TestContext():
    """Rendering Context with custom viewpoint and render
    Note: will have slightly different results as OpenGLContext
    automatically enables lighting.
    """

    initialPosition = (0, 0, 0)  # set initial camera position, tutorial does the re-positioning

    def Render(self, mode):
        """Render the geometry for the scene."""
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glDisable(GL_CULL_FACE)

        glTranslatef(-1.5, 0.0, -6.0)

        # Show Traingle
        glBegin(GL_TRIANGLES)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glEnd()

        glTranslatef(3.0, 0.0, 0.0)

        # Show Square
        glBegin(GL_QUADS)
        glVertex3f(-1.0, -1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(-1.0, 1.0, 0.0)
        glEnd()


if __name__ == "__main__":
    TestContext.ContextMainLoop()
