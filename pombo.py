#Classe Pombo: personoagem do jogo

import pygame
from config import (ALTURA, CHAO_Y, POMBO_X, GRAVIDADE,EMPUXO, VELOCIDADE_MAX_SUBIDA, VELOCIDADE_MAX_QUEDA, VIDAS_INICIAIS, VIDAS_MAXIMAS, TEMPO_INVENCIVEL, DURACAO_IMA,DURACAO_TURBO,CORES)
from icones import guarda_chuva

#Posicao da ponta da asa em cada quadro
ASAS = [-20, -8, 6, -8]


class Pombo:
    def __init__(self):
        self.x = POMBO_X
        self.y = ALTURA/2
        self.vel_y = 0
        self.vidas = VIDAS_INICIAIS
        self.paes = 0
        #TEMPORIZADORES
        self.tempo_invencivel = 0
        self.tempo_ima = 0
        self.tempo_turbo = 0
        self.tem_guarda_chuva = False
        #animacao
        self.quadro =0
        self.tempo_quadro = 0
        self.rect = pygame.Rect(0,0,52,28)
        self.atualizar_rect()
    def atualizar_rect(self):
        """retangulo de colisao acompanha o pombo."""
        self.rect.x = int(self.x) - 22
        self.rect.y = int(self.y) - 16

    def reposicionar(self):
        """Chamado no começo de cada fase."""
        self.y = ALTURA/2
        self.vel_y = 0
        self.tempo_invencivel = 0
        self.tempo_ima = 0
        self.tempo_turbo = 0
        self.atualizar_rect()

    def animar(self, dt,  voando):
        """Troca o quadro da asa. Bate mais rapido quando esta subindo."""
        if voando:
            intervalo = 0.06
        else:
            intervalo = 0.14
        self.tempo_quadro += dt
        if self.tempo_quadro >= intervalo:
            self.tempo_quadro = 0
            self.quadro = (self.quadro + 1) % len(ASAS)
    def atualizar(self, dt, voando):
        #Física: segurar a tecla empurra para cima,gravidade para baixo
        if voando:
            self.vel_y += EMPUXO * dt
        self.vel_y += GRAVIDADE * dt
        #limita velocidade
        if self.vel_y < VELOCIDADE_MAX_SUBIDA:
            self.vel_y = VELOCIDADE_MAX_SUBIDA
        if self.vel_y > VELOCIDADE_MAX_QUEDA:
            self.vel_y = VELOCIDADE_MAX_QUEDA
        self.y += self.vel_y * dt
        #Nao deixa sair da tela por cima nem atravessar a rua
        if self.y < 20:
            self.y = 20
            self.vel_y = 0
        if self.y > CHAO_Y -16:
            self.y = CHAO_Y -16
            self.vel_y = 0
        #diminui os temporizadores
        self.tempo_invencivel = max(0,self.tempo_invencivel - dt)
        self.tempo_ima = max(0, self.tempo_ima -dt)
        self.tempo_turbo = max(0, self.tempo_turbo - dt)

        self.animar(dt, voando)
        self.atualizar_rect()

    def esta_invencivel(self):
        return self.tempo_invencivel > 0 or self.tempo_turbo > 0
    def levar_dano(self):
        """Retorna 'escudo' se o guarda-chuva protegeu ou 'vida' se perdeu uma vida"""
        if self.tem_guarda_chuva:
            self.tem_guarda_chuva = False
            self.tempo_invencivel = 1.0
            return "escudo"
        self.vidas -= 1
        self.tempo_invencivel = TEMPO_INVENCIVEL
        return "vida"
    def ativar_powerup(self, tipo):
        if tipo == "guarda_chuva":
            self.tem_guarda_chuva = True
        elif tipo == "ima":
            self.tempo_ima = DURACAO_IMA
        elif tipo == "turbo":
            self.tempo_turbo = DURACAO_TURBO
        elif tipo == "coxinha":
            if self.vidas < VIDAS_MAXIMAS:
                self.vidas += 1
    def desenhar(self,tela):
        #Pisca enquanto esta invencivel depois de bater
        if self.tempo_invencivel > 0 and int(self.tempo_invencivel*10)%2 == 0:
            return 
        cx = int(self.x)
        cy = int(self.y)

        #rastro de fogo
        if self.tempo_turbo > 0:
            for i in range(1, 5):
                pygame.draw.circle(tela,(255,160 - 25*i,0),(cx-20-i*12,cy+2), 11-i*2)
        #Anel do ima
        if self.tempo_ima>0:
            pygame.draw.circle(tela,(200,60,200),(cx,cy),34,2)
        #Rabo
        pygame.draw.polygon(tela, CORES["cinza_escuro"], [(cx-20,cy-4),(cx-36, cy-10),(cx - 36,cy+6)])
        #corpo
        pygame.draw.ellipse(tela, CORES["cinza_pombo"], (cx-24,cy-14,44,28))
        #pescoco verde
        pygame.draw.circle(tela, CORES["verde_pecoco"],(cx+13,cy-3),8)
        #cabeca
        pygame.draw.circle(tela, CORES["cinza_pombo"],(cx-20, cy-11),10)
        #olho
        pygame.draw.circle(tela, CORES["laranja"], (cx+24, cy-13),3)
        pygame.draw.circle(tela,CORES["preto"], (cx + 25,cy-13),1)
        #bico
        pygame.draw.polygon(tela,(230,170,60),[(cx+29,cy-12), (cx +37, cy-9),(cx+29,cy-7)])
        #Asa
        ponta = ASAS[self.quadro]
        pygame.draw.polygon(tela,CORES["cinza_escuro"], [(cx -14,cy-2),(cx+10, cy-2),(cx-10,cy+ponta)])
        #Guarda-chuva por cima do pombo
        if self.tem_guarda_chuva:
            guarda_chuva(tela,cx+4,cy-36,26)

        
        
        

