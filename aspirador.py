class Aspirador:
    def __init__(self):
        self.posicao_atual = [0, 0]
        self.estrutura_para_limpar = None
        self.energia = 100
        self.bolsa = Bolsa()

    def mover(self, direcao):
        self.energia -= 1

        x, y = self.posicao_atual

        if direcao == "cima":
            if y == 0:
                print("Não é possível subir!")
                return
            self.posicao_atual[1] -= 1
        elif direcao == "baixo":
            if y == len(self.estrutura_para_limpar) - 1:
                print("Não é possível descer!")
                return
            self.posicao_atual[1] += 1
        elif direcao == "esquerda":
            if x == 0:
                print("Não é possível mover-se para a esquerda!")
                return
            self.posicao_atual[0] -= 1
        elif direcao == "direita":
            if x == len(self.estrutura_para_limpar[y]) - 1:
                print("Não é possível mover-se para a direita!")
                return
            self.posicao_atual[0] += 1

    def ligar(self, estrutura_para_limpar):
        if estrutura_para_limpar is None or len(estrutura_para_limpar) == 0:
            print("Não há estrutura para limpar")
            self.mostrar_estrutura()
            return
        self.estrutura_para_limpar = estrutura_para_limpar

    def limpar(self):
        x, y = self.posicao_atual
        self.estrutura_para_limpar[y][x] = True
        self.bolsa.espaco_disponivel -= 1
        self.bolsa.sujeira_coletada += 1

    def verificar_bolsa(self):
        if self.bolsa.espaco_disponivel == 0:
            self.voltar_ao_inicio()
            self.esvaziar_bolsa()

    def voltar_ao_inicio(self):
        self.posicao_atual = [0, 0]

    def esvaziar_bolsa(self):
        self.bolsa.espaco_disponivel = 10

    def mostrar_posicao_atual(self):
        print(f'x: {self.posicao_atual[0]} y: {self.posicao_atual[1]}')

    def recarregar_energia(self):
        pass

    def mostrar_estrutura(self):
        for i in range(len(self.estrutura_para_limpar)):
            line = ""
            for j in range(len(self.estrutura_para_limpar[i])):
                x, y = self.posicao_atual

                if y == i and x == j:
                    line += "| (ASP) |"
                else:
                    line += "| LIMPO |" if self.estrutura_para_limpar[i][j] else "| SUJO  |"
            print(line)

    def get_posicao_atual(self):
        return self.posicao_atual

    def get_estrutura_para_limpar(self):
        return self.estrutura_para_limpar

    def get_energia(self):
        return self.energia

    def get_bolsa(self):
        return self.bolsa


class Bolsa:
    def __init__(self):
        self.espaco_disponivel = 10
        self.sujeira_coletada = 0


def mostrar_status_do_aspirador(aspirador):
    print(f'Espaço disponível na bolsa: {aspirador.get_bolsa().espaco_disponivel}')
    print(f'Sujeira coletada: {aspirador.get_bolsa().sujeira_coletada}')
    print(f'Energia: {aspirador.get_energia()}')


if __name__ == "__main__":
    aspirador = Aspirador()

    tudo_limpo = False

    estrutura = [
        [1, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 1, 0, 1]
    ]

    direcao = "baixo"
    virar_direita = False

    while not tudo_limpo:
        aspirador.ligar(estrutura)
        aspirador.mostrar_estrutura()
        aspirador.mostrar_posicao_atual()
        mostrar_status_do_aspirador(aspirador)

        pos_x, pos_y = aspirador.get_posicao_atual()
        chegou_ao_final = pos_y == 0 and pos_x == len(aspirador.get_estrutura_para_limpar()[pos_y]) - 1

        if not aspirador.get_estrutura_para_limpar()[pos_y][pos_x]:
            print("Limpando...")
            aspirador.limpar()

        if virar_direita:
            aspirador.mover("direita")
            virar_direita = False
        else:
            if direcao == "baixo":
                aspirador.mover("baixo")
            elif direcao == "cima":
                aspirador.mover("cima")

            pos_x, pos_y = aspirador.get_posicao_atual()
            chegou_limite_profundidade = pos_y == len(aspirador.get_estrutura_para_limpar()) - 1
            chegou_limite_altura = pos_y == 0

            if chegou_limite_profundidade:
                direcao = "cima"
                virar_direita = True
            elif chegou_limite_altura:
                direcao = "baixo"
                virar_direita = True

            if chegou_ao_final:
                tudo_limpo = True
                aspirador.voltar_ao_inicio()