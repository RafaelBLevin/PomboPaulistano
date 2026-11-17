#Constantes do jogo: tamanho da tela, física do pombo, tempos e cores.
# Mudar um número aqu muda o jogo inteiro.

LARGURA = 900
ALTURA = 540
FPS = 60
TITULO = "Pombo Paulistano"

CHAO_Y = 500 #altura onde começa a rua

#Física do pombo
GRAVIDADE = 1500
EMPUXO = -3100 #Força para cima enquanto espaço é pressionado

VELOCIDADE_MAX_SUBIDA = -480 #Velocidade máxima do pombo
VELOCIDADE_MAX_QUEDA = 620 #Velocidade máxima do pombO

POMBO_X = 180 #pombo fica parado cenario que anda
VIDAS_INICIAIS = 3 #quantidade de vidas iniciais
VIDAS_MAXIMAS = 5 #quantidade máxima de vidas
TEMPO_INVENCIVEL = 2 #tempo de invencibilidade após perder uma vida
DURACAO_IMA= 7
DURACAO_TURBO = 3

PIXELS_POR_METRO = 10 #quantos pixels equivalem a 1 metro no jogo
MODO_TESTE = False #modo teste para pular fases e ganhar vidas infinitas

CORES = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "amarelo": (255,215,0),
    "vermelho": (220, 50, 50),
    "cinza_pombo": (125, 130, 145),
    "cinza_escuro": (80, 85, 100),
    "verde_pescoco": (70,160,120),
    "laranja": (255, 140, 0),
    "asfalto": (60, 60, 65),
    "calcada": (170, 165, 155),}
