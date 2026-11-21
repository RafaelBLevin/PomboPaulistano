# fases.py
# Dados das fases e dos "padrões" de obstáculos.
# Tudo aqui é só DADO (listas e dicionários): para criar uma fase nova
# basta adicionar um dicionário na lista FASES, sem mexer no resto do código.

import math
from config import CHAO_Y


def linha_de_paes(dx_inicial, y, quantidade):
    """Cria uma fileira reta de pães de queijo."""
    pecas = []
    for i in range(quantidade):
        pecas.append(("pao", dx_inicial + i * 45, y))
    return pecas


def onda_de_paes(dx_inicial, y_centro, quantidade):
    """Cria pães de queijo em formato de onda (usa seno)."""
    pecas = []
    for i in range(quantidade):
        y = y_centro + int(math.sin(i * 0.8) * 70)
        pecas.append(("pao", dx_inicial + i * 45, y))
    return pecas


# Cada padrão é uma lista de peças no formato (tipo, distância_x, valor).
#   predio -> valor = altura do prédio
#   placa  -> valor = comprimento da placa pendurada no viaduto
#   fio    -> valor = altura (y) do fio
#   drone  -> valor = altura (y) central do drone
#   gaviao -> valor = segundos EXTRAS de espera antes do ataque
#             (serve para fazer um gavião atacar logo depois do outro)
#   pao    -> valor = altura (y) do pão de queijo
PADROES = {
    "predio_baixo": [("predio", 0, 150)] + linha_de_paes(10, CHAO_Y - 150 - 50, 2),
    "predio_alto": [("predio", 0, 260)],
    "placa": [("placa", 0, 180)] + linha_de_paes(0, 270, 2),
    "fio": [("fio", 0, 230)] + linha_de_paes(20, 150, 5),
    "corredor": [("predio", 0, 150), ("placa", 0, 170)] + linha_de_paes(15, 260, 2),
    "escada": [("predio", 0, 110), ("predio", 230, 200), ("predio", 460, 290)],
    "drone": [("drone", 0, 220)],
    "drone_duplo": [("drone", 0, 160), ("drone", 220, 360)],
    "paes_reta": linha_de_paes(0, 250, 8),
    "paes_onda": onda_de_paes(0, 260, 10),
    "gaviao": [("gaviao", 0, 0)],
    "gaviao_predio": [("predio", 0, 200), ("gaviao", 0, 0)],
    # Padrões difíceis (fase 4)
    "gaviao_duplo": [("gaviao", 0, 0), ("gaviao", 0, 0.8)],
    "gaviao_triplo": [("gaviao", 0, 0), ("gaviao", 0, 0.6), ("gaviao", 0, 1.2)],
    "gaviao_corredor": [("predio", 0, 140), ("placa", 0, 160), ("gaviao", 0, 0.4)],
    "gaviao_drones": [("drone", 0, 170), ("drone", 260, 370), ("gaviao", 0, 0.5)],
    "gaviao_escada": [("predio", 0, 120), ("predio", 230, 210), ("gaviao", 0, 0.6)],
}

# Cada fase é um dicionário:
#   meta            -> metros até a entrega
#   velocidade      -> pixels por segundo no início da fase
#   chance_powerup  -> chance (0 a 1) de aparecer um power-up depois de cada padrão
#   espaco_min/max  -> distância (pixels) entre um padrão e outro (menor = mais difícil)
#   aviso_gaviao    -> segundos que o sinal de perigo aparece antes do gavião atacar
#   rasante_gaviao  -> velocidade extra do gavião no ataque
FASES = [
    {
        "nome": "Avenida Paulista",
        "meta": 1600,
        "velocidade": 300,
        "ceu_topo": (110, 170, 230),
        "ceu_base": (190, 225, 245),
        "predios_longe": (150, 165, 190),
        "predios_perto": (100, 110, 135),
        "chuva": False,
        "noite": False,
        "chance_powerup": 0.2,
        "espaco_min": 300,
        "espaco_max": 460,
        "aviso_gaviao": 1.2,
        "rasante_gaviao": 380,
        "padroes": ["predio_baixo", "predio_alto", "placa", "fio", "paes_reta", "paes_onda"],
    },
    {
        "nome": "Marginal com Chuva",
        "meta": 2200,
        "velocidade": 350,
        "ceu_topo": (80, 90, 105),
        "ceu_base": (140, 150, 160),
        "predios_longe": (105, 112, 125),
        "predios_perto": (70, 76, 90),
        "chuva": True,
        "noite": False,
        "chance_powerup": 0.2,
        "espaco_min": 290,
        "espaco_max": 440,
        "aviso_gaviao": 1.2,
        "rasante_gaviao": 380,
        "padroes": ["predio_baixo", "predio_alto", "placa", "fio", "corredor",
                    "drone", "paes_onda"],
    },
    {
        "nome": "Centro à Noite",
        "meta": 2700,
        "velocidade": 390,
        "ceu_topo": (10, 15, 40),
        "ceu_base": (45, 40, 90),
        "predios_longe": (35, 35, 65),
        "predios_perto": (25, 25, 45),
        "chuva": False,
        "noite": True,
        "chance_powerup": 0.18,
        "espaco_min": 280,
        "espaco_max": 420,
        "aviso_gaviao": 1.2,
        "rasante_gaviao": 380,
        "padroes": ["predio_alto", "corredor", "escada", "drone", "drone_duplo",
                    "fio", "paes_reta", "gaviao"],
    },
    {
        "nome": "Fuga do Gavião",
        "meta": 3200,
        "velocidade": 450,
        "ceu_topo": (240, 120, 80),
        "ceu_base": (255, 200, 140),
        "predios_longe": (170, 110, 110),
        "predios_perto": (110, 70, 80),
        "chuva": False,
        "noite": False,
        "chance_powerup": 0.1,      # menos ajuda
        "espaco_min": 220,          # obstáculos mais colados
        "espaco_max": 340,
        "aviso_gaviao": 0.85,       # menos tempo para reagir
        "rasante_gaviao": 500,      # ataque mais rápido
        "padroes": ["gaviao_duplo", "gaviao_triplo", "gaviao_corredor", "gaviao_drones",
                    "gaviao_escada", "gaviao_predio", "corredor", "drone_duplo", "escada"],
    },
]