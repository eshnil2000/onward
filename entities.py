import random


class Exp:

    def __init__(self, x, y, amount):
        self.type = "experience"
        self.x = x
        self.y = y
        self.amount = amount

class Bullet:

    def __init__(self, x, y, x_vel, y_vel, owner):
        self.type = "bullet"
        self.x = x
        self.y = y
        self.x_velocity = x_vel
        self.y_velocity = y_vel
        self.owner = owner

class Creature:

    def __init__(self, x, y, size):
        self.type = "creature"
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.size = size
        self.state = "alive"

        self.direction = 'left'
        self.health = 100
        self.experience = 0

        self.weapon = 0
        self.cooldown_period = 0

    def move(self, direction):
        self.direction = direction
        if direction is "left":
            self.x_velocity -= 1
        elif direction is "right":
            self.x_velocity += 1

    def jump(self):
        pass

    def shoot(self, dext_x, dest_y):
        bullets = []
        speed = 0
        nr_of_bullets = 0

        if self.cooldown_period > 0:
            return []

        if self.weapon == "pistol":
            nr_of_bullets = 1
            speed = 4
            self.cooldown_period += 40
        elif self.weapon == "shotgun":
            nr_of_bullets = 5
            speed = 3
            self.cooldown_period += 50
        elif self.weapon == "machine_gun":
            nr_of_bullets = 1
            speed = 6
            self.cooldown_period += 5

        for i in range(nr_of_bullets):
            speed += random.uniform(-1, 1)
            x_vel = (1 * speed) + random.uniform(-1, 1)
            y_vel = ((dest_y / dest_x) * speed) + random.uniform(-1, 1)
            bullet = Bullet(self.x + (self.size / 2), self.y + (self.size / 2), x_vel, y_vel, self)
            bullets.append(bullet)

        return bullets
