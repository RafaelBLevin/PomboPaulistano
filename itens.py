# Itens coletáveis: classe base Item e as filhas PaoDeQueijo e PowerUp.

import math
import random
import pygame
from config import CORES
from icones import desenhar_icone
# Dicionário com as informações de cada power-up
TIPOS_POWERUP = {
    "guarda_chuva": {"nome": "Guarda-chuva", "cor": (170, 210, 255),"descricao": "Guarda-chuva: aguenta uma batida"},
    "ima": {"nome": "Ímã", "cor": (235, 205, 245),"descricao": "Ímã: puxa os pães de queijo"},
    "turbo": {"nome": "Turbo", "cor": (255, 150, 40),"descricao": "Turbo: fica invencível e destrói obstáculos"},
    "coxinha": {"nome": "Coxinha", "cor": (255, 200, 210), "descricao": "Coxinha: ganha uma vida"},
}
class Item:
    def __init__(self, x, y, raio, cor):
        self.x = float(x)
        self.y = float(y)
        self.raio = raio
        self.cor = cor
        self.ativo = True
        self.som = "pao"
        self.rect = pygame.Rect(0, 0, raio * 2, raio * 2)
        self.atualizar_rect()

    def atualizar_rect(self):
        self.rect.center = (int(self.x), int(self.y))

    def atualizar(self, dt, velocidade, pombo):
        self.x -= velocidade * dt
        if self.x < -50:
            self.ativo = False
        self.atualizar_rect()

    def aplicar(self, pombo):
        """Efeito ao ser coletado. Retorna quantos pontos vale."""
        return 0

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, self.rect.center, self.raio)


class PaoDeQueijo(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 11, (240, 190, 90))
        self.tempo = random.uniform(0, 6)

    def atualizar(self, dt, velocidade, pombo):
        super().atualizar(dt, velocidade, pombo)
        self.tempo += dt
        # Com o ímã ativo, o pão é puxado na direção do pombo
        if pombo.tempo_ima > 0:
            dx = pombo.x - self.x
            dy = pombo.y - self.y
            distancia = math.hypot(dx, dy)
            if 1 < distancia < 260:
                self.x += dx / distancia * 700 * dt
                self.y += dy / distancia * 700 * dt
                self.atualizar_rect()

    def aplicar(self, pombo):
        pombo.paes += 1
        return 10

    def desenhar(self, tela):
        flutua = int(math.sin(self.tempo * 4) * 3)     # balança para cima e para baixo
        cx = self.rect.centerx
        cy = self.rect.centery + flutua
        pygame.draw.circle(tela, (190, 140, 50), (cx, cy), self.raio)
        pygame.draw.circle(tela, self.cor, (cx - 1, cy - 1), self.raio - 2)
        pygame.draw.circle(tela, (255, 230, 160), (cx - 4, cy - 4), 3)


class PowerUp(Item):
    def __init__(self, x, y, tipo):
        super().__init__(x, y, 18, TIPOS_POWERUP[tipo]["cor"])
        self.tipo = tipo
        self.som = "powerup"
        self.tempo = 0

    def atualizar(self, dt, velocidade, pombo):
        super().atualizar(dt, velocidade, pombo)
        self.tempo += dt

    def aplicar(self, pombo):
        pombo.ativar_powerup(self.tipo)
        return 50

    def desenhar(self, tela):
        # Bolha branca que "pulsa" + bolha colorida + ícone no meio
        brilho = self.raio + 3 + int(math.sin(self.tempo * 6) * 3)
        cx, cy = self.rect.center
        pygame.draw.circle(tela, CORES["branco"], (cx, cy), brilho)
        pygame.draw.circle(tela, self.cor, (cx, cy), self.raio)
        desenhar_icone(tela, self.tipo, cx, cy, 12)