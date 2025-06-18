import pygame, os, random
import speech_recognition as sr
from datetime import datetime

# Inicializações pygame
pygame.init()
tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
relogio = pygame.time.Clock()
pygame.display.set_caption("Sans fight")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (180, 180, 180)
vermelho = (255, 0, 0)

# Fontes
fonte = pygame.font.Font(os.path.join("Recursos", "press_start.ttf"), 20)
fonte_grande = pygame.font.Font(os.path.join("Recursos", "press_start.ttf"), 60)

def desenhar_texto(texto, fonte, cor, surface, x, y):
    render = fonte.render(texto, True, cor)
    surface.blit(render, (x, y))

def pedir_nome_por_voz():
    recognizer = sr.Recognizer()
    microfone = sr.Microphone()
    nome_capturado = None
    tentando = True

    while tentando:
        tela.fill(preto)
        desenhar_texto("Fale seu nome após o sinal sonoro...", fonte_grande, branco, tela, 100, 250)
        desenhar_texto("Aperte ESC para cancelar", fonte, cinza, tela, 10, 650)
        pygame.display.update()

        pygame.time.delay(1000)

        try:
            with microfone as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Ouvindo...")
                audio = recognizer.listen(source, timeout=5)
                print("Processando...")
                nome_capturado = recognizer.recognize_google(audio, language='pt-BR')
                print("Nome capturado:", nome_capturado)
                tentando = False
        except sr.WaitTimeoutError:
            print("Nenhuma fala detectada. Tente novamente.")
        except sr.UnknownValueError:
            print("Não entendi. Tente novamente.")
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento: {e}")
            tentando = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                tentando = False

    return nome_capturado

def tela_game_over(nome, pontos):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        tela.fill(preto)

        texto_game_over = fonte_grande.render("GAME OVER", True, vermelho)
        texto_nome = fonte.render(f"Jogador: {nome}", True, branco)
        texto_pontos = fonte.render(f"Pontos: {pontos}", True, branco)
        texto_data = fonte.render(f"Data/Hora: {data_hora}", True, branco)
        texto_sair = fonte.render("Feche a janela para sair", True, cinza)

        tela.blit(texto_game_over, ((tamanho[0] - texto_game_over.get_width()) // 2, 150))
        tela.blit(texto_nome, ((tamanho[0] - texto_nome.get_width()) // 2, 250))
        tela.blit(texto_pontos, ((tamanho[0] - texto_pontos.get_width()) // 2, 300))
        tela.blit(texto_data, ((tamanho[0] - texto_data.get_width()) // 2, 350))
        tela.blit(texto_sair, ((tamanho[0] - texto_sair.get_width()) // 2, 600))

        pygame.display.update()
        relogio.tick(30)

# -- Programa principal --

nome = pedir_nome_por_voz()
if not nome:
    nome = "Jogador"

vida = 5
pontuacao = 0

# Carregar imagens
sansVoador = pygame.image.load(os.path.join("Recursos", "sans.png"))
sansVoador = pygame.transform.scale(sansVoador, (380, 350))
sansVoador_rect = sansVoador.get_rect(midbottom=(tamanho[0] // 2, 270))
sans_velocidade_x = 2

jogador = pygame.image.load(os.path.join("Recursos", "jogador.png"))
jogador = pygame.transform.scale(jogador, (30, 30))
jogadorRect = jogador.get_rect()
jogadorRect.topleft = (30, 30)

osso = pygame.image.load(os.path.join("Recursos", "osso.png"))
osso = pygame.transform.scale(osso, (120, 100))

ossoLongo = pygame.image.load(os.path.join("Recursos", "ossoLongo.png"))
ossoLongo = pygame.transform.scale(ossoLongo, (110, 170))

ossoAzul = pygame.image.load(os.path.join("Recursos", "osso_azul.png"))
ossoAzul = pygame.transform.scale(ossoAzul, (150, 680))

velocidade = 5
velocidade_osso = 7.0
ossos = []
SPAWN_EVENTO = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENTO, 1000)
pausado = False

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
            tipo = random.choice(["curto", "longo"])
            if pontuacao > 0 and pontuacao % 40 == 0:
                ossos.append({
                    "imagem": ossoAzul,
                    "rect": ossoAzul.get_rect(topleft=(1000, 205)),
                    "tipo": "azul"
                })
            elif tipo == "curto":
                altura_osso = osso.get_height()
                y_random = random.randint(205, tamanho[1] - altura_osso)
                ossos.append({
                    "imagem": osso,
                    "rect": osso.get_rect(topleft=(1000, y_random)),
                    "tipo": "curto"
                })
            else:
                altura_ossoLongo = ossoLongo.get_height()
                y_random = random.randint(205, tamanho[1] - altura_ossoLongo)
                ossos.append({
                    "imagem": ossoLongo,
                    "rect": ossoLongo.get_rect(topleft=(1000, y_random)),
                    "tipo": "longo"
                })

    if not pausado:
        teclas = pygame.key.get_pressed()
        movendo = teclas[pygame.K_w] or teclas[pygame.K_UP] or teclas[pygame.K_s] or teclas[pygame.K_DOWN]

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            jogadorRect.y -= velocidade
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            jogadorRect.y += velocidade

        # Limitar movimento vertical entre y = 205 e y = 700
        jogadorRect.y = max(205, min(tamanho[1] - jogadorRect.height, jogadorRect.y))

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
            tela_game_over(nome, pontuacao)

        # Movimento horizontal do Sans
        sansVoador_rect.x += sans_velocidade_x
        if sansVoador_rect.left <= 0 or sansVoador_rect.right >= tamanho[0]:
            sans_velocidade_x *= -1
        sansVoador_rect.bottom = 270  # manter fixo na linha

    tela.fill(preto)

    # Linha branca entre y = 200 e y = 205
    pygame.draw.rect(tela, branco, pygame.Rect(0, 200, tamanho[0], 5))

    tela.blit(sansVoador, sansVoador_rect)
    tela.blit(jogador, jogadorRect)
    for o in ossos:
        tela.blit(o["imagem"], o["rect"])

    tela.blit(fonte.render(f"VIDA: {vida}", True, branco), (10, 10))
    tela.blit(fonte.render(f"PONTOS: {pontuacao}", True, branco), (10, 40))
    tela.blit(fonte.render(f"VEL: {velocidade_osso:.1f}", True, branco), (10, 70))
    tela.blit(fonte.render("Press SPACE to Pause", True, cinza), (780, 10))

    if pausado:
        texto_pause = fonte_grande.render("PAUSE", True, branco)
        tela.blit(texto_pause, ((tamanho[0] - texto_pause.get_width()) // 2,
                                (tamanho[1] - texto_pause.get_height()) // 2))

    pygame.display.update()
    relogio.tick(60)
