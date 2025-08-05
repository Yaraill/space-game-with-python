import pygame
from sys import exit
import random

WIDTH = 1000
HEIGHT = 800

pygame.init()
game_name = pygame.display.set_caption("Meteordan Kaç")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2

bg_music = pygame.mixer.Sound("C:/Kodlama/space_game/space_game_images/Miami_Disco.mp3")
bg_music.set_volume(0.1)
bg_music.play(-1)

current_game_state = GAME_STATE_MENU
initial_meteor_spawn_rate = 325
min_meteor_spawn_rate = 125
difficulty_increase_amount = 50

current_meteor_spawn_rate = initial_meteor_spawn_rate

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Ship(pygame.sprite.Sprite):
    def __init__(self, image_path,speed,health,x,y):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert()
        self.original_image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.original_image,(50,50))

        self.rect = self.image.get_rect(center=(x,y))

        self.speed = speed
        self.health = health

    def take_damage(self,amount):
        self.health -= amount
        print(f"Gemi hasar aldı! Kalan can: {self.health}")
        if self.health <= 0:
            self.health = 0
            print(f"Gemi yok oldu! Oyun bitti!")
            self.kill()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        asteorid_images = [
            pygame.image.load("C:/Kodlama/space_game/space_game_images/asteroid_images/asteroid_1.png").convert_alpha(),
            pygame.image.load("C:/Kodlama/space_game/space_game_images/asteroid_images/asteroid_2.png").convert_alpha(),
            pygame.image.load("C:/Kodlama/space_game/space_game_images/asteroid_images/asteroid_3.png").convert_alpha(),
            pygame.image.load("C:/Kodlama/space_game/space_game_images/asteroid_images/asteroid_4.png").convert_alpha()
]
        self.original_image = random.choice(asteorid_images)

        size = random.randint(30,80)
        self.image = pygame.transform.scale(self.original_image,(size,size))

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0,WIDTH-self.rect.width)
        self.rect.y = random.randint(-HEIGHT,-self.rect.height)

        self.speed = random.randint(4,8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            global score
            score += 1
            self.kill()

def reset_game():
    global player_ship,all_sprites,enemies,score,game_active,current_game_state, current_background_image

    score = 0
    current_meteor_spawn_rate = initial_meteor_spawn_rate

    selected_ship_properties = SHIP_PROPERTIES[current_selected_ship_index]

    player_ship = Ship(
        image_path=selected_ship_properties["image_path"],
        speed=selected_ship_properties["speed"],
        health=selected_ship_properties["health"],
        x=WIDTH / 2,
        y=HEIGHT - 70
    )

    all_sprites.empty()
    enemies.empty()
    all_sprites.add(player_ship)

    pygame.time.set_timer(METEOR_SPAWN_EVENT,current_meteor_spawn_rate)
    pygame.time.set_timer(CHANGE_BACKGROUND_EVENT,10000)

    current_background_image = random.choice(loaded_background)

SHIP_PROPERTIES = [
    {
        "name": "Hızlı Gemi",
        "image_path": "C:/Kodlama/space_game/space_game_images/ship_images/ship_1.png",
        "speed": 6,
        "health": 3,
        "locked": False,
        "unlock_score": 0
    },
    {
        "name": "Tank Gemi",
        "image_path": "C:/Kodlama/space_game/space_game_images/ship_images/ship_2.png",
        "speed": 3,
        "health": 5,
        "locked": False,
        "unlock_score": 0
    },
    {
        "name": "Normal Gemi",
        "image_path": "C:/Kodlama/space_game/space_game_images/ship_images/ship_3.png",
        "speed": 4,
        "health": 4,
        "locked": False,
        "unlock_score": 0
    },
    {
        "name": "Millennium Falcon",
        "image_path": "C:/Kodlama/space_game/space_game_images/ship_images/ship_4.png",
        "speed": 8,
        "health": 4,
        "locked": True,
        "unlock_score": 200
    }
]

unlocked_ships = [False] * len(SHIP_PROPERTIES)
unlocked_ships[0] = True
unlocked_ships[1] = True
unlocked_ships[2] = True

BACKGROUND_IMAGES = [
    "C:/Kodlama/space_game/space_game_images/Purple Nebula/Purple Nebula 1 - 1024x1024.png",
    "C:/Kodlama/space_game/space_game_images/Purple Nebula/Purple Nebula 2 - 1024x1024.png",
    "C:/Kodlama/space_game/space_game_images/Purple Nebula/Purple Nebula 3 - 1024x1024.png",
    "C:/Kodlama/space_game/space_game_images/Purple Nebula/Purple Nebula 4 - 1024x1024.png",
    "C:/Kodlama/space_game/space_game_images/Purple Nebula/Purple Nebula 5 - 1024x1024.png",
]

loaded_background = []
for path in BACKGROUND_IMAGES:
    bg_image = pygame.image.load(path).convert()
    bg_image = pygame.transform.scale(bg_image,(WIDTH,HEIGHT))
    loaded_background.append(bg_image)

loaded_ship_images = []
for ship_prop in SHIP_PROPERTIES:
    ship_image = pygame.image.load(ship_prop["image_path"]).convert()
    ship_image.set_colorkey(WHITE)
    scaled_ship_image = pygame.transform.scale(ship_image,(50,50))
    loaded_ship_images.append(scaled_ship_image)

current_selected_ship_index = 0
current_background_image = random.choice(loaded_background)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

score = 0
game_active = True

CHANGE_BACKGROUND_EVENT = pygame.USEREVENT+2
pygame.time.set_timer(CHANGE_BACKGROUND_EVENT,10000)
METEOR_SPAWN_EVENT = pygame.USEREVENT+1
# pygame.time.set_timer(METEOR_SPAWN_EVENT,500)

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_game_state == GAME_STATE_MENU:
                    if SHIP_PROPERTIES[current_selected_ship_index]["locked"] and not unlocked_ships[current_selected_ship_index]:
                        print("You need to unlock this ship first!")
                    else:
                        reset_game()
                        current_game_state = GAME_STATE_PLAYING
                elif current_game_state == GAME_STATE_GAME_OVER:
                    current_game_state = GAME_STATE_MENU
            if current_game_state == GAME_STATE_MENU:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    next_index = current_selected_ship_index - 1
                    if next_index < 0:
                        next_index = len(SHIP_PROPERTIES) - 1
                    current_selected_ship_index = next_index
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    next_index = current_selected_ship_index + 1
                    if next_index >= len(SHIP_PROPERTIES):
                        next_index = 0
                    current_selected_ship_index = next_index

        if current_game_state == GAME_STATE_PLAYING:
            if event.type == METEOR_SPAWN_EVENT:
                new_meteor = Enemy()
                all_sprites.add(new_meteor)
                enemies.add(new_meteor)

            if event.type == CHANGE_BACKGROUND_EVENT:
                current_background_image = random.choice(loaded_background)
                current_meteor_spawn_rate -= difficulty_increase_amount

                if current_meteor_spawn_rate < min_meteor_spawn_rate:
                    current_meteor_spawn_rate = min_meteor_spawn_rate

                pygame.time.set_timer(METEOR_SPAWN_EVENT,current_meteor_spawn_rate)
                print(f"Zorluk arttı! Yeni meteor düşme hızı: {current_meteor_spawn_rate} ms")

    if current_game_state == GAME_STATE_MENU:
        screen.blit(current_background_image, (0,0))
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None,36)

        title_next = font_large.render("Run from Meteors",True,WHITE)
        title_rect = title_next.get_rect(center=(WIDTH/2, HEIGHT/2 - 150))
        screen.blit(title_next, title_rect)

        selected_ship_image = loaded_ship_images[current_selected_ship_index]
        ship_rect = selected_ship_image.get_rect(center=(WIDTH/2, HEIGHT/2-20))
        screen.blit(selected_ship_image, ship_rect)

        selected_ship_props = SHIP_PROPERTIES[current_selected_ship_index]

        if selected_ship_props["locked"] and not unlocked_ships[current_selected_ship_index]:
            overlay = pygame.Surface(selected_ship_image.get_size(),pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            screen.blit(selected_ship_image,ship_rect)
            screen.blit(overlay,ship_rect)

            ship_name_text = font_medium.render("Locked Ship!",True,(200,50,50))
            speed_text = font_small.render(f"To open: {selected_ship_props["unlock_score"]} Point",True,WHITE)
            health_text = font_small.render("Press -> You Cannot Use This Ship",True,WHITE)

            instruction_text = font_medium.render("Start with Space / Select Ship with A-D or DIRECTION keys",True,WHITE)
            if selected_ship_props["locked"] and not unlocked_ships[current_selected_ship_index]:
                instruction_text = font_medium.render(f"This Ship is Locked! {selected_ship_props["unlock_score"]} Points to Unlock",True,WHITE)

        else:
            screen.blit(selected_ship_image, ship_rect)
            ship_name_text = font_medium.render(f"Ship: {selected_ship_props['name']}", True, WHITE)
            speed_text = font_small.render(f"Speed: {selected_ship_props['speed']}", True, WHITE)
            health_text = font_small.render(f"Health: {selected_ship_props['health']}", True, WHITE)
            instruction_text = font_medium.render("Start with Space / Select Ship with A-D or DIRECTION keys",True,WHITE) 
        
        ship_name_rect = ship_name_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
        speed_rect = speed_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 90))
        health_rect = health_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 130))
        instruction_rect = instruction_text.get_rect(center=(WIDTH/2, HEIGHT - 50)) 

        screen.blit(ship_name_text, ship_name_rect)
        screen.blit(speed_text, speed_rect)
        screen.blit(health_text, health_rect)
        screen.blit(instruction_text, instruction_rect)

    elif current_game_state == GAME_STATE_PLAYING:
        screen.blit(current_background_image,(0,0))

        all_sprites.update()

        collide_meteors = pygame.sprite.spritecollide(player_ship,enemies,True)
        if collide_meteors:
            for meteor in collide_meteors:
                player_ship.take_damage(1)

        if not player_ship.alive():
            current_game_state = GAME_STATE_GAME_OVER

            pygame.time.set_timer(METEOR_SPAWN_EVENT,0)
            pygame.time.set_timer(CHANGE_BACKGROUND_EVENT,0)

        all_sprites.draw(screen)
        
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True,WHITE)
        screen.blit(score_text,(10,10))

        health_text = font.render(f"Health: {player_ship.health}", True,WHITE)
        screen.blit(health_text,(10,50))
    
    elif current_game_state == GAME_STATE_GAME_OVER:
        screen.blit(current_background_image,(0,0))
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)

        game_over_text = font_large.render("Game Over",True,WHITE)
        final_score_text = font_medium.render(f"Your Score: {score}",True,WHITE)
        restart_text = font_medium.render("Press Space to Restart",True,WHITE)

        game_over_rect = game_over_text.get_rect(center=(WIDTH/2,HEIGHT/2-80))
        final_score_rect = final_score_text.get_rect(center=(WIDTH/2,HEIGHT/2))
        restart_rect = restart_text.get_rect(center=(WIDTH/2,HEIGHT/2+80))

        screen.blit(game_over_text,game_over_rect)
        screen.blit(final_score_text,final_score_rect)
        screen.blit(restart_text,restart_rect)

        for i, ship_prop in enumerate(SHIP_PROPERTIES):
            if ship_prop["locked"] and not unlocked_ships[i]:
                if score >= ship_prop["unlock_score"]:
                    unlocked_ships[i] = True
                    print(f"CONGRATULATIONS! {ship_prop["name"]} is now unlocked!")


    pygame.display.update()
    clock.tick(60)
