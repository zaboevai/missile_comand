import math
import turtle
import random as rnd

screen_size = [1200,800]

window = turtle.Screen()
window.setup(1200+3,800+3)
window.bgpic('images/background.png')
window.screensize(screen_size[0],screen_size[1])
window.tracer(n=2)

base_y = -320
enemy_count = 10

base = {'our_base': 0,
        'nuclear': -500,
        'kremlin': -250,
        'skyscraper': 250,
        'house': 500
       }

base_image = {'our_base':   ['images/base.gif', 'images/base_opened.gif'],
              'kremlin':    ['images/kremlin_1.gif', 'images/kremlin_2.gif', 'images/kremlin_3.gif'],
              'house':      ['images/house_1.gif', 'images/house_2.gif', 'images/house_3.gif'],
              'nuclear':    ['images/nuclear_1.gif', 'images/nuclear_2.gif', 'images/nuclear_3.gif'],
              'skyscraper': ['images/skyscraper_1.gif', 'images/skyscraper_2.gif', 'images/skyscraper_3.gif']
             }

class Base:

    def __init__(self, x, y, name, image):
        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        base_pic = image
        window.register_shape(base_pic)
        pen.shape(base_pic)
        pen.showturtle()
        self.pen = pen
        self.base_name = name

    def get_base_name(self):
        return self.base_name

    def change_image(self, image):
        base_pic = image
        window.register_shape(base_pic)
        self.pen.shape(base_pic)

class Missile:
    def __init__(self, x, y, color, x2, y2):
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x=x2, y=y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen
        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(3)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                self.pen.color('red')
                self.pen.shape('circle')

        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 4:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            color = ('red', 'orange', 'yellow')
            self.pen.shape('circle')
            j = 0
            for i in range(1, 9):
                self.pen.shapesize(i)
                if i % 3 == 0:
                    j += 1
                    self.pen.color(color[j])
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()

def fire_missile(x, y):
    info = Missile(color='white',x = base['our_base'], y = base_y, x2= x, y2 = y)
    our_missiles.append(info)
    our_base.change_image(base_image['our_base'][1])

def fire_enemy_missile(enemy_x, enemy_y):
    x = rnd.randint(-100, 100)
    y = 400
    info = Missile(color='orange', x=x, y=y, x2=enemy_x, y2=enemy_y-30)
    enemy_missiles.append(info)


def moveMissile(missiles):
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)

def check_interception():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius*10:
                enemy_missile.state = 'dead'


def check_enemy_count():
    for key in base:
        if len(enemy_missiles) < enemy_count:
            fire_enemy_missile(base[key], base_y)

def game_over():
    return base_health < 0


def check_impact(target):
    global base_health
    global hit

    for key in target:
        for enemy_missile in enemy_missiles:
            if enemy_missile.state != 'explode':
                continue
            if enemy_missile.pen.distance(x=target[key], y=base_y) < enemy_missile.radius*10:
                base_health -= 100


# def check_base_health(hit):
# #     global base_health
# #     base_health -= hit
# #     print('base_health'+str(base_health))
# #     if base_health <= 1000:
# #         base_pic = 'images/base_opened.gif'
# #         window.register_shape(base_pic)
# #         our_base.shape(base_pic)
# #         return True
# #     return False

our_missiles = []
enemy_missiles = []
our_bases = []
base_health = 2000
hit = 0

for key in base:
    if key == 'our_base':
        our_base = Base(x=base[key],y=base_y, name=key, image=base_image[key][0])
    else:
        others_basis = Base(x=base[key],y=base_y, name=key, image=base_image[key][0])

window.onclick(fire_missile)



while True:
    window.update()

    if game_over():
        continue
    check_impact(target=base)
    # if check_base_health(hit)
    check_enemy_count()
    check_interception()
    moveMissile(missiles=our_missiles)
    moveMissile(missiles=enemy_missiles)


