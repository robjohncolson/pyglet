import pyglet
from pyglet.window import key
import math

window = pyglet.window.Window(fullscreen=True)
pyglet.resource.path.append('./images')
pyglet.resource.reindex()



def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

planet_image = pyglet.resource.image('mars.png')
center_anchor(planet_image)

class Planet(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, batch=None):
        super(Planet, self).__init__(
                image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.mass = 5000000 # experiment !
        #self.radius = (self.image.height +
        #               self.image.width) / 4
        print(self.image.height)
        print(self.image.width)
        self.radius = (50)

    def dist_vec_to(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        sqr_distance = dx**2 + dy**2
        distance = math.sqrt(sqr_distance)

        angle = math.acos(float(dx) / distance)
        if dy < 0:
            angle = 2*math.pi -angle
        return (distance, angle)

    def force_on(self, target):
        G = 1 #experiment !
        distance, angle = self.dist_vec_to(target)
        return ((-G * self.mass) / (distance ** 2), angle)

    def update(self, dt):
        force, angle = self.force_on(ship)
        force_x = force * math.cos(angle) * dt
        force_y = force * math.sin(angle) * dt
        ship.dx += force_x
        ship.dy += force_y
        distance, angle = self.dist_vec_to(ship)
        if distance <= ship.radius + self.radius:
            ship.reset()
            ship.alive = False
            return


center_x = int(window.width/2)
center_y = int(window.height/2)
planet = Planet(planet_image, center_x, center_y, None)

ship_image = pyglet.resource.image('ship.png')
center_anchor(ship_image)

class Ship(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0,
            dx=0, dy=0, rotv=0, batch=None):
        super(Ship, self).__init__(
                image, x, y, batch=batch)
        self.rot_left = False
        self.rot_right = False
        self.engines = False
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rotation = rotv
        self.thrust = 200.0
        self.rot_spd = 100.0
        self.alive = True
        self.radius = self.image.width / 2

    def reset(self):
        self.life_timer = 2.0 #seconds until resqawn
        self.x = center_x + 300
        self.y = center_y
        self.dx = 0; self.dy = 150
        self.rotation = -90

    def update(self, dt):
       self.image = ship_image
       if self.rot_left:
           self.rotation -= self.rot_spd * dt
       if self.rot_right:
           self.rotation += self.rot_spd * dt
       self.rotation = wrap(self.rotation, 360.)

       if self.engines:
           print("Self.Engine!")
           self.image = ship_image_on
           rotation_x = math.cos(
                   to_radians(self.rotation))
           rotation_y = math.sin(
                   to_radians(-self.rotation))
           self.dx += self.thrust * rotation_x * dt
           self.dy += self.thrust * rotation_y * dt
       self.x += self.dx * dt
       self.y += self.dy * dt
       self.x = wrap(self.x, window.width)
       self.y = wrap(self.y, window.height)
       
       if not self.alive:
           print ("Dead! Respawn in %s" %
                   self.life_timer)
           self.life_timer -= dt
           if self.life_timer > 0:
               return
           else:
               self.reset()
               self.alive = True

        

def update(dt):
        planet.update(dt)
        ship.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)
ship = Ship(ship_image,
            x=center_x + 300, y=center_y,
            dx=0, dy=150, rotv=-90)
ship.reset()

#window = pyglet.window.Window(fullscreen=True, visible=False, screen=screens[1])
window.set_visible()

display = pyglet.canvas.get_display()
#'find . -name *.py | entr python3 scratch.py'
for screen in display.get_screens():
    print(screen)

    label = pyglet.text.Label('Hello, world!',
                         font_name='Times New Roman',
                         font_size=10,
                         x=window.width//2, y=window.height//2,
                         anchor_x='center', anchor_y='center')


ship_image_on = pyglet.resource.image('ship_on.png')
center_anchor(ship_image_on)

def wrap(value, width):
    if width == 0:
        return 0
    if value > width:
        value -= width
    if value < 0:
        value += width
    return value

def to_radians(degrees):
    return math.pi * degrees / 180.0


@window.event
def on_draw():
    window.clear()
    planet.draw()
    #label.draw()
    if ship.alive:
        ship.draw()
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        ship.rot_left = True
        print('left')
    if symbol == key.RIGHT:
        ship.rot_right = True
        print('right')
    if symbol == key.UP:
        ship.engines = True
        print('up')
@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.LEFT:
        ship.rot_left = False
        print('left release')
    if symbol == key.RIGHT:
        ship.rot_right = False
        print('right release')
    if symbol == key.UP:
        ship.engines = False
        print('up release')

pyglet.app.run()
