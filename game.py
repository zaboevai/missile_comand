import turtle
import random as rnd
import time
import os

BASE_PATH = os.path.dirname(__file__)
ENEMY_MISSILE_COUNT = 5
OUR_MISSILE_COUNT = 5
BASE_X, BASE_Y = 0, -320

BUILDINGS_INFOS = {
    'nuclear': [BASE_X - 500, BASE_Y],
    'kremlin': [BASE_X - 250, BASE_Y],
    'skyscraper': [BASE_X + 250, BASE_Y],
    'house': [BASE_X + 500, BASE_Y]
}

class Building:
    INITIAL_HEALTH = 1000

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.health = self.INITIAL_HEALTH
        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=self.x, y=self.y)
        pen.pendown()
        pic_path = os.path.join(BASE_PATH, 'images', self.get_pic_name())
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()

        self.pen = pen

        title = turtle.Turtle(visible=False)
        title.speed(0)
        title.penup()
        title.setpos(x=self.x, y=self.y - 75)
        title.color('white')
        title.write(str(self.health), align="center", font=["Arial", 12, "bold"])
        self.title = title
        self.title_health = self.health

    def get_pic_name(self):
        if self.health < self.INITIAL_HEALTH*0.2:
            return f'{self.name}_3.gif'
        if self.health < self.INITIAL_HEALTH*0.8:
            return f'{self.name}_2.gif'
        return f'{self.name}_1.gif'

    def draw(self):
        pic_name = self.get_pic_name()
        pic_path = os.path.join(BASE_PATH, 'images', pic_name)
        if self.pen.shape() != pic_path:
            window.register_shape(pic_path)
            self.pen.shape(pic_path)
            self.pen.shape(pic_path)
        if self.health != self.title_health:
            self.title_health = self.health
            if self.title_health <= 0:
                self.health = 0
            self.title.clear()
            self.title.write(str(self.health), align="center", font=["Arial", 12, "bold"])

    def is_alive(self):
        return self.health > 0


class MissileBase(Building):
    INITIAL_HEALTH = 2000

    def get_pic_name(self):
        for missile in our_missiles:
            if missile.distance(self.x, self.y) < 120:
                return f'{self.name}_opened.gif'
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
        if self.color == 'blue':
            pic_path = os.path.join(BASE_PATH, 'images', 'missile.gif')
        else:
            pic_path = os.path.join(BASE_PATH, 'images', 'missile2.gif')
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()
        self.pen = pen


        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            self.pen.clear()
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
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


def fire_missile(x, y):
    if len(our_missiles) < 5:
        info = Missile(color='blue', x=our_base.x, y=our_base.y+20, x2=x, y2=y)
        our_missiles.append(info)


def fire_enemy_missile():
    x = rnd.randint(-200, 200)
    y = 400
    alive_buildings = [b for b in buildings if b.is_alive()]
    if alive_buildings:
        target = rnd.choice(alive_buildings)
        info = Missile(color='red', x=x, y=y, x2=target.x, y2=target.y)
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
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius*10:
                enemy_missile.state = 'dead'


def game_over():
    return our_base.health <= 0


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_MISSILE_COUNT:
        fire_enemy_missile()


def check_impact():

    for enemy_missile in enemy_missiles:

        if enemy_missile.state != 'explode':
            continue
        else:
            for building in buildings:

                if enemy_missile.pen.distance(x=building.x,
                                              y=building.y) < enemy_missile.radius*20:
                    building.health -= 50
                    break


def draw_building():
    for building in buildings:
        building.draw()


screen_size = [1200, 800]
window = turtle.Screen()
window.setup(1200+3, 800+3)
window.screensize(screen_size[0], screen_size[1])


def game():
    global our_missiles, enemy_missiles, buildings, our_base

    window.clear()
    window.tracer(n=2)
    window.bgpic(os.path.join(BASE_PATH, 'images', 'background.png'))
    window.onclick(fire_missile)

    our_missiles = []
    enemy_missiles = []
    buildings = []

    our_base = MissileBase(x=BASE_X, y=BASE_Y, name='base')
    buildings.append(our_base)

    for name, position in BUILDINGS_INFOS.items():
        others_base = Building(x=position[0], y=position[1], name=name)
        buildings.append(others_base)

    while True:
        window.update()



        if game_over():
            break

        check_enemy_count()
        check_impact()
        check_interception()
        draw_building()

        move_missile(missiles=our_missiles)
        move_missile(missiles=enemy_missiles)
        time.sleep(.01)

    pen = turtle.Turtle(visible=False)
    pen.speed(0)
    pen.penup()
    pen.setpos(x=0, y=0)
    pen.color('white')
    pen.write('GAME OVER', align="center", font=["Arial", 60, "bold"])


while True:
    game()

    answer = window.textinput('Игра', 'Еще разок ?')
    if answer == None:
        break
