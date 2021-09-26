import random
import sys
import pygame
import os


WIDTH = 1100
HEIGHT = 800

backgroundColor = "#000000"
padelColor = "#ff8629"
ballColor = "#7bff00"
timeColor = "#ffab6b"
FPS = 60
# backgroundColor = "#282a36"
# padelColor = "#f8f8f2"
# ballColor = "#ff79c6"
# timeColor = "#bd93f9"
# FPS = 60


class PongGame:
    def __init__(self):
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))
        self.padel_speed_left = 0
        self.padel_speed_right = 0
        self.scoreL = 0
        self.scoreR = 0
        self.speed = 15 # change this for padel speed
        self.padel_width = 12 # change this for padel width
        self.leftP = pygame.Rect(3, HEIGHT / 2, self.padel_width, 140) # x, y, width, height
        self.rightP = pygame.Rect((WIDTH - self.padel_width) - 3, HEIGHT / 2, self.padel_width, 140)
        self.ball = pygame.Rect(WIDTH / 2 - 8, HEIGHT / 2 - 8, 18, 18)
        self.score_time = True

    def score(self):
        if self.ball.left <= 0:
            self.score_time = pygame.time.get_ticks()
            self.scoreR += 1
        if self.ball.right >= WIDTH:
            self.score_time = pygame.time.get_ticks()
            self.scoreL += 1

    def ball_reset(self):
        self.ball.center = ((WIDTH / 2)-(self.ball.width/2),
                            (HEIGHT / 2)-(self.ball.height/2))
        current_time = pygame.time.get_ticks()
        # countdown
        if current_time - self.score_time < 700:
            number_three = game_font.render("3", True, timeColor)
            screen.blit(number_three, (WIDTH / 2 - 10, HEIGHT / 2 + 20))
        if 700 < current_time - self.score_time < 1400:
            number_two = game_font.render("2", True, timeColor)
            screen.blit(number_two, (WIDTH / 2 - 10, HEIGHT / 2 + 20))
        if 1400 < current_time - self.score_time < 2100:
            number_one = game_font.render("1", True, timeColor)
            screen.blit(number_one, (WIDTH / 2 - 10, HEIGHT / 2 + 20))
        # ctrl+v
        if current_time - self.score_time < 2100:
            self.speed_y, self.speed_x = 0, 0
        else:
            self.speed_x = 7 * random.choice((1, -1))
            self.speed_y = 7 * random.choice((1, -1))
            self.score_time = None

    def ball_movement(self):
        if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
            self.speed_y *= -1
        if self.ball.left <= 0 or self.ball.right >= WIDTH:
            sound_ball.play()
            self.score()
            self.ball_reset()
        # checks collision
        if self.ball.colliderect(self.leftP) and self.ball.x:
            self.speed_x *= -1
            sound_padel.play()
        if self.ball.colliderect(self.rightP) and self.ball.x:
            self.speed_x *= -1
            sound_padel.play()

    def end_border(self):
        if self.leftP.top <= 0:
            self.leftP.top = 0
        if self.leftP.bottom >= HEIGHT:
            self.leftP.bottom = HEIGHT

        if self.rightP.top <= 0:
            self.rightP.top = 0
        if self.rightP.bottom >= HEIGHT:
            self.rightP.bottom = HEIGHT

    def text_surf(self):
        # score of leftPlayer
        score_surf = game_font.render(str(self.scoreL), True, padelColor)
        score_rect = score_surf.get_rect(center=((WIDTH/2)/2, 70))
        screen.blit(score_surf, score_rect)
        # score of rightPlayer
        score_surf = game_font.render(str(self.scoreR), True, padelColor)
        score_rect = score_surf.get_rect(center=(((WIDTH/2)/2)+(WIDTH/2), 70))
        screen.blit(score_surf, score_rect)

    def draw_obj(self):
        self.rightP.x = WIDTH - self.padel_width - 3 # for perfect placement when screen in resized.
        pygame.draw.rect(screen, padelColor, self.leftP)
        pygame.draw.rect(screen, padelColor, self.rightP)
        pygame.draw.ellipse(screen, ballColor, self.ball)

    def draw_line(self):
        start_pos = [WIDTH / 2, 0]
        line_lenth = 10
        end_pos = [start_pos[0], start_pos[1] + line_lenth]
        gap = line_lenth
        while end_pos[1] <= HEIGHT:
            pygame.draw.line(screen, padelColor, start_pos, end_pos, width=2)
            start_pos[1] += (line_lenth+gap)
            end_pos[1] += (line_lenth+gap)

    def handle_movement_speed(self):
        # moving the ball
        self.ball.x += self.speed_x
        self.ball.y += self.speed_y
        self.leftP.y += self.padel_speed_left
        self.rightP.y += self.padel_speed_right

    def handle_keyboard(self):
        # leftPadel key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.padel_speed_left -= self.speed
            if event.key == pygame.K_s:
                self.padel_speed_left += self.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.padel_speed_left += self.speed
            if event.key == pygame.K_s:
                self.padel_speed_left -= self.speed
        # rightPadel key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.padel_speed_right -= self.speed
            if event.key == pygame.K_DOWN:
                self.padel_speed_right += self.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.padel_speed_right += self.speed
            if event.key == pygame.K_DOWN:
                self.padel_speed_right -= self.speed


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
game_font = pygame.font.Font('FFFFORWA.ttf', 23)
# Sound
sound_padel = pygame.mixer.Sound('sfx\\hit.wav')
sound_ball = pygame.mixer.Sound('sfx\\blip.wav')
pong_game = PongGame()

while True:
    screen.fill(backgroundColor)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        pong_game.handle_keyboard()
    WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    pong_game.text_surf()
    pong_game.ball_movement()
    pong_game.end_border()
    pong_game.draw_obj()
    pong_game.draw_line()

    if pong_game.score_time:
        pong_game.ball_reset()
    pong_game.handle_movement_speed()
    pygame.display.update()
    clock.tick(FPS)
