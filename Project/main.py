import pygame
import sys
import random
from settings import *
from sprites import *
from ui import *

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(main_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
buffs = pygame.sprite.Group()

player = Player()
player.set_image(player_img)
all_sprites.add(player)

for i in range(enemy_count):
    enemy = Enemy()
    enemy.set_image(enemy_img)
    all_sprites.add(enemy)
    enemies.add(enemy)

game_state = MENU
is_critical_playing = False
clock = pygame.time.Clock()
running = True

def reset_game():
    global all_sprites, enemies, bullets, enemy_bullets, buffs, player, score, enemy_count, score_for_next_wave
    
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    buffs = pygame.sprite.Group()
    
    player = Player()
    player.set_image(player_img)
    all_sprites.add(player)
    
    enemy_count = 8
    score_for_next_wave = 100
    
    for i in range(enemy_count):
        enemy = Enemy()
        enemy.set_image(enemy_img)
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    score = 0
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

def increase_enemies():
    global enemy_count, score_for_next_wave
    
    enemy_count += 3
    score_for_next_wave += 100
    
    for _ in range(3):
        enemy = Enemy()
        enemy.set_image(enemy_img)
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    if random.random() < 0.7:
        buff = Buff(random.randint(50, WIDTH-50), -50)
        buff_type = buff.type
        if buff_type == 'health':
            buff.set_image(health_icon)
        elif buff_type == 'fire_rate':
            buff.set_image(fire_rate_icon)
        elif buff_type == 'speed':
            buff.set_image(speed_icon)
        all_sprites.add(buff)
        buffs.add(buff)
    
    wave_notification = font.render(f"Уровень {round((enemy_count-8)/3)+1}!", True, YELLOW)
    screen.blit(wave_notification, (WIDTH//2 - wave_notification.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    if new_wave_sound:
        new_wave_sound.play()
    pygame.time.delay(1500)
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if game_state == MENU:
            if start_button.is_clicked(pygame.mouse.get_pos(), event):
                game_state = start_button.action
                reset_game()
            if quit_button.is_clicked(pygame.mouse.get_pos(), event):
                running = False
                
        elif game_state == PAUSE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    game_state = GAME
            for button in pause_buttons:
                if button.is_clicked(pygame.mouse.get_pos(), event):
                    if button.action == GAME:
                        game_state = GAME
                    elif button.action == "reset":
                        reset_game()
                        game_state = GAME
                    elif button.action == "quit":
                        running = False
                        
        elif game_state == GAME_OVER:
            for button in final_buttoons:
                if button.is_clicked(pygame.mouse.get_pos(), event):
                    if button.action == "reset":
                        reset_game()
                        game_state = GAME
                    elif button.action == "quit":
                        running = False
                    
        elif game_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    game_state = PAUSE
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    if bullet:
                        bullet.set_image(bullet_img)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        if shoot_sound:
                            shoot_sound.play()
    
    if game_state == GAME:
        for enemy in enemies:
            enemy_bullet = enemy.update()
            if enemy_bullet:
                enemy_bullet.set_image(enemy_bullet_img)
                all_sprites.add(enemy_bullet)
                enemy_bullets.add(enemy_bullet)
        
        all_sprites.update()
    
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            explosion = Explosion(hit.rect.center, 50)
            all_sprites.add(explosion)
            if explosion_sound:
                explosion_sound.play()
            enemy = Enemy()
            enemy.set_image(enemy_img)
            all_sprites.add(enemy)
            enemies.add(enemy)
        
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in hits:
            player.health -= 10
            if hit_sound:
                hit_sound.play()

            if player.health <= 25 and not is_critical_playing and critical_sound:
                critical_sound.play(-1)
                is_critical_playing = True
            
            if player.health <= 0:
                if critical_sound:
                    critical_sound.stop()
                pygame.mixer.music.stop()
                if lost_sound:
                    lost_sound.play()
                game_state = GAME_OVER
        
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 25
            explosion = Explosion(hit.rect.center, 50)
            all_sprites.add(explosion)
            if hit_sound:
                hit_sound.play()
            if explosion_sound:
                explosion_sound.play()
            enemy = Enemy()
            enemy.set_image(enemy_img)
            all_sprites.add(enemy)
            enemies.add(enemy)
            if player.health <= 25 and not is_critical_playing and critical_sound:
                critical_sound.play(-1)
                is_critical_playing = True
            if player.health <= 0:
                if critical_sound:
                    critical_sound.stop()
                pygame.mixer.music.stop()
                if lost_sound:
                    lost_sound.play()
                game_state = GAME_OVER

        hits = pygame.sprite.spritecollide(player, buffs, True)
        for hit in hits:
            if hit.type == 'health':
                player.health = min(100, player.health + 25)
                notification = font.render("+25 здоровья!", True, RED)
            elif hit.type == 'fire_rate':
                player.shoot_delay = int(player.shoot_delay * 0.7)
                notification = font.render("Скорострельность увеличена!", True, RED)
            elif hit.type == 'speed':
                player.speed += 2
                notification = font.render("Скорость повышена!", True, RED)
            
            screen.blit(notification, (WIDTH//2 - notification.get_width()//2, HEIGHT//2 - 50))
            if powerup_sound:
                powerup_sound.play()
            pygame.display.flip()
            pygame.time.delay(1000)
        
        if player.health > 25 and is_critical_playing and critical_sound:
            critical_sound.stop()
            is_critical_playing = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.speed
        if keys[pygame.K_UP]:
            player.rect.y -= player.speed
        if keys[pygame.K_DOWN]:
            player.rect.y += player.speed

        if score >= score_for_next_wave:
            increase_enemies()

    screen.blit(background_img, (0, 0))
    
    if game_state == MENU:
        show_menu()
    elif game_state == GAME:
        all_sprites.draw(screen)
        draw_text(screen, f"Счет: {score}", 24, WIDTH // 2, 10)
        draw_text(screen, f"Уровень: {round((enemy_count-8)/3)+1}", 24, WIDTH // 2, 40)
        draw_health_bar(screen, 5, 5, player.health)
        draw_text(screen, "Жизни:", 24, 50, 30)
    elif game_state == PAUSE:
        all_sprites.draw(screen)
        show_pause_menu()
    elif game_state == GAME_OVER:
        show_game_over(score)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()