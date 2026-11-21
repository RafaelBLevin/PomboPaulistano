# obstaculos.py

import math
import random
import pygame
from config import LARGURA, CHAO_Y, CORES


class Obstaculo:
    def __init__(self, x, y, largura, altura):
        self.x = float(x)             # posição com casas decimais (movimento suave)
        self.rect = pygame.Rect(int(x), int(y), largura, altura)
        self.ativo = True             # quando vira False, o jogo remove da lista

    def atualizar(self, dt, velocidade):
        self.x -= velocidade * dt
        self.rect.x = int(self.x)
        if self.rect.right < 0:
            self.ativo = False

    def desenhar(self, tela):
        pygame.draw.rect(tela, CORES["vermelho"], self.rect)


class Predio(Obstaculo):
    def __init__(self, x, altura, noite):
        super().__init__(x, CHAO_Y - altura, 90, altura)
        self.noite = noite

    def desenhar(self, tela):
        if self.noite:
            cor_predio = (45, 45, 70)
            cor_janela = (255, 220, 120)
        else:
            cor_predio = (120, 100, 95)
            cor_janela = (180, 215, 235)

        pygame.draw.rect(tela, cor_predio, self.rect)
        pygame.draw.rect(tela, CORES["preto"], self.rect, 2)

        # Janelas: grade feita com dois "for"
        for y in range(self.rect.top + 12, self.rect.bottom - 20, 28):
            for x in range(self.rect.left + 12, self.rect.right - 14, 26):
                pygame.draw.rect(tela, cor_janela, (x, y, 14, 16))

        # Antena no topo
        topo_x = self.rect.centerx
        pygame.draw.line(tela, CORES["preto"], (topo_x, self.rect.top), (topo_x, self.rect.top - 14), 2)


class Placa(Obstaculo):
    """Placa pendurada em um viaduto (vem de cima)."""

    def __init__(self, x, comprimento):
        super().__init__(x, 0, 70, comprimento)

    def desenhar(self, tela):
        # Pilar de concreto
        pilar = pygame.Rect(self.rect.x + 25, 0, 20, self.rect.height - 50)
        pygame.draw.rect(tela, (150, 150, 150), pilar)
        # Placa verde de trânsito
        placa = pygame.Rect(self.rect.x, self.rect.bottom - 55, self.rect.width, 55)
        pygame.draw.rect(tela, (30, 120, 60), placa)
        pygame.draw.rect(tela, CORES["branco"], placa, 3)
        pygame.draw.line(tela, CORES["branco"], (placa.x + 12, placa.centery),
                         (placa.right - 12, placa.centery), 3)
        pygame.draw.polygon(tela, CORES["branco"],
                            [(placa.right - 12, placa.centery - 8),
                             (placa.right - 2, placa.centery),
                             (placa.right - 12, placa.centery + 8)])


class Fio(Obstaculo):
    """Fio elétrico solto no ar soltando faíscas."""

    def __init__(self, x, y):
        super().__init__(x, y - 4, 240, 20)

    def desenhar(self, tela):
        pontos = []
        for i in range(13):
            t = i / 12
            px = self.rect.left + t * self.rect.width
            py = self.rect.top + 4 + math.sin(math.pi * t) * 12   # fio "barrigudo"
            pontos.append((px, py))
        pygame.draw.lines(tela, CORES["preto"], False, pontos, 4)
        pygame.draw.circle(tela, (90, 90, 90), (self.rect.left, self.rect.top + 4), 6)
        pygame.draw.circle(tela, (90, 90, 90), (self.rect.right, self.rect.top + 4), 6)

        # Faíscas aleatórias
        if random.random() < 0.3:
            fx, fy = random.choice(pontos)
            for _ in range(3):
                pygame.draw.line(tela, CORES["amarelo"], (fx, fy),
                                 (fx + random.randint(-10, 10), fy + random.randint(-10, 10)), 2)


class Drone(Obstaculo):
    """Drone de entrega que sobe e desce."""

    def __init__(self, x, y_centro):
        super().__init__(x, y_centro, 56, 22)
        self.y_centro = y_centro
        self.tempo = random.uniform(0, 3)

    def atualizar(self, dt, velocidade):
        super().atualizar(dt, velocidade)          # reaproveita o movimento da classe mãe
        self.tempo += dt
        self.rect.centery = int(self.y_centro + math.sin(self.tempo * 3) * 50)

    def desenhar(self, tela):
        r = self.rect
        pygame.draw.rect(tela, (50, 50, 60), (r.x + 10, r.y + 8, r.width - 20, r.height - 8),
                         border_radius=4)
        # Hélices piscando (animação simples)
        tamanho = 14 if int(self.tempo * 20) % 2 == 0 else 6
        for hx in (r.x + 8, r.right - 8):
            pygame.draw.line(tela, (30, 30, 30), (hx, r.y + 8), (hx, r.y + 2), 2)
            pygame.draw.line(tela, (200, 200, 200), (hx - tamanho, r.y + 2), (hx + tamanho, r.y + 2), 2)
        # Luz vermelha
        if int(self.tempo * 3) % 2 == 0:
            pygame.draw.circle(tela, CORES["vermelho"], (r.centerx, r.bottom - 6), 3)


class Gaviao(Obstaculo):
    """Gavião que mira na altura do pombo e dá um rasante.
    Ele GUARDA uma referência ao pombo (self.alvo): é uma relação entre objetos."""

    def __init__(self, x, alvo, aviso=1.2, rasante=380):
        super().__init__(LARGURA + 20, alvo.y, 64, 30)
        self.alvo = alvo
        self.y = float(alvo.y)
        self.aviso = aviso         # segundos de aviso antes do ataque
        self.rasante = rasante     # velocidade extra no ataque

    def atualizar(self, dt, velocidade):
        if self.aviso > 0:
            # Fica fora da tela seguindo a altura do pombo
            self.aviso -= dt
            self.y += (self.alvo.y - self.y) * 3 * dt
        else:
            # Ataca: voa mais rápido que o cenário
            self.x -= (velocidade + self.rasante) * dt
        self.rect.x = int(self.x)
        self.rect.centery = int(self.y)
        if self.rect.right < 0:
            self.ativo = False

    def desenhar(self, tela):
        if self.aviso > 0:
            # Sinal de perigo piscando na borda direita
            if int(self.aviso * 8) % 2 == 0:
                y = int(self.y)
                x = LARGURA - 30
                pygame.draw.polygon(tela, CORES["vermelho"], [(x, y - 18), (x - 16, y + 12), (x + 16, y + 12)])
                pygame.draw.rect(tela, CORES["branco"], (x - 2, y - 8, 4, 11))
                pygame.draw.circle(tela, CORES["branco"], (x, y + 7), 2)
            return

        r = self.rect
        marrom = (110, 70, 40)
        pygame.draw.ellipse(tela, marrom, (r.x + 10, r.y + 8, 48, 18))
        pygame.draw.polygon(tela, (80, 50, 30), [(r.x + 25, r.y + 12), (r.x + 50, r.y - 6), (r.x + 42, r.y + 14)])
        pygame.draw.circle(tela, (230, 220, 200), (r.x + 12, r.y + 13), 8)       # cabeça
        pygame.draw.polygon(tela, CORES["amarelo"], [(r.x + 5, r.y + 11), (r.x - 4, r.y + 16), (r.x + 6, r.y + 17)])
        pygame.draw.circle(tela, CORES["preto"], (r.x + 10, r.y + 11), 2)
        pygame.draw.polygon(tela, marrom, [(r.right - 8, r.y + 15), (r.right + 6, r.y + 8), (r.right + 6, r.y + 22)])