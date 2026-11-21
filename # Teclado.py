# Teclado
  
def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                self.tecla_apertada(evento)

def tecla_apertada(self, evento):
        tecla = evento.key

        if self.estado == "menu":
            self.teclas_menu(tecla)

        elif self.estado in ("instrucoes", "recordes"):
            if tecla in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.estado = "menu"

        elif self.estado == "jogando":
            if tecla in (pygame.K_p, pygame.K_ESCAPE):
                self.estado = "pausado"
            elif MODO_TESTE and tecla == pygame.K_n:
                self.distancia = self.meta_pixels

        elif self.estado == "pausado":
            if tecla in (pygame.K_p, pygame.K_ESCAPE):
                self.estado = "jogando"
            elif tecla == pygame.K_m:
                self.estado = "menu"

        elif self.estado == "fase_concluida":
            if tecla == pygame.K_RETURN:
                self.indice_fase += 1
                self.iniciar_fase()
                self.estado = "jogando"

        elif self.estado in ("game_over", "vitoria"):
            if tecla == pygame.K_RETURN:
                self.terminar_partida()

        elif self.estado == "nome":
            self.digitar_nome(evento)

def teclas_menu(self, tecla):
        if tecla == pygame.K_UP:
            self.opcao_menu = (self.opcao_menu - 1) % len(OPCOES_MENU)
            self.sons.tocar("menu")
        elif tecla == pygame.K_DOWN:
            self.opcao_menu = (self.opcao_menu + 1) % len(OPCOES_MENU)
            self.sons.tocar("menu")
        elif tecla == pygame.K_ESCAPE:
            self.rodando = False
        elif tecla == pygame.K_RETURN:
            escolha = OPCOES_MENU[self.opcao_menu]
            if escolha == "Jogar":
                self.novo_jogo()
                self.estado = "jogando"
            elif escolha == "Como jogar":
                self.estado = "instrucoes"
            elif escolha == "Recordes":
                self.recordes = carregar_recordes()
                self.estado = "recordes"
            elif escolha == "Sair":
                self.rodando = False

def digitar_nome(self, evento):
        if evento.key == pygame.K_RETURN:
            salvar_recorde(self.nome_digitado, int(self.pontos))
            self.recordes = carregar_recordes()
            self.estado = "recordes"
        elif evento.key == pygame.K_BACKSPACE:
            self.nome_digitado = self.nome_digitado[:-1]       # fatiamento: tira a última letra
        else:
            letra = evento.unicode
            if letra != "" and (letra.isalnum() or letra == " ") and len(self.nome_digitado) < 12:
                self.nome_digitado += letra

def terminar_partida(self):
        # Só entra no ranking quem completou as 4 fases (estado "vitoria")
        if self.estado == "vitoria" and eh_recorde(int(self.pontos)):
            self.nome_digitado = ""
            self.estado = "nome"
        else:
            self.estado = "menu"

def jogador_quer_voar(self):
        teclas = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        return teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w] or mouse[0]