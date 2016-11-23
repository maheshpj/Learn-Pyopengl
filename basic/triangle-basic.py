#! /usr/bin/env python

__author__ = 'maheshjadhav'

from OpenGL.GL import *
import glfw
import numpy, sys


class BasicTriangle:
    vertex_shader = """
        #version 410
        in vec3 vp;
        void main () {
            gl_Position = vec4 (vp, 1.0);
        }
    """

    frag_shader = """
        #version 410
        out vec4 frag_colour;
        void main () {
            frag_colour = vec4 (0.5, 0.0, 0.5, 1.0);
        }
    """

    def create_window(self):
        # Initialize the library
        if not glfw.init():
            return

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.SAMPLES, 4)  # anti-aliasing

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(640, 480, "Basic Triangle", None, None)
        if not self.window:
            print >> sys.stderr, "ERROR: Could not open window with glfw3"
            glfw.terminate()
            return

        glfw.set_key_callback(self.window, self.keypress)
        # Make the window's context current
        glfw.make_context_current(self.window)

    def keypress(key, action):
        """When ESCAPE key is pressed, close the window"""
        if key == glfw.KEY_ESCAPE:
            glfw.terminate()
            sys.exit(-1)

    prev_seconds = 0.0
    frame_count = 0

    def update_fps_counter(self, window):
        current_seconds = glfw.get_time()
        elapsed_seconds = current_seconds - self.prev_seconds

        if elapsed_seconds > 0.25:
            self.prev_seconds = current_seconds
            fps = self.frame_count / elapsed_seconds
            tmp = "Opengl @ fps: %f" % fps
            glfw.set_window_title(window, tmp)
            self.frame_count = 0

        self.frame_count += 1

    def run(self):
        """Render the geometry for the Triangle"""

        print >> sys.stderr, "Rendering basic Triangle"

        self.create_window()

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glDisable(GL_CULL_FACE)

        points = [
            0.0, 0.5, 0.0,
            0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0
        ]
        vertex_data = numpy.array(points, numpy.float32)

        # Setup VBO
        print >> sys.stderr, "Generate VBO"
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, 9 * len(vertex_data), vertex_data, GL_STATIC_DRAW)

        # Setup VAO
        print >> sys.stderr, "Generate VAO"
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # Setup Shader
        print >> sys.stderr, "Setup Shader"
        vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vs, self.vertex_shader)
        glCompileShader(vs)

        fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fs, self.frag_shader)
        glCompileShader(fs)

        shader_programme = glCreateProgram()
        glAttachShader(shader_programme, fs)
        glAttachShader(shader_programme, vs)
        glLinkProgram(shader_programme)

        glDeleteShader(vs)
        glDeleteShader(fs)

        glClearColor(0.6, 0.6, 0.8, 1.0)

        # Loop until the user closes the window
        while not glfw.window_should_close(self.window):
            self.update_fps_counter(self.window)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram(shader_programme)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        glfw.terminate()

    def __init__(self):
        pass


if __name__ == "__main__":
    BasicTriangle().run()
