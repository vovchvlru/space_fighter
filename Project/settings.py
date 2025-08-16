import pygame

pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
screen_w, screen_h = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_w, screen_h), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Space Fighter")

def load_image(name, scale=1):
    image = pygame.image.load(name)
    if scale != 1:
        size = image.get_size()
        image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
    return image.convert_alpha()

def load_sound(name):
    return pygame.mixer.Sound(name)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 

score = 0
font = pygame.font.SysFont(None, 36)
enemy_count = 8
score_for_next_wave = 100

MENU = 0
GAME = 1
GAME_OVER = 2
PAUSE = 3

player_img = load_image("assets/player.png", 0.1)
enemy_img = load_image("assets/enemy.png", 0.1)
bullet_img = load_image("assets/bullet.png", 0.05)
enemy_bullet_img = load_image("assets/enemy_bullet.png", 0.05)
background_img = load_image("assets/background.png")
health_icon = load_image("assets/health.png", 0.1)
fire_rate_icon = load_image("assets/fire_rate.png", 0.1)
speed_icon = load_image("assets/speed.png", 0.1)
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

shoot_sound = load_sound("assets/sounds/shoot.wav")
explosion_sound = load_sound("assets/sounds/explosion.wav")
hit_sound = load_sound("assets/sounds/hit.wav")
lost_sound = load_sound("assets/sounds/game_over.wav")
critical_sound = load_sound("assets/sounds/critical.wav")
powerup_sound = load_sound("assets/sounds/powerup.wav")
new_wave_sound = load_sound("assets/sounds/new_wave.wav")
background_music = "assets/sounds/background.mp3"
main_music = "assets/sounds/main.mp3"