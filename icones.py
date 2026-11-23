#Ícones dos power-ups desenhados com formas do pygame
import math
import pygame
def coracao(tela,cx,cy,s):
    """Vida extra (coxinha)"""
    vermelho = (220,40,60)
    raio = max(2, int(s* 0.52))
    pygame.draw.circle(tela, vermelho,(int(cx - s * 0.45), int (cy - s * 0.2)), raio)
    pygame.draw.circle(tela, vermelho,(int(cx + s * 0.45), int (cy - s * 0.2)), raio)
    pygame.draw.polygon(tela, vermelho, [(cx - s * 0.97, cy - s * 0.05), (cx + s * 0.97, cy - s * 0.05), (cx, cy + s * 0.95)])
    #brilho
    pygame.draw.circle(tela, (255,200,210), (int(cx - s * 0.5), int(cy - s * 0.35)), max(1, int(s*0.18)))
def guarda_chuva(tela, cx, cy, s):
    """Proteção contra chuva"""
    azul = (40, 90, 200)
    centro_cobertura = (int(cx), int(cy - s * 0.05))
    pygame.draw.circle(tela, azul, centro_cobertura, int(s * 0.95), draw_top_left = True, draw_top_right = True)
    #Gomos da cobertura
    for dx in (-0.32, 0.32):
        pygame.draw.line(tela, (120,170,255), centro_cobertura, (int(cx + s * dx * 2.6),int(cy - s * 0.05)),1)
        #Cabo e gancho do Guarda chuva
        pygame.draw.line(tela, (40,40,40), (cx,cy-s * 0.05), (cx,cy+s * 0.7),2)
        gancho = pygame.Rect(int(cx - s * 0.4), int(cy + s * 0.45), int(s*0.4), int(s * 0.5))
        pygame.draw.arc (tela, (40,40,40), gancho, math.pi, 2*math.pi, 2)
def ima(tela,cx,cy,s):
    """Imã que atrai os paes de queijo"""
    vermelho = (215,35,35)
    externo = s * 0.8
    interno = s * 0.38
    topo = cy - s*0.75
    pontos = [(cx - externo,topo)]
    #meia-volta de fora
    for i in range(13):
        a = math.pi * (i/12)
        pontos.append((cx-externo * math.cos(a), cy + externo * math.sin(a)))
        pontos.append((cx +externo, topo))
        pontos.append((cx + interno, topo))
    #meia-volta de dentro
    for i in range(13):
        a = math.pi * (i/12)
        pontos.append((cx + interno * math.cos(a), cy + interno * math.sin(a)))
        pontos.append((cx - interno, topo))
        pygame.draw.polygon(tela, vermelho, pontos)
        #pontas
        largura_braco = externo - interno
        prata = (220,220,230)
        pygame.draw.rect(tela, prata, (cx - externo, topo, largura_braco, s*0.4))
        pygame.draw.rect(tela, prata, (cx + interno, topo,largura_braco, s * 0.4))
def raio(tela,cx,cy,s):
    """Raio: Turbo"""
    formato = [(0.2, -1), (-0.6,0.12), (-0.05,0.12), (-0.25,1), (0.6, -0.18), (0.05, -0.18)]
    pontos = []
    for px, py in formato:
        pontos.append((cx + px * s, cy + py * s))
    pygame.draw.polygon(tela, (255,230,40), pontos)
    pygame.draw.polygon(tela, (150,70,0), pontos, 2)
#dicionario que liga o tipo de power-up à função que desenha o ícone
ICONES = {"guarda_chuva": guarda_chuva, 'ima': ima, "turbo": raio, "coxinha": coracao,}
def desenhar_icone(tela, tipo, cx,cy,s):
            funcao = ICONES[tipo]
            funcao(tela, cx, cy, s)
            

