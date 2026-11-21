# sons.py

import array
import math
import os
import pygame

PASTA = os.path.dirname(os.path.abspath(__file__))


def criar_som(freq_inicial, freq_final, duracao, volume=0.3, onda="seno"):
    """Cria um som que vai de freq_inicial até freq_final (em Hz)."""
    taxa, formato, canais = pygame.mixer.get_init()
    if abs(formato) != 16:
        return None
    total = int(taxa * duracao)
    amostras = array.array("h")         # lista de números inteiros de 16 bits
    fase = 0.0
    for i in range(total):
        t = i / total
        freq = freq_inicial + (freq_final - freq_inicial) * t
        fase += 2 * math.pi * freq / taxa
        valor = math.sin(fase)
        if onda == "quadrada":
            if valor >= 0:
                valor = 1
            else:
                valor = -1
        amostra = int(32767 * volume * valor * (1 - t))   # (1 - t) faz o som sumir aos poucos
        for _ in range(canais):
            amostras.append(amostra)
    return pygame.mixer.Sound(buffer=amostras.tobytes())


class Sons:
    def __init__(self):
        self.efeitos = {}
        if pygame.mixer.get_init() is None:
            return
        try:
            self.efeitos["pao"] = criar_som(900, 1400, 0.08, 0.25)
            self.efeitos["powerup"] = criar_som(400, 1600, 0.35, 0.25)
            self.efeitos["batida"] = criar_som(300, 60, 0.35, 0.18, "quadrada")
            self.efeitos["escudo"] = criar_som(700, 300, 0.25, 0.25)
            self.efeitos["explosao"] = criar_som(200, 40, 0.3, 0.2, "quadrada")
            self.efeitos["fase"] = criar_som(500, 1200, 0.6, 0.25)
            self.efeitos["game_over"] = criar_som(450, 90, 0.9, 0.2, "quadrada")
            self.efeitos["menu"] = criar_som(600, 700, 0.05, 0.2)
        except pygame.error:
            self.efeitos = {}

    def tocar(self, nome):
        if nome in self.efeitos and self.efeitos[nome] is not None:
            self.efeitos[nome].play()

    def tocar_musica(self):
        caminho = os.path.join(PASTA, "assets", "musica.ogg")
        if pygame.mixer.get_init() and os.path.exists(caminho):
            try:
                pygame.mixer.music.load(caminho)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)      # -1 = repetir para sempre
            except pygame.error:
                pass