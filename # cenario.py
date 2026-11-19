# cenario.py

import math
import random
import pygame
from config import LARGURA, ALTURA, CHAO_Y, CORES


def criar_degrade(cor_topo, cor_base):
    """Desenha o céu uma vez só, em uma superfície, para não gastar tempo a cada quadro."""
    superficie = pygame.Surface((LARGURA, CHAO_Y))
    for y in range(CHAO_Y):
        t = y / CHAO_Y
        cor = (int(cor_topo[0] + (cor_base[0] - cor_topo[0]) * t),
               int(cor_topo[1] + (cor_base[1] - cor_topo[1]) * t),
               int(cor_topo[2] + (cor_base[2] - cor_topo[2]) * t))
        pygame.draw.line(superficie, cor, (0, y), (LARGURA, y))
    return superficie


class Camada:
    """Uma fileira de prédios do fundo. Cada prédio é um dicionário."""

    def __init__(self, cor, fator, altura_min, altura_max, com_janelas):
        self.cor = cor
        self.fator = fator            # 0.2 = anda a 20% da velocidade do jogo
        self.altura_min = altura_min
        self.altura_max = altura_max
        self.com_janelas = com_janelas
        self.predios = []
        x = 0
        while x < LARGURA + 200:
            predio = self.novo_predio(x)
            self.predios.append(predio)
            x += predio["largura"] + random.randint(0, 20)

    def novo_predio(self, x):
        largura = random.randint(60, 140)
        altura = random.randint(self.altura_min, self.altura_max)
        janelas = []
        if self.com_janelas:
            for dy in range(12, altura - 10, 22):
                for dx in range(8, largura - 10, 18):
                    if random.random() < 0.35:
                        janelas.append((dx, dy))
        return {"x": x, "largura": largura, "altura": altura, "janelas": janelas}

    def atualizar(self, dt, velocidade):
        for predio in self.predios:
            predio["x"] -= velocidade * self.fator * dt

        # Prédio que saiu pela esquerda é trocado por um novo no final da fila
        primeiro = self.predios[0]
        if primeiro["x"] + primeiro["largura"] < 0:
            self.predios.pop(0)
            ultimo = self.predios[-1]
            novo_x = ultimo["x"] + ultimo["largura"] + random.randint(0, 20)
            self.predios.append(self.novo_predio(novo_x))

    def desenhar(self, tela):
        for predio in self.predios:
            x = int(predio["x"])
            y = CHAO_Y - predio["altura"]
            pygame.draw.rect(tela, self.cor, (x, y, predio["largura"], predio["altura"]))
            for dx, dy in predio["janelas"]:
                pygame.draw.rect(tela, (250, 210, 110), (x + dx, y + dy, 7, 9))


class Cenario:
    def __init__(self, fase):
        self.ceu = criar_degrade(fase["ceu_topo"], fase["ceu_base"])
        self.noite = fase["noite"]
        self.chuva = fase["chuva"]
        self.camadas = [
            Camada(fase["predios_longe"], 0.15, 140, 300, False),
            Camada(fase["predios_perto"], 0.40, 80, 200, fase["noite"]),
        ]
        self.deslocamento_rua = 0

        self.nuvens = []
        for _ in range(5):
            self.nuvens.append([random.randint(0, LARGURA), random.randint(30, 160), random.randint(30, 60)])

        self.estrelas = []
        if self.noite:
            for _ in range(60):
                self.estrelas.append((random.randint(0, LARGURA), random.randint(0, 300)))

        self.gotas = []
        if self.chuva:
            for _ in range(140):
                self.gotas.append([random.randint(0, LARGURA), random.randint(0, CHAO_Y)])

    def atualizar(self, dt, velocidade):
        for camada in self.camadas:
            camada.atualizar(dt, velocidade)

        self.deslocamento_rua = (self.deslocamento_rua + velocidade * dt) % 80

        for nuvem in self.nuvens:
            nuvem[0] -= velocidade * 0.05 * dt
            if nuvem[0] < -120:
                nuvem[0] = LARGURA + 60
                nuvem[1] = random.randint(30, 160)

        for gota in self.gotas:
            gota[0] -= (200 + velocidade * 0.5) * dt
            gota[1] += 750 * dt
            if gota[1] > CHAO_Y or gota[0] < 0:
                gota[0] = random.randint(0, LARGURA + 200)
                gota[1] = random.randint(-50, 0)

    def desenhar(self, tela):
        tela.blit(self.ceu, (0, 0))

        if self.noite:
            for estrela in self.estrelas:
                pygame.draw.circle(tela, CORES["branco"], estrela, 1)
            pygame.draw.circle(tela, (240, 240, 210), (800, 90), 34)    # lua
        elif not self.chuva:
            pygame.draw.circle(tela, (255, 230, 120), (820, 90), 40)    # sol

        if not self.noite:
            cor_nuvem = (200, 200, 205) if self.chuva else CORES["branco"]
            for x, y, tamanho in self.nuvens:
                pygame.draw.ellipse(tela, cor_nuvem, (x, y, tamanho * 2.4, tamanho))
                pygame.draw.ellipse(tela, cor_nuvem, (x + tamanho * 0.6, y - tamanho * 0.4, tamanho * 1.3, tamanho))

        for camada in self.camadas:
            camada.desenhar(tela)

        # Rua com faixas que andam
        pygame.draw.rect(tela, CORES["asfalto"], (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
        pygame.draw.rect(tela, CORES["calcada"], (0, CHAO_Y, LARGURA, 8))
        for x in range(-int(self.deslocamento_rua), LARGURA, 80):
            pygame.draw.rect(tela, CORES["amarelo"], (x, CHAO_Y + 22, 40, 4))

        for gx, gy in self.gotas:
            pygame.draw.line(tela, (170, 190, 220), (gx, gy), (gx - 4, gy + 12), 1)


class Particula:
    """Pedaçinho que voa e some (usado ao pegar itens, bater e explodir obstáculos)."""

    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(80, 260)
        self.vx = math.cos(angulo) * velocidade
        self.vy = math.sin(angulo) * velocidade
        self.vida_maxima = random.uniform(0.3, 0.7)
        self.vida = self.vida_maxima
        self.cor = cor
        self.ativo = True

    def atualizar(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 400 * dt
        self.vida -= dt
        if self.vida <= 0:
            self.ativo = False

    def desenhar(self, tela):
        raio = max(1, int(5 * self.vida / self.vida_maxima))
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), raio)