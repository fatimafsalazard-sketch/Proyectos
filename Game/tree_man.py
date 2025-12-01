# Importar las bibliotecas necesarias
import pygame
import random
import time

# Inicialización de pygame
pygame.init()

# Configuración de la ventana del juego
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TreeMan - El Árbol Aventura")

# Definición de colores (RGB)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 235)

# Tamaños de los objetos del juego
TREE_SIZE = 30
ACHAS_SIZE = 25
POINT_SIZE = 15

# Control de FPS
FPS = 30
clock = pygame.time.Clock()

# Fuente para textos
font = pygame.font.SysFont("Arial", 30)

# Carga y escalado de imágenes
tree_img = pygame.image.load('tree.png')
tree_img = pygame.transform.scale(tree_img, (60, 60))

tree2_img = pygame.image.load('tree2.png')
tree2_img = pygame.transform.scale(tree2_img, (60, 60))

acha_img = pygame.image.load('acha.png')
acha_img = pygame.transform.scale(acha_img, (50, 50))

agua_img = pygame.image.load('agua.png')
agua_img = pygame.transform.scale(agua_img, (30, 30))

sol_img = pygame.image.load('sol.png')
sol_img = pygame.transform.scale(sol_img, (30, 30))

semilla_img = pygame.image.load('semilla.png')
semilla_img = pygame.transform.scale(semilla_img, (30, 30))

background_img = pygame.image.load('background.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

menu_background_img = pygame.image.load('menu_background.jpg')
menu_background_img = pygame.transform.scale(menu_background_img, (WIDTH, HEIGHT))

menu_background1_img = pygame.image.load('menu_background1.jpg')
menu_background1_img = pygame.transform.scale(menu_background1_img, (WIDTH, HEIGHT))

# Sonidos
pick_sound = pygame.mixer.Sound('pick_sound.wav')
collision_sound = pygame.mixer.Sound('collision_sound.wav')
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1, 0.0)  # Música de fondo en bucle

# Función para guardar el puntaje y acción del jugador
def save_score(score, action, player_name):
    with open("game_scores.txt", "a") as file:
        file.write(f"Jugador: {player_name} - Puntaje: {score} - Acción: {action}\n")

# Clase del jugador (el árbol)
class Tree:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.size = TREE_SIZE
        self.image = image
        self.speed = 5
        self.lives = 3

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        screen.blit(self.image, (self.x - self.size, self.y - self.size))

    def collide(self, obj):
        return abs(self.x - obj.x) < self.size and abs(self.y - obj.y) < self.size

# Clase de las hachas enemigas
class Acha:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = ACHAS_SIZE
        self.image = acha_img
        self.speed = 2

    # Las hachas se mueven hacia el árbol
    def move(self, target_x, target_y):
        if self.x < target_x:
            self.x += self.speed
        elif self.x > target_x:
            self.x -= self.speed
        if self.y < target_y:
            self.y += self.speed
        elif self.y > target_y:
            self.y -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x - self.size, self.y - self.size))

# Clase de los puntos recolectables (agua, sol, semilla)
class Point:
    def __init__(self, x, y, image, type):
        self.x = x
        self.y = y
        self.size = POINT_SIZE
        self.image = image
        self.type = type  # "Agua", "Sol" o "Semilla"

    def draw(self):
        screen.blit(self.image, (self.x - self.size / 2, self.y - self.size / 2))

# Mostrar la puntuación, vidas y nivel en pantalla
def draw_ui(tree, score, level):
    score_text = font.render(f"Puntuación: {score}", True, BLUE)
    lives_text = font.render(f"Vidas: {tree.lives}", True, RED)
    level_text = font.render(f"Nivel: {level}", True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))

# Pantalla de fin del juego
def game_over(score, player_name):
    screen.blit(background_img, (0, 0))
    game_over_text = font.render("¡Juego Terminado!", True, RED)
    score_text = font.render(f"Puntuación Final: {score}", True, BLUE)
    adoption_text = font.render(player_name + "¿Te gustaría adoptar un árbol? (Presiona 'A')", True, GREEN)
    restart_text = font.render("Presiona [ENTER] para reiniciar o [ESC] para salir", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
    screen.blit(adoption_text, (WIDTH // 2 - adoption_text.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))
    pygame.display.update()

    # Esperar a que el jugador elija una opción
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    save_score(score, "Adoptó un árbol", player_name)
                    thank_you_text = font.render("¡Gracias por adoptar un árbol!", True, LIGHT_BLUE)
                    screen.blit(background_img, (0, 0))
                    screen.blit(thank_you_text, (WIDTH // 2 - thank_you_text.get_width() // 2, HEIGHT // 2))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    waiting = False
                    start_menu()
                elif event.key == pygame.K_RETURN:
                    waiting = False
                    start_menu()
                elif event.key == pygame.K_ESCAPE:
                    save_score(score, "Abandonó sin adoptar", player_name)
                    pygame.quit()
                    quit()

# Función principal del juego
def game(player_name, selected_image):
    tree = Tree(WIDTH // 2, HEIGHT // 2, selected_image)
    achas = [Acha(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(4)]
    points = [
        Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), agua_img, "Agua"),
        Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), sol_img, "Sol"),
        Point(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), semilla_img, "Semilla")
    ]

    score = 0
    level = 1
    level_up_score = 50
    running = True
    last_point_move_time = time.time()

    # Bucle principal del juego
    while running:
        screen.blit(background_img, (0, 0))

        # Eventos de salida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: tree.move(-tree.speed, 0)
        if keys[pygame.K_RIGHT]: tree.move(tree.speed, 0)
        if keys[pygame.K_UP]: tree.move(0, -tree.speed)
        if keys[pygame.K_DOWN]: tree.move(0, tree.speed)

        # Mover puntos cada 10 segundos
        if time.time() - last_point_move_time > 10:
            for point in points:
                point.x = random.randint(50, WIDTH - 50)
                point.y = random.randint(50, HEIGHT - 50)
            last_point_move_time = time.time()

        # Movimiento de hachas hacia el árbol
        for acha in achas:
            acha.move(tree.x, tree.y)

        # Colisiones entre árbol y puntos
        for point in points[:]:
            if tree.collide(point):
                points.remove(point)
                if point.type == "Agua": score += 10
                elif point.type == "Sol": score += 15
                elif point.type == "Semilla": score += 20; tree.speed += 1
                pick_sound.play()
                # Añadir nuevo punto
                points.append(Point(
                    random.randint(50, WIDTH - 50),
                    random.randint(50, HEIGHT - 50),
                    random.choice([agua_img, sol_img, semilla_img]),
                    random.choice(["Agua", "Sol", "Semilla"])))

        # Subida de nivel
        if score >= level * level_up_score:
            level += 1
            for acha in achas:
                acha.speed += 1

        # Colisión con hachas
        for acha in achas:
            if tree.collide(acha):
                tree.lives -= 1
                collision_sound.play()
                if tree.lives <= 0:
                    game_over(score, player_name)
                    running = False
                else:
                    tree.x, tree.y = WIDTH // 2, HEIGHT // 2  # Reinicio posición

        # Dibujar interfaz y objetos
        draw_ui(tree, score, level)
        tree.draw()
        for acha in achas:
            acha.draw()
        for point in points:
            point.draw()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

# Función para pedir nombre del jugador
def ask_player_name():
    input_active = True
    player_name = ""
    input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 1, 300, 50)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive
    font_input = pygame.font.SysFont("Arial", 28)

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip() != "":
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    if event.unicode.isalpha() or event.unicode == " ":
                        if len(player_name) < 20:
                            player_name += event.unicode

        screen.blit(menu_background1_img, (0, 0))

        prompt = font_input.render("Ingresa tu nombre:", True, BLUE)
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 250))

        input_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 250 + 40 + 10, 300, 40)
        txt_surface = font_input.render(player_name, True, color)
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 10))
        pygame.draw.rect(screen, color, input_rect, 2)

        pygame.display.flip()
        clock.tick(30)

    return player_name

# Selección de personaje
def select_character():
    selecting = True
    option_font = pygame.font.SysFont("Arial", 28)
    while selecting:
        screen.blit(background_img, (0, 0))
        msg = font.render("Selecciona tu personaje (1 o 2):", True, BLACK)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 3))
        screen.blit(tree_img, (WIDTH // 4 - 30, HEIGHT // 2))
        screen.blit(tree2_img, (3 * WIDTH // 4 - 30, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return tree_img
                elif event.key == pygame.K_2:
                    return tree2_img

# Menú principal
def start_menu():
    screen.blit(menu_background_img, (0, 0))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

    player_name = ask_player_name()
    selected_image = select_character()
    game(player_name, selected_image)

# Ejecutar el juego desde el menú principal
if __name__ == "__main__":
    start_menu()
