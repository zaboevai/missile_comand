import math
import turtle
import random as rnd
import time
import os


BASE_PATH = os.path.dirname(__file__)
ENEMY_MISSILE_COUNT = 1
OUR_MISSILE_COUNT = 5
BASE_X, BASE_Y = 0, -320


class Building:
    INITIAL_HEALTH = 1000

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=self.x, y=self.y)
        pen.pendown()
        pic_path = os.path.join(BASE_PATH, 'images', self.get_pic_name())
        print(pic_path)
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()

        self.pen = pen
        self.health = self.INITIAL_HEALTH

    def get_pic_name(self):
        return f'{self.name}_1.gif'

    def change_image(self):
        # self.pen.showturtle()
        base_pic = image
        window.register_shape(base_pic)
        self.pen.shape(base_pic)


class MissileBase(Building):
    INITIAL_HEALTH = 2000

    def get_pic_name(self):
        return f'{self.name}.gif'


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
            self.pen.forward(4)
            # self.pen.clear()
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                # self.pen.color(self.pen.color)
                self.pen.shape('circle')

        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)

        elif self.state == 'dead':
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

    @property
    def target_x(self):
        return self.target[0]

    @property
    def target_y(self):
        return self.target[1]


def fire_missile(x, y):
    if len(our_missiles) < 5:
        info = Missile(color='red', x=our_base.x, y=our_base.y, x2=x, y2=y)
        our_missiles.append(info)


def fire_enemy_missile(enemy_x, enemy_y):
    x = rnd.randint(-200, 200)
    y = 400
    info = Missile(color='orange', x=x, y=y, x2=enemy_x, y2=enemy_y-30)
    enemy_missiles.append(info)


def move_missile(missiles):
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
            print(enemy_missile.distance(our_missile.x, our_missile.y), our_missile.radius)
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius*10:
                enemy_missile.state = 'dead'


def game_over():
    return our_base.health < 0


def check_base_fire():
    if len(our_missiles) > 0:
        our_base.change_image(our_base['our_base']['image'][1])
    elif len(our_missiles) == 0:
        our_base.change_image(our_base['our_base']['image'][0])


def check_enemy_count():
    target = rnd.choice(buildings)
    if len(enemy_missiles) < ENEMY_MISSILE_COUNT:
        fire_enemy_missile(target.x, target.y)


def check_impact():
    # global game_end

    for enemy_missile in enemy_missiles:

        if enemy_missile.state != 'explode':
            continue
        else:
            for building in buildings:

                if enemy_missile.pen.distance(x=building.x,
                                              y=building.y) < enemy_missile.radius*20:
                    building.health -= 100
                    print(f'{building.name} - {building.health}')
                    break

def check_base_health():
    for base in buildings:
        if base.health < 2000:
            print(base.health)


screen_size = [1200, 800]
window = turtle.Screen()
window.setup(1200+3, 800+3)
window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
window.screensize(screen_size[0], screen_size[1])
window.tracer(2)

our_missiles = []
enemy_missiles = []
buildings = []
game_end = False

our_base = MissileBase(x=BASE_X, y=BASE_Y, name='base')
buildings.append(our_base)

buildings_infos = {
    'nuclear': [BASE_X - 500, BASE_Y],
    'kremlin': [BASE_X - 250, BASE_Y],
    'skyscraper': [BASE_X + 250, BASE_Y],
    'house': [BASE_X + 500, BASE_Y]
}

for name, position in buildings_infos.items():
    others_base = Building(x=position[0], y=position[1], name=name)
    buildings.append(others_base)

window.onclick(fire_missile)

while True:
    window.update()

    if game_over():
        continue

    check_enemy_count()
    check_impact()
    check_interception()
    # check_base_health()

    # check_base_fire()

    move_missile(missiles=our_missiles)
    move_missile(missiles=enemy_missiles)
    time.sleep(.01)