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
jogador = pygame.transform.scale(jogador, (40, 40))
jogadorRect = jogador.get_rect()
jogadorRect.topleft = (10, 350)

# Velocidade de movimento
velocidade = 5

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Teclas pressionadas
    teclas = pygame.key.get_pressed()

    # Movimento para cima
    if teclas[pygame.K_w] or teclas[pygame.K_UP]:
        jogadorRect.y -= velocidade

    # Movimento para baixo
    if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
        jogadorRect.y += velocidade

    # Impede que o jogador saia da tela
    if jogadorRect.top < 0:
        jogadorRect.top = 0
    if jogadorRect.bottom > tamanho[1]:
        jogadorRect.bottom = tamanho[1]

    # Desenho da tela
    tela.fill(preto)
    tela.blit(jogador, jogadorRect)

    pygame.display.update()
    relogio.tick(60)
