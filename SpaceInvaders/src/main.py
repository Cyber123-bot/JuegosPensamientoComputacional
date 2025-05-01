# Importación de las librerías necesarias
import pygame

# Constantes del juego
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 31, 0)
GREEN = (0, 200, 0)
BULLET_COLOR = (0, 0, 255)

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
ENEMY_WIDTH, ENEMY_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 10, 30

PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 7

ENEMY_ROWS = 3
ENEMY_COLS = 10
MOVE_DELAY = 5  # Frames entre movimientos

# Configuraciones iniciales
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Cargamos y redimensionamos las imágenes
PLAYER_IMAGE = pygame.image.load(r"..\Images\rocket.png")
ENEMY_IMAGE = pygame.image.load(r"..\Images\ovni.png")
BACKGROUND_IMAGE = pygame.image.load(r"..\Images\background.png")

PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Clases del juego
class Player:
    def __init__(self):
        self.x = WIDTH // 2 - 25  # Centrado en X
        self.y = HEIGHT - PLAYER_HEIGHT - 10  # Parte inferior
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= PLAYER_SPEED
        elif direction == "right" and self.x < WIDTH - self.width:
            self.x += PLAYER_SPEED

    def draw(self):
        screen.blit(PLAYER_IMAGE, (self.x, self.y))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        screen.blit(ENEMY_IMAGE, (self.x, self.y))

# Inicialización del jugador
player = Player()

# Listas de balas y enemigos
bullets = []
enemies = []

# Creación de enemigos
for row in range(ENEMY_ROWS):
    for col in range(ENEMY_COLS):
        x = col * (ENEMY_WIDTH + 10) + 50
        y = row * (ENEMY_HEIGHT + 10) + 50
        enemies.append(Enemy(x, y))

score = 0
font = pygame.font.Font(None, 36)
move_timer = 0
game_over = False
win = False
end_of_game = False

# Ciclo de juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            end_of_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = pygame.Rect(
                    player.x + player.width//2 - BULLET_WIDTH//2,
                    player.y - BULLET_HEIGHT,
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                )
                bullets.append(bullet_rect)

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")

    # Movimiento de balas
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Movimiento de enemigos con temporizador
    move_timer += 1
    if move_timer >= MOVE_DELAY:
        for enemy in enemies:
            enemy.x += ENEMY_SPEED
        move_timer = 0

        # Verificación de bordes
        edge_hit = False
        for enemy in enemies:
            if enemy.x <= 0 or enemy.x + enemy.width >= WIDTH:
                edge_hit = True
                break

        if edge_hit:
            ENEMY_SPEED *= -1
            for enemy in enemies:
                enemy.y += 30

    # Colisiones bala-enemigo
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy.get_rect()):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10

    # Colisión jugador-enemigo
    for enemy in enemies:
        if player.get_rect().colliderect(enemy.get_rect()):
            game_over = True

    # Victoria
    if not enemies:
        win = True
        break

    # Renderizado
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    player.draw()
    
    for bullet in bullets:
        pygame.draw.rect(screen, BULLET_COLOR, bullet)
    
    for enemy in enemies:
        enemy.draw()
    
    # Puntaje
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

# Pantallas finales
screen.blit(BACKGROUND_IMAGE, (0, 0))
if win:
    text = font.render("¡Ganaste!", True, GREEN)

elif game_over and end_of_game:
    text = font.render("¡Adios!", True, WHITE)

elif game_over:
    text = font.render("Perdiste", True, RED)

screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
pygame.display.flip()
pygame.time.delay(2000)
pygame.quit()