import pygame, os, random

# Inicializações
pygame.init()
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
relogio = pygame.time.Clock()
pygame.display.set_caption("Sans fight")

# Cores
preto = (0, 0, 0)

# Carregar imagens e redimensionar
sansVoador = pygame.image.load(os.path.join("Recursos", "sans.png"))
sansVoador = pygame.transform.scale(sansVoador, (100, 100))

jogador = pygame.image.load(os.path.join("Recursos", "jogador.png"))
jogador = pygame.transform.scale(jogador, (50, 50))
jogadorRect = jogador.get_rect()
jogadorRect.topleft = (10, 350)

osso = pygame.image.load(os.path.join("Recursos", "osso.png"))
osso = pygame.transform.scale(osso, (100, 100))

ossoLongo = pygame.image.load(os.path.join("Recursos", "ossoLongo.png"))
ossoLongo = pygame.transform.scale(ossoLongo, (100, 300))

# Velocidade de movimento
velocidade = 5
velocidade_osso = 7

# Lista de ossos ativos
ossos = []

# Timer para spawn de ossos
SPAWN_EVENTO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENTO, 1000)  # a cada 1 segundo

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == SPAWN_EVENTO:
            y_random = random.randint(0, 600)
            tipo = random.choice(["curto", "longo"])
            if tipo == "curto":
                ossos.append({"imagem": osso, "rect": osso.get_rect(topleft=(1000, y_random))})
            else:
                ossos.append({"imagem": ossoLongo, "rect": ossoLongo.get_rect(topleft=(1000, y_random))})

    # Teclas pressionadas
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        jogadorRect.y -= velocidade
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        jogadorRect.y += velocidade

    # Limites da tela
    if jogadorRect.top < 0:
        jogadorRect.top = 0
    if jogadorRect.bottom > tamanho[1]:
        jogadorRect.bottom = tamanho[1]

    # Atualizar posição dos ossos
    for o in ossos:
        o["rect"].x -= velocidade_osso

    # Remover ossos que saíram da tela
    ossos = [o for o in ossos if o["rect"].right > 0]

    # Desenho da tela
    tela.fill(preto)
    tela.blit(jogador, jogadorRect)

    for o in ossos:
        tela.blit(o["imagem"], o["rect"])

    pygame.display.update()
    relogio.tick(60)
