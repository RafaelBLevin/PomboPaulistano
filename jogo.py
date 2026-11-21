# Classe Jogo: junta todos os objetos e controla as telas (estados).
# Relação entre os objetos (composição):
#   Jogo TEM um Pombo, um Cenario, uma lista de Obstaculos, uma lista de Itens,
#   uma lista de Particulas e um objeto Sons.
#   O Gaviao guarda uma referência ao Pombo para poder persegui-lo.
# Estados (telas) possíveis em self.estado:
#   "menu", "instrucoes", "recordes", "jogando", "pausado",
#   "fase_concluida", "game_over", "vitoria", "nome"

import math
import random
import pygame

from config import (LARGURA, ALTURA, FPS, TITULO, CHAO_Y, CORES, PIXELS_POR_METRO,MODO_TESTE, DURACAO_IMA, DURACAO_TURBO)
from fases import FASES, PADROES
from pombo import Pombo
from obstaculos import Predio, Placa, Fio, Drone, Gaviao
from itens import PaoDeQueijo, PowerUp, TIPOS_POWERUP
from icones import desenhar_icone, coracao
from cenario import Cenario, Particula
from sons import Sons
from recordes import carregar_recordes, eh_recorde, salvar_recorde

OPCOES_MENU = ["Jogar", "Como jogar", "Recordes", "Sair"]

INSTRUCOES = [
    "Segure ESPAÇO (ou o botão do mouse) para voar.",
    "Solte para o pombo descer.",
    "Desvie de prédios, placas, fios, drones e do gavião!",
    "Pegue pães de queijo para ganhar pontos.",
    "Fique sem bater para subir o multiplicador (até x5).",
    "Complete as 4 fases para entrar no ranking!",
]
# Os power-ups aparecem na tela "Como jogar" com o ícone de cada um
def remover_inativos(lista):
    """Devolve uma nova lista só com os objetos que ainda estão ativos."""
    nova = []
    for objeto in lista:
        if objeto.ativo:
            nova.append(objeto)
    return nova


class Jogo:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.relogio = pygame.time.Clock()
        self.mundo = pygame.Surface((LARGURA, ALTURA))   # onde o jogo é desenhado (para tremer a tela)

        self.fonte_titulo = pygame.font.Font(None, 84)
        self.fonte_grande = pygame.font.Font(None, 56)
        self.fonte_media = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 26)

        self.sons = Sons()
        self.sons.tocar_musica()
        self.recordes = carregar_recordes()

        self.rodando = True
        self.opcao_menu = 0
        self.tempo_total = 0
        self.nome_digitado = ""

        # Cenário e pombo que aparecem animados atrás do menu
        self.cenario_menu = Cenario(FASES[0])
        self.pombo_menu = Pombo()

        self.novo_jogo()
        self.estado = "menu"
    # Preparação de partida e de fase
    def novo_jogo(self):
        self.pombo = Pombo()
        self.pontos = 0
        self.indice_fase = 0
        self.iniciar_fase()
    def iniciar_fase(self):
        self.fase = FASES[self.indice_fase]
        self.meta_pixels = self.fase["meta"] * PIXELS_POR_METRO
        self.cenario = Cenario(self.fase)
        self.obstaculos = []
        self.itens = []
        self.particulas = []
        self.distancia = 0
        self.proximo_padrao = 700          # um respiro antes do primeiro obstáculo
        self.velocidade = self.fase["velocidade"]
        self.tempo_sem_bater = 0
        self.multiplicador = 1
        self.tremor = 0
        self.tempo_banner = 2.5
        self.bonus_fase = 0
        self.pombo.reposicionar()
    # Laço principal   
    def executar(self):
        while self.rodando:
            dt = self.relogio.tick(FPS) / 1000     # segundos desde o último quadro
            dt = min(dt, 0.05)                      # evita "pulos" se o PC travar
            self.tempo_total += dt
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()
            pygame.display.flip()
        pygame.quit()