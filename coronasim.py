from hashlib import new
import os
from warnings import showwarning
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from math import e, inf
import pygame
import random
from pygame.math import Vector2
import time
import math
from termcolor import colored
import pandas as pd
from datetime import datetime
from tqdm import tqdm



print(colored('Blue', 'blue')+' squares are inital infected: These can infect others')
print(colored('Red', 'red')+' squares are new infected: They cannot infect others')
print(colored('Green', 'green')+' squares are heatlhy people')


# Settings
WIDTH = 750
HEIGHT = 750
FPS = 30
SPEED = 1
SIZE = 7
DIRECTION_CHANGE_THRESHOLD_X = 0.2
DIRECTION_CHANGE_THRESHOLD_Y = 0.2
STEPS_BEFORE_CHANGE = 30
MIN_STEPS = 10
MAX_STEPS = 50
MIN_THRESHOLD = 0
MAX_THRESHOLD = 100
INFECTION_DISTANCE = 7
NUMBER_PERSONS = int(input("How many people in the shop?: "))
NUMBER_INFECTED_PERSONS = int(input("How many infected people in the shop?: "))
MINUTES = int(input("How many minutes should the simulation run for?: "))
HOW_MANY_RUNS = int(input("How many runs should the simulation run for?: "))
MAX_TIME_IN_SHOP = 10
MIN_TIME_IN_SHOP = 2
INFECTION_THRESHOLD = 0.8
SHOP_SIZE=HEIGHT/5


RELATIONSHIP_MATRIX= {
    1: [1,0,0,0,0,0,0,0,0,0],
    2: [0,1,0.34,0.35,0,0,0,0,0,0],
    3: [0,0.4,1,0.42,0,0,0,0,0,0.3],
    4: [0,0.2,0.2,1,0,0,0,0,0,0],
    5: [0,0,0,0,1,0.63,0,0.5,0.53,0],
    6: [0,0,0,0,0.32,1,0.31,0,0,0],
    7: [0,0,0,0,0,0.31,1,0,0,0],
    8: [0,0,0,0,0.13,0,1,0,0,0],
    9: [0,0,0,0.18,0,0,0,0,1,0],
    10: [0,0,0.2,0,0,0,0,0,0,1]
    }


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Person(pygame.sprite.Sprite):
    def __init__(self, infected, selected_shop, shops, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((SIZE, SIZE))
        self.rect = self.image.get_rect()

        self.id = id

        self.shop_duration = random.randint(MIN_TIME_IN_SHOP, MAX_TIME_IN_SHOP)

        self.start_time = time.time()
        self.infection_time = "N/A"
        self.dt_string = 'N/A'



        self.selected_shop = selected_shop

        self.known_shops = shops

        self.width_limit = self.selected_shop.x + self.selected_shop.width
        self.height_limit = self.selected_shop.y + self.selected_shop.height
        self.x_limit = self.selected_shop.x
        self.y_limit = self.selected_shop.y

        self.rect.x = random.randint(self.x_limit, self.width_limit)
        self.rect.y = random.randint(self.y_limit, self.height_limit)

        self.xsign = 0
        self.ysign = 0
        self.destination_x = 0
        self.destination_y = 0

        self.radius = SIZE//2

        self.infected = infected
        self.original_infected = infected
        if self.original_infected == True:
            self.image.fill(BLUE)
        else:
            self.image.fill(GREEN)


        self.choose_x_point()
        self.choose_y_point()
        self.choose_x_sign()
        self.choose_y_sign
        
    
    def update(self):
        if self.rect.x >= self.destination_x:
            self.choose_x_point()
            self.choose_x_sign()

        if self.rect.y >= self.destination_y:
            self.choose_y_point()
            self.choose_y_sign()


        self.move_x()
        self.move_y()
        end_time = time.time()
        elapsed_time = (end_time - self.start_time)
        if elapsed_time >= self.shop_duration:
            self.select_new_shop()
            self.start_time = time.time()
            self.shop_duration = random.randint(MIN_TIME_IN_SHOP, MAX_TIME_IN_SHOP)
        self.check_bounds()
        

    def choose_x_sign(self):
            if self.destination_x > self.rect.x:
                self.xsign = 1
            else:
                self.xsign = -1
    

    def choose_y_sign(self):
            if self.destination_y > self.rect.y:
                self.ysign = 1
            else:
                self.ysign = -1
            
    
    def move_x(self):
        self.rect.x += SPEED*self.xsign


    def move_y(self):
        self.rect.y += SPEED*self.ysign

    
    def choose_x_point(self):
        self.destination_x = random.randint(self.x_limit, self.width_limit)


    def choose_y_point(self):
        self.destination_y = random.randint(self.y_limit, self.height_limit)


    def check_bounds(self):
        if self.rect.x+SIZE >= self.width_limit:
            self.xsign = -1
        if self.rect.x <= self.x_limit:
            self.xsign = 1
        if self.rect.y+SIZE >= self.height_limit:
            self.ysign = -1
        if self.rect.y <= self.y_limit:
            self.ysign = 1


    def select_new_shop(self):
        weight_list =  RELATIONSHIP_MATRIX[self.selected_shop.id]
        new_shop=random.choices(population=self.known_shops,weights=weight_list,k=1)
        if new_shop[0] == self.selected_shop:
            pass
        else:
            self.selected_shop = new_shop[0]
            self.width_limit = self.selected_shop.x + self.selected_shop.width
            self.height_limit = self.selected_shop.y + self.selected_shop.height
            self.x_limit = self.selected_shop.x
            self.y_limit = self.selected_shop.y
            self.rect.x = random.randint(self.x_limit, self.width_limit)
            self.rect.y = random.randint(self.y_limit, self.height_limit)
            self.xsign = 0
            self.ysign = 0
            self.destination_x = 0
            self.destination_y = 0
            self.choose_x_point()
            self.choose_y_point()
            self.choose_x_sign()
            self.choose_y_sign


class Shop(pygame.sprite.Sprite):
    def __init__(self, screen, color, name, x, y, width, height, id):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.color = color
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id
    

    def drawself(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 2)


def check_infection(left, right):
    if left != right:
        distance = Vector2(left.rect.center).distance_to(right.rect.center)
        if distance < left.radius+INFECTION_DISTANCE:
            status = random.random()
            if status < INFECTION_THRESHOLD:
                if left.original_infected == True:
                    if left.selected_shop == right.selected_shop:
                        right.infected = True
                        if right.original_infected != True:
                            right.image.fill(RED)
                            right.infection_time = time.time()
                            right_now = datetime.now()
                            right.dt_string = right_now.strftime("%d/%m/%Y %H:%M:%S")


        distance = Vector2(right.rect.center).distance_to(left.rect.center)
        if distance < left.radius+50:
            status = random.random()
            if status < INFECTION_THRESHOLD:
                if right.original_infected == True:
                    if left.selected_shop == right.selected_shop:
                        left.infected = True
                        if left.original_infected != True:
                            left.image.fill(RED)
                            left.infection_time = time.time()
                            right_now = datetime.now()
                            left.dt_string = right_now.strftime("%d/%m/%Y %H:%M:%S")


    
def main():
    run_count = 0
    first_write_general = True
    first_write_person = True
    for run_count in tqdm(range(0, HOW_MANY_RUNS)):
        pygame.init()
        pygame.mixer.init()

        # BackGround = Background('Images/shops.png', [0,0])
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Coronavirus Infection Simulation")
        clock = pygame.time.Clock()
        all_people = pygame.sprite.Group()
        all_shops = pygame.sprite.Group()

        shops = []


        #Left Side
        optician = Shop(screen, BLACK, 'Optician', 0, SHOP_SIZE*4, SHOP_SIZE, SHOP_SIZE, 1)
        shops.append(optician)

        sports_outlet = Shop(screen, BLACK, 'Sports Outlet', 0, SHOP_SIZE*3, SHOP_SIZE, SHOP_SIZE, 2)
        shops.append(sports_outlet)

        clothing_store = Shop(screen, BLACK, 'Clothing Store', 0, SHOP_SIZE*2, SHOP_SIZE, SHOP_SIZE, 3)
        shops.append(clothing_store)

        shoe_shop = Shop(screen, BLACK, 'Shoe Shop', 0, SHOP_SIZE, SHOP_SIZE, SHOP_SIZE, 4)
        shops.append(shoe_shop)

        #Top
        Supermarket = Shop(screen, BLACK, 'Supermarket', 0, 0, WIDTH, SHOP_SIZE, 5)
        shops.append(Supermarket)

        #Right Side
        bakery = Shop(screen, BLACK, 'Bakery', WIDTH-SHOP_SIZE, SHOP_SIZE, SHOP_SIZE, SHOP_SIZE, 6)
        shops.append(bakery)

        salon = Shop(screen, BLACK, 'Salon', WIDTH-SHOP_SIZE, SHOP_SIZE*2, SHOP_SIZE, SHOP_SIZE, 7)
        shops.append(salon)

        toys = Shop(screen, BLACK, 'Toys & Gifts', WIDTH-SHOP_SIZE, SHOP_SIZE*3, SHOP_SIZE, SHOP_SIZE, 8)
        shops.append(toys)

        pharmacy = Shop(screen, BLACK, 'Pharmacy', WIDTH-SHOP_SIZE, SHOP_SIZE*4, SHOP_SIZE, SHOP_SIZE, 9)
        shops.append(pharmacy)

        #Mid
        cafe = Shop(screen, BLACK, 'Cafe', (WIDTH/2)-(SHOP_SIZE/2), (HEIGHT/2), SHOP_SIZE, SHOP_SIZE, 10)
        shops.append(cafe)

        exit = Shop

        infected_count = 0
        for n in range(0, NUMBER_PERSONS):
            selected_shop = random.choice(shops)
            if infected_count != NUMBER_INFECTED_PERSONS:
                person = Person(True, selected_shop, shops, n)
                all_people.add(person)
                infected_count += 1
            else:
                person = Person(False, selected_shop, shops,n)
                all_people.add(person)
        

        # Game loop
        end_simulation = False
        start_time = time.time()
        now = datetime.now()               
        start_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
        while time.time() < start_time+(60*MINUTES) and end_simulation != True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_simulation = True

            # Update
            all_people.update()
            collided_sprites = pygame.sprite.groupcollide(all_people, all_people, False, False,collided=check_infection)

            screen.fill(WHITE)
            # screen.blit(BackGround.image, BackGround.rect)
            for shop in shops:
                shop.drawself()
            all_people.draw(screen)
            pygame.display.flip()


        end_time = time.time()
        now = datetime.now()               
        end_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
        elapsed_time = (end_time - start_time)
        final_infected = 0
        for sprite in all_people:
            if sprite.infected == True:
                final_infected += 1


        # print('There were '+str(final_infected-NUMBER_INFECTED_PERSONS)+ ' new infections for '+str(NUMBER_INFECTED_PERSONS)+' initial infected people in a total of '+str(NUMBER_PERSONS)+ ' people over '+str(round((elapsed_time/60),2)) +' minutes')
        data = [[final_infected-NUMBER_INFECTED_PERSONS, NUMBER_INFECTED_PERSONS, NUMBER_PERSONS, round((elapsed_time/60),2)]]
        df = pd.DataFrame(data, columns = ['Number of New Infected', 'Number of original infected', 'Total number of people', 'Time elapsed'])
        if first_write_general:
            df.to_csv('general_data.csv')
            first_write_general = False
        else:
            df.to_csv('general_data.csv', mode='a', header=False)

        timestamp_list = []
        for person in all_people:
            if person.infection_time == 'N/A':
                timestamp_list.append([run_count, person.id, person.infection_time, start_datetime, person.dt_string, end_datetime])
            else:
                elapsed = person.infection_time-start_time
                timestamp_list.append([run_count, person.id, round((elapsed/60),2), start_datetime, person.dt_string, end_datetime])


        df = pd.DataFrame(timestamp_list, columns = ['Run ID', 'Person ID', 'Time of Infection (Mins)', 'Datetime of Sim Start', 'Datetime of When Infected', 'Datetime if Sim End'])
        if first_write_person:
            df.to_csv('person_data.csv')
            first_write_person = False
        else:
            df.to_csv('person_data.csv', mode='a', header=False)


        pygame.quit()


if __name__=="__main__":
    main()
