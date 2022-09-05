import pyglet
from pyglet.window import key

window = pyglet.window.Window(visible=False)
window.set_visible()

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed')

@window.event
def on_draw():
    window.clear()


@window.event
def on_key_press(symbol, modifiers):
        if symbol == key.A:
            print('The "A" key was pressed.')
        elif symbol == key.LEFT:
            print('The left arrow key was pressed.')
        elif symbol == key.ENTER:                                               print('The enter key was pressed.')
pyglet.app.run()
