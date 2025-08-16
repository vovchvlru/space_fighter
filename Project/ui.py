import pygame
from settings import *

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.SysFont(None, 36)
        
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
            
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 60, "Начать игру", GREEN, (100, 255, 100), GAME)
quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60, "Выход", RED, (255, 100, 100), "quit")

final_buttoons = [Button(WIDTH//2 - 100, HEIGHT//2 - 10, 200, 60, "Играть снова", GREEN, (100, 255, 100), "reset"),
                  Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "Выход", RED, (255, 100, 100), "quit")]

pause_buttons = [
    Button(WIDTH//2 - 100, HEIGHT//2 - 80, 200, 50, "Продолжить", GREEN, (100, 255, 100), GAME),
    Button(WIDTH//2 - 100, HEIGHT//2 - 20, 200, 50, "Сброс", BLUE, (100, 100, 255), "reset"),
    Button(WIDTH//2 - 100, HEIGHT//2 + 40, 200, 50, "Выход", RED, (255, 100, 100), "quit")
]

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_health_bar(surface, x, y, health):
    BAR_LENGTH = 200
    BAR_HEIGHT = 20
    fill = (health / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, RED, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def show_menu():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "Space Fighter", 64, WIDTH//2, HEIGHT//4)
    start_button.draw(screen)
    quit_button.draw(screen)
    pygame.display.flip()

def show_game_over(rank):
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    screen.blit(s, (0, 0))
    
    draw_text(screen, "ИГРА ОКОНЧЕНА", 64, WIDTH//2, HEIGHT//4)
    draw_text(screen, f"Ваш счет: {rank}", 48, WIDTH//2, HEIGHT//2 - 60)
    
    for button in final_buttoons:
        button.draw(screen)
    
    pygame.display.flip()

def show_pause_menu():
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    screen.blit(s, (0, 0))
    
    draw_text(screen, "ПАУЗА", 64, WIDTH//2, HEIGHT//4)
    
    for button in pause_buttons:
        button.draw(screen)
    
    pygame.display.flip()