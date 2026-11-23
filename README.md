# PomboPaulistano
Integrantes
Rafael Baldassarri Levin
Pedro Buelta
Vídeo
Link do vídeo: (https://youtu.be/wLfsu3B74Ck)

Como instalar e rodar
Instale o Python 3 (versão 3.9 ou mais nova).
Instale o PyGame (versão pygame-ce): pip install pygame-ce
Dentro da pasta do projeto, rode: python main.py
Controles
Tecla	Ação
ESPAÇO, seta para cima, W ou clique do mouse (segurar)	Voar
Soltar a tecla	Descer
P ou ESC	Pausar
M (no pause)	Voltar ao menu
ENTER	Confirmar / próxima fase
Como jogar
Segure para subir e solte para descer. Desvie dos obstáculos.
Cada pão de queijo vale 10 pontos (vezes o multiplicador).
A cada 8 segundos sem bater, o multiplicador sobe (até x5).
São 4 fases: Avenida Paulista, Marginal com Chuva, Centro à Noite e Fuga do Gavião.
No fim de cada fase você ganha 100 pontos por vida restante.
A fase 4 é a mais difícil: gaviões atacam em sequência, com menos aviso e mais rápido, e aparecem menos power-ups.
Só entra no ranking quem completa todas as fases.
Power-ups
Ícone	Power-up	Efeito
Guarda-chuva azul	Guarda-chuva	Aguenta uma batida
Ímã vermelho	Ímã	Puxa os pães de queijo por 7 segundos
Raio amarelo	Turbo	Invencível e destrói obstáculos por 3 segundos
Coração	Coxinha	+1 vida (máximo 5)
Organização do código
Arquivo	O que faz
main.py	Inicia o jogo
jogo.py	Classe Jogo: laço principal, telas, colisões e pontuação
pombo.py	Classe Pombo: física, vidas, power-ups e animação
obstaculos.py	Classe Obstaculo e as filhas Predio, Placa, Fio, Drone e Gaviao
icones.py	Ícones dos power-ups desenhados com formas do pygame
itens.py	Classe Item e as filhas PaoDeQueijo e PowerUp
cenario.py	Fundo com parallax, chuva e partículas
fases.py	Dados das fases e dos padrões de obstáculos
sons.py	Efeitos sonoros gerados por código
recordes.py	Ranking salvo no arquivo recordes.txt
config.py	Constantes (tamanho da tela, física, cores)
Relação entre os objetos
Composição: o Jogo tem um Pombo, um Cenario, uma lista de obstáculos, uma lista de itens e um objeto Sons.
Herança: Predio, Placa, Fio, Drone e Gaviao herdam de Obstaculo. PaoDeQueijo e PowerUp herdam de Item.
Associação: o Gaviao guarda uma referência ao Pombo para mirar nele.
Recursos que não foram vistos em aula
Herança de classes e super()
Fundo com parallax
Delta time (movimento independente do FPS)
Sons gerados matematicamente com o módulo array
Partículas e tremor de tela
Ranking salvo em arquivo
Uso de IA generativa:
Ajuda na criação dos sprites(coração,guarda-chuva,raio,imã e pombo) e ajuda a entender funções do pygame como (pygame.draw, pygame.Rect)

