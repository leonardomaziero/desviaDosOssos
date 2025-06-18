import pygame, os, random
import speech_recognition as sr
from datetime import datetime
import pyttsx3
import threading
import time
import math
import sys


def exit():
    pygame.quit()
    sys.exit()
    
pygame.init()
pygame.mixer.init()

tamanho = (1000, 700)
tela = pygame.display.set_mode(tamanho)
relogio = pygame.time.Clock()
pygame.display.set_caption("Dodge the bones!")

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (180, 180, 180)
vermelho = (255, 0, 0)

# Fontes
fonte = pygame.font.Font(os.path.join("Recursos", "press_start.ttf"), 20)
fonte_grande = pygame.font.Font(os.path.join("Recursos", "press_start.ttf"), 40)

# Carregar sons
som_dano = pygame.mixer.Sound(os.path.join("Recursos", "dano.ogg"))
mus_menu = os.path.join("Recursos", "mus_menu1.ogg")
mus_jogo = os.path.join("Recursos", "soundtrack_jogo.ogg")
mus_gameover = os.path.join("Recursos", "mus_intronoise.ogg")

# Inicializa pyttsx3 e configura voz masculina e mais grave
engine = pyttsx3.init()
engine.setProperty('rate', 120)  # voz mais lenta e grave
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')

voz_masculina_id = None
for voice in voices:
    nome_voze = voice.name.lower()
    if 'male' in nome_voze or 'homem' in nome_voze:
        voz_masculina_id = voice.id
        break
if voz_masculina_id is None:
    voz_masculina_id = voices[0].id
engine.setProperty('voice', voz_masculina_id)

frases_sans = [
    "Você já está cansado?",
    "Você não vai conseguir",
    "Você não vai desviar do próximo osso"
]

sans_falando = False
frase_atual = ""

def sans_fala(frase):
    global sans_falando, frase_atual
    frase_atual = frase
    def falar():
        global sans_falando
        sans_falando = True
        pygame.mixer.music.pause()
        engine.say(frase)
        engine.runAndWait()
        time.sleep(2)
        pygame.mixer.music.unpause()
        sans_falando = False
    threading.Thread(target=falar, daemon=True).start()

def desenhar_texto(texto, fonte, cor, surface, x, y):
    render = fonte.render(texto, True, cor)
    surface.blit(render, (x, y))

def salvar_pontuacao(nome, pontos):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log.dat", "a") as f:
        f.write(f"{nome},{pontos},{data_hora}\n")

def carregar_pontuacoes():
    try:
        with open("log.dat", "r") as f:
            linhas = f.readlines()
            pontuacoes = []
            for linha in linhas:
                partes = linha.strip().split(",")
                if len(partes) == 3:
                    nome, pontos, data = partes
                    pontuacoes.append((nome, int(pontos), data))
            pontuacoes.sort(key=lambda x: x[1], reverse=True)
            return pontuacoes[:5]
    except FileNotFoundError:
        return []

def tela_ranking():
    mostrando = True
    ranking = carregar_pontuacoes()

    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False

        tela.fill(preto)

        texto_titulo = fonte_grande.render("Ranking - Top 5", True, branco)
        tela.blit(texto_titulo, ((tamanho[0] - texto_titulo.get_width()) // 2, 50))

        if ranking:
            for i, (n, p, d) in enumerate(ranking):
                desenhar_texto(f"{i+1}. {n} - {p} pts ({d})", fonte, branco, tela, 100, 150 + i * 40)
        else:
            desenhar_texto("Nenhuma pontuação registrada.", fonte, branco, tela, 100, 150)

        desenhar_texto("Pressione ESC para voltar", fonte, cinza, tela, 500, 650)

        pygame.display.update()
        relogio.tick(30)

def pedir_nome_por_voz():
    recognizer = sr.Recognizer()
    microfone = sr.Microphone()
    nome_capturado = None
    tentando = True

    while tentando:
        tela.fill(preto)
        desenhar_texto("Fale o nome do jogador!", fonte_grande, branco, tela, 60, 300)
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

def tela_instrucoes():
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    mostrando = False

        tela.fill(preto)
        desenhar_texto("Instruções do Jogo:", fonte_grande, branco, tela, 170, 80)
        instrucoes = [
            "Use W / S ou SETAS para mover para cima/baixo",
            "Evite ossos normais e longos",
            "O osso AZUL só te atinge se você se mover",
            "Cada osso evitado = +1 ponto",
            "Pressione ESPAÇO para pausar",
            "O jogo acaba quando a vida zera",
            "",
            "Pressione ENTER para continuar"
        ]
        for i, linha in enumerate(instrucoes):
            desenhar_texto(linha, fonte, branco, tela, 60, 200 + i * 40)

        pygame.display.update()
        relogio.tick(30)

def tela_game_over(nome, pontos):
    tocar_musica(mus_gameover)  # Toca música de game over
    salvar_pontuacao(nome, pontos)
    ranking = carregar_pontuacoes()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mostrando = True

    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                mostrando = False
                parar_musica()  # Para música do game over ao sair

        tela.fill(preto)

        texto_game_over = fonte_grande.render("GAME OVER", True, vermelho)
        tela.blit(texto_game_over, ((tamanho[0] - texto_game_over.get_width()) // 2, 50))

        desenhar_texto(f"Jogador: {nome}", fonte, branco, tela, 50, 150)
        desenhar_texto(f"Pontos: {pontos}", fonte, branco, tela, 50, 180)
        desenhar_texto(f"Data: {data_hora}", fonte, branco, tela, 50, 210)

        desenhar_texto("Top 5 Pontuações:", fonte, branco, tela, 50, 260)
        for i, (n, p, d) in enumerate(ranking):
            desenhar_texto(f"{i+1}. {n} - {p} pts ({d})", fonte, branco, tela, 50, 300 + i * 30)

        desenhar_texto("Pressione ESC para voltar ao menu", fonte, cinza, tela, 50, 600)

        pygame.display.update()
        relogio.tick(30)

def menu_inicial():
    tocar_musica(mus_menu)  # toca música do menu ao entrar
    selecionado = 0
    opcoes = ["Jogar", "Ranking", "Sair"]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    parar_musica()  # Para música do menu ao sair da tela
                    return opcoes[selecionado]

        tela.fill(preto)
        titulo = fonte_grande.render("Dodge the bones!", True, branco)
        tela.blit(titulo, ((tamanho[0] - titulo.get_width()) // 2, 100))

        for i, opcao in enumerate(opcoes):
            cor = branco
            if i == selecionado:
                cor = vermelho
            texto_opcao = fonte.render(opcao, True, cor)
            tela.blit(texto_opcao, ((tamanho[0] - texto_opcao.get_width()) // 2, 300 + i * 50))

        desenhar_texto("Use UP/DOWN para navegar e ENTER para selecionar", fonte, cinza, tela, 20, 650)

        pygame.display.update()
        relogio.tick(30)

def tocar_musica(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(-1)  # Loop infinito

def parar_musica():
    pygame.mixer.music.stop()

def jogo():
    global sans_falando, frase_atual

    nome = pedir_nome_por_voz()
    if not nome:
        nome = "Jogador"

    tela_instrucoes()

    tocar_musica(mus_jogo)  # toca música do jogo APÓS nome e instruções

    vida = 5
    pontuacao = 0

    sansVoador = pygame.image.load(os.path.join("Recursos", "sans.png"))
    sansVoador = pygame.transform.scale(sansVoador, (380, 350))
    sansVoador_rect = sansVoador.get_rect(midbottom=(tamanho[0] // 2, 270))
    sans_velocidade_x = 2

    jogador = pygame.image.load(os.path.join("Recursos", "jogador.png"))
    jogador = pygame.transform.scale(jogador, (30, 30))
    jogadorRect = jogador.get_rect()
    jogadorRect.topleft = (10, 205)
    jogadorRect.inflate_ip(-10, -10)  # HITBOX AJUSTADA

    osso = pygame.image.load(os.path.join("Recursos", "osso.png"))
    osso = pygame.transform.scale(osso, (120, 100))

    ossoLongo = pygame.image.load(os.path.join("Recursos", "ossoLongo.png"))
    ossoLongo = pygame.transform.scale(ossoLongo, (110, 170))

    ossoAzul = pygame.image.load(os.path.join("Recursos", "osso_azul.png"))
    ossoAzul = pygame.transform.scale(ossoAzul, (120, 680))

    velocidade = 5
    velocidade_osso = 7.0
    ossos = []
    SPAWN_EVENTO = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENTO, 1000)
    pausado = False

    # Variáveis para lua pulsante
    import math
    lua_base_raio = 30
    tempo_inicial = time.time()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                    if pausado:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
            elif evento.type == SPAWN_EVENTO and not pausado:
                tipo = random.choice(["curto", "longo"])
                if pontuacao > 0 and pontuacao % 60 == 0:
                    frase_aleatoria = random.choice(frases_sans)
                    sans_fala(frase_aleatoria)
                    rect_azul = ossoAzul.get_rect(topleft=(1000, 205)).inflate(-60, -40)  # HITBOX AJUSTADA
                    ossos.append({"imagem": ossoAzul, "rect": rect_azul, "tipo": "azul"})
                elif tipo == "curto":
                    altura_osso = osso.get_height()
                    y_random = random.randint(205, tamanho[1] - altura_osso)
                    rect_curto = osso.get_rect(topleft=(1000, y_random)).inflate(-40, -40)  # HITBOX AJUSTADA
                    ossos.append({"imagem": osso, "rect": rect_curto, "tipo": "curto"})
                else:
                    altura_ossoLongo = ossoLongo.get_height()
                    y_random = random.randint(205, tamanho[1] - altura_ossoLongo)
                    rect_longo = ossoLongo.get_rect(topleft=(1000, y_random)).inflate(-30, -30)  # HITBOX AJUSTADA
                    ossos.append({"imagem": ossoLongo, "rect": rect_longo, "tipo": "longo"})

        if not pausado:
            teclas = pygame.key.get_pressed()
            movendo = teclas[pygame.K_w] or teclas[pygame.K_UP] or teclas[pygame.K_s] or teclas[pygame.K_DOWN]

            if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                jogadorRect.y -= velocidade
            if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                jogadorRect.y += velocidade

            jogadorRect.y = max(205, min(tamanho[1] - jogadorRect.height, jogadorRect.y))

            ossos_remover = []
            for o in ossos:
                o["rect"].x -= velocidade_osso
                if jogadorRect.colliderect(o["rect"]):
                    if o["tipo"] == "azul":
                        if movendo:
                            vida -= 1
                            som_dano.play()
                            ossos_remover.append(o)
                    else:
                        vida -= 1
                        som_dano.play()
                        ossos_remover.append(o)
                elif o["rect"].right <= 0:
                    pontuacao += 1
                    velocidade_osso += 0.1
                    ossos_remover.append(o)
            for o in ossos_remover:
                ossos.remove(o)
            if vida <= 0:
                parar_musica()
                tela_game_over(nome, pontuacao)
                return

            # Só move o sansVoador se ele NÃO estiver falando
            if not sans_falando:
                sansVoador_rect.x += sans_velocidade_x
                if sansVoador_rect.left <= 0 or sansVoador_rect.right >= tamanho[0]:
                    sans_velocidade_x *= -1
            sansVoador_rect.bottom = 270

        tela.fill(preto)
        pygame.draw.rect(tela, branco, pygame.Rect(0, 200, tamanho[0], 5))
        tela.blit(sansVoador, sansVoador_rect)
        tela.blit(jogador, jogadorRect)
        for o in ossos:
            tela.blit(o["imagem"], o["rect"])

        # Lua pulsante
        tempo_passado = time.time() - tempo_inicial
        raio_pulsante = lua_base_raio + 5 * math.sin(tempo_passado * 2)
        pos_x = tamanho[0] - 50
        pos_y = 50
        pygame.draw.circle(tela, (255, 255, 0), (int(pos_x), int(pos_y)), int(raio_pulsante))

        tela.blit(fonte.render(f"VIDA: {vida}", True, branco), (10, 10))
        tela.blit(fonte.render(f"PONTOS: {pontuacao}", True, branco), (10, 40))
        tela.blit(fonte.render(f"VEL: {velocidade_osso:.1f}", True, branco), (10, 70))
        tela.blit(fonte.render("Press SPACE to Pause", True, cinza), (580, 10))

        # Mostra a fala do Sans na caixa ao lado direito dele
        if sans_falando and frase_atual:
            caixa_largura, caixa_altura = 400, 60
            caixa_x = sansVoador_rect.right + 10
            caixa_y = sansVoador_rect.top + 50
            pygame.draw.rect(tela, preto, (caixa_x, caixa_y, caixa_largura, caixa_altura))
            pygame.draw.rect(tela, branco, (caixa_x, caixa_y, caixa_largura, caixa_altura), 2)
            texto_fala = fonte.render(frase_atual, True, branco)
            tela.blit(texto_fala, (caixa_x + 10, caixa_y + 15))

        if pausado:
            texto_pause = fonte_grande.render("PAUSE", True, branco)
            tela.blit(texto_pause, ((tamanho[0] - texto_pause.get_width()) // 2,
                                    (tamanho[1] - texto_pause.get_height()) // 2))

        pygame.display.update()
        relogio.tick(60)


# Loop do programa
while True:
    escolha = menu_inicial()
    if escolha == "Jogar":
        jogo()
    elif escolha == "Ranking":
        tela_ranking()
    elif escolha == "Sair":
        pygame.quit()
        exit()
