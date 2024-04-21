import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
game_running = False

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return[pygame.transform.flip(sprite, True, False) for sprite in sprites]

def draw_menu(win, width, height, background_image_path):
    # Load the background image
    background_image = pygame.image.load(background_image_path)
    # Resize the background image to match the window size
    background_image = pygame.transform.scale(background_image, (width, height))
    
    # Blit the background image onto the window
    win.blit(background_image, (0, 0))

    font = pygame.font.SysFont(None, 60)
    font_2 = pygame.font.SysFont(None, 40)
    font_3 = pygame.font.SysFont(None, 20)
    text = font.render('Welcome to the Platformer!', True, (0, 0, 0))
    text_2 = font_2.render('A work by Sefrid Kapllani!', True, (0, 0, 0))
    text_3 = font_3.render('Press any key to START!', True, (0, 0, 0))
    
    # Calculate the positions of the two text surfaces so they don't overlap
    text_rect = text.get_rect(center=(width / 2, height / 2 - 30))  # Positioning slightly above center
    text_rect_2 = text_2.get_rect(center=(width / 2, height / 2 + 30))  # Positioning slightly below center
    text_rect_3 = text_3.get_rect(center=(width / 2, height / 2 + 90))  # Positioning slightly below center

    # Blit each text surface separately onto the window
    win.blit(text, text_rect)
    win.blit(text_2, text_rect_2)
    win.blit(text_3, text_rect_3)

    # Update the display
    pygame.display.update()

# Example usage
pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
background_image_path = "assets/Background/Screenshot.png"  # Change this to the path of your image
draw_menu(window, window_width, window_height, background_image_path)


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}  # This dictionary will hold all sprites, keyed by their names
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)  # Note the removal of the extra space in "_left "
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites  # Return the dictionary of all sprites

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 5
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.score = 0 
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count +=1
        if self.jump_count ==1:
            self.count = 0
            
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        if not self.hit:  # Only register a hit if not currently hit
            self.hit = True
            self.hit_count = FPS * 2  # 2 seconds recovery time

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)   
        if self.hit:
            self.hit_count -= 1
            if self.hit_count <= 0:
                self.hit = False  # Reset hit status after recovery time

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0\
        
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        if self.y_vel < 0:
            if self.jump_count ==1:
                sprite_sheet = "jump"
            elif self.jump_count ==2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel !=0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count != 1
        self.update()
    
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, name=""):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name  # Add a name attribute

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def collect(self):
        self.kill()

class Object(pygame.sprite.Sprite):
    def __init__(self, x , y, width, height, name=None):
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self,x ,y ,size):
        super().__init__(x,y,size,size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height): 
        super().__init__(x,y,width,height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]

        # Increment the animation count
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        # Reset the animation count if it exceeds the number of sprites times the delay
        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0

class Button:
    def __init__(self, image, pos, action):
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.action = action
    
    def draw(self, win):
        win.blit(self.image, self.rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

def load_buttons():
    path = "assets/Menu/Buttons"  # Update with the correct path
    return {
        "start": Button(pygame.image.load(os.path.join(path, "Play.png")), (WIDTH // 2, HEIGHT // 2 - 100), start_game),
        "levels": Button(pygame.image.load(os.path.join(path, "Levels.png")), (WIDTH // 2, HEIGHT // 2), view_levels),
        "achievements": Button(pygame.image.load(os.path.join(path, "Achievements.png")), (WIDTH // 2, HEIGHT // 2 + 100), view_achievements),
        "settings": Button(pygame.image.load(os.path.join(path, "Settings.png")), (WIDTH // 2, HEIGHT // 2 + 200), settings)
    }

def start_game():
    global game_running
    game_running = True  # Set the game state to running

def view_levels():
    pass
def view_achievements():
    pass
def settings():
    pass

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width +1):
        for j in range (HEIGHT // height+1):
            pos = (i * width, j * height)
            tiles.append(pos)
    
    return tiles, image

def draw(window, bacground, bg_image, player, objects, offset_x):
    for tile in bacground:
        window.blit(bg_image, tile)
    
    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head
            collided_objects.append(obj)
    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0) 
    player.update()
    return collided_object 


def handle_move(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)
    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

def draw_score(surface, score, x, y):
    print(f"Drawing score: {score}")  # Debug print
    font = pygame.font.SysFont('arial', 30)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(score_text, (x, y))

def main(window, background_image_path):
    clock = pygame.time.Clock()

    menu_open = True
    while menu_open:
        draw_menu(window, WIDTH, HEIGHT, background_image_path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                menu_open = False

    buttons = load_buttons()

    # Second menu loop
    second_menu_open = True
    while second_menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                second_menu_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, button in buttons.items():
                    if button.rect.collidepoint(event.pos):
                        button.action()
                        if button_name == "start":  # If the start button was pressed
                            second_menu_open = False  # Close the menu to start the game
                        
        window.fill((0, 0, 0))  # Clear the window or draw a background
        for button in buttons.values():
            button.draw(window)
        pygame.display.update()
        clock.tick(FPS)

    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    objects = []
    block_size = 96
    player = Player(100, 100, 50, 50)
    fire_objects = [Fire(100, HEIGHT - block_size - 64, 16, 32), Fire(150, HEIGHT - block_size - 64, 16, 32)]
    start_x = 0
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)]
    blocks_in_column = HEIGHT // block_size
    starting_column = [Block(start_x, y * block_size, block_size) for y in range(blocks_in_column)]
    last_vertical_block_x = starting_column[-1].rect.right
    fruits = []
    fruit_spacing = 5  # This means an apple every 5 blocks
    for i, block in enumerate(floor):
        if i % fruit_spacing == 0 and block.rect.x > last_vertical_block_x:
            fruits.append(Collectible(block.rect.x, block.rect.y - block_size, 'assets/Items/Fruits/Apple.png'))
    objects = [*starting_column, *floor, Block(0, HEIGHT - block_size * 2, block_size), Block(block_size * 2, HEIGHT - block_size * 3, block_size), Block(block_size * 3, HEIGHT - block_size * 3, block_size), *fire_objects]
    offset_x = 0
    scroll_area_width = 200
    objects.extend(floor)
    for fire in fire_objects:
        fire.on()
        objects.append(fire)  # Add fire objects to the list
    fruits = [Collectible(block.rect.x, block.rect.y - block_size, 'assets/Items/Fruits/Apple.png') for block in floor]
    objects.extend(fruits)  # Add fruit objects to the list
    run = True
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        for fire in fire_objects:
            fire.loop()

        for fruit in fruits[:]:  # Use a slice copy to avoid issues when removing items
            if pygame.sprite.collide_mask(player, fruit):
                fruit.collect()
                player.score += 1
                objects.remove(fruit)  # Remove from objects list
                fruits.remove(fruit)  # Remove from fruits list

        # Draw everything including fruits
        for obj in objects:
            obj.draw(window, player.rect.x - player.rect.width // 2)  # Adjust as necessary for scrolling
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)
        draw_score(window, player.score, WIDTH - 120, 10)
        if((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        pygame.display.update()  # Update the display
    pygame.quit()
    quit()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Platformer")
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    main(window, background_image_path)

