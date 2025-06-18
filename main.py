import pygame, os, random

# Inicializações
pygame.init()
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
relogio = pygame.time.Clock()
pygame.display.set_caption("Sans fight")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (180, 180, 180)

# Vida e pontuação
vida = 5
pontuacao = 0

# Fontes
fonte = pygame.font.Font(os.path.join("Recursos", "press_start.ttf"), 20)
fonte_grande = pygame.font.Font(os.path.join("Recursos", "press_start.ttf"), 60)

# Estado de pausa
pausado = False

# Carregar imagens
sansVoador = pygame.image.load(os.path.join("Recursos", "sans.png"))
sansVoador = pygame.transform.scale(sansVoador, (100, 100))

jogador = pygame.image.load(os.path.join("Recursos", "jogador.png"))
jogador = pygame.transform.scale(jogador, (50, 50))
jogadorRect = jogador.get_rect()
jogadorRect.topleft = (10, 350)

osso = pygame.image.load(os.path.join("Recursos", "osso.png"))
osso = pygame.transform.scale(osso, (100, 100))

ossoLongo = pygame.image.load(os.path.join("Recursos", "ossoLongo.png"))
ossoLongo = pygame.transform.scale(ossoLongo, (80, 170))

ossoAzul = pygame.image.load(os.path.join("Recursos", "osso_azul.png"))
ossoAzul = pygame.transform.scale(ossoAzul, (80, 700))  # Ocupa toda altura (350 para cima e 350 para baixo)

# Velocidade
velocidade = 5
velocidade_osso = 7.0

# Lista de ossos ativos
ossos = []

# Timer para spawn de ossos
SPAWN_EVENTO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENTO, 1000)

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                pausado = not pausado

        elif evento.type == SPAWN_EVENTO and not pausado:
            y_random = random.randint(0, 600)
            tipo = random.choice(["curto", "longo"])

            if pontuacao > 0 and pontuacao % 40 == 0:
                # Osso azul nasce fixo na vertical, ocupando toda a altura da tela
                ossos.append({
                    "imagem": ossoAzul,
                    "rect": ossoAzul.get_rect(topleft=(1000, 0)),  # Sempre no topo da tela
                    "tipo": "azul"
                })
            elif tipo == "curto":
                ossos.append({
                    "imagem": osso,
                    "rect": osso.get_rect(topleft=(1000, y_random)),
                    "tipo": "curto"
                })
            else:
                ossos.append({
                    "imagem": ossoLongo,
                    "rect": ossoLongo.get_rect(topleft=(1000, y_random)),
                    "tipo": "longo"
                })

    if not pausado:
        # Detectar teclas
        teclas = pygame.key.get_pressed()
        movendo = teclas[pygame.K_w] or teclas[pygame.K_UP] or teclas[pygame.K_s] or teclas[pygame.K_DOWN]

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            jogadorRect.y -= velocidade
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            jogadorRect.y += velocidade

        # Limites da tela
        jogadorRect.y = max(0, min(tamanho[1] - jogadorRect.height, jogadorRect.y))

        # Atualizar ossos
        ossos_remover = []
        for o in ossos:
            o["rect"].x -= velocidade_osso

            if jogadorRect.colliderect(o["rect"]):
                if o["tipo"] == "azul":
                    if movendo:
                        vida -= 1
                        ossos_remover.append(o)
                else:
                    vida -= 1
                    ossos_remover.append(o)

            elif o["rect"].right <= 0:
                pontuacao += 1
                velocidade_osso += 0.1
                ossos_remover.append(o)

        for o in ossos_remover:
            ossos.remove(o)

        if vida <= 0:
            print("GAME OVER")
            pygame.quit()
            exit()

    # Desenhar fundo
    tela.fill(preto)

    # Desenhar jogador e ossos
    tela.blit(jogador, jogadorRect)
    for o in ossos:
        tela.blit(o["imagem"], o["rect"])

    # HUD: Vida, Pontuação, Velocidade
    tela.blit(fonte.render(f"VIDA: {vida}", True, branco), (10, 10))
    tela.blit(fonte.render(f"PONTOS: {pontuacao}", True, branco), (10, 40))
    tela.blit(fonte.render(f"VEL: {velocidade_osso:.1f}", True, branco), (10, 70))
    tela.blit(fonte.render("Press SPACE to Pause", True, cinza), (700, 10))

    # Pausa
    if pausado:
        texto_pause = fonte_grande.render("PAUSE", True, branco)
        tela.blit(texto_pause, ((tamanho[0] - texto_pause.get_width()) // 2,
                                (tamanho[1] - texto_pause.get_height()) // 2))

    pygame.display.update()
    relogio.tick(60)
