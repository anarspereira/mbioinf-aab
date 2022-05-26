# este algoritmo é baseado em duas regras:
# – Bad-character rule
# – Good suffix rule
# o bad-character rule, diz podemos avançar para a próxima ocorrência no padrão do símbolo que falhou (ou se não
# existir avançar o máximo possível).
# good suffix rule: Avançar para a próxima ocorrência no padrão da parte que fez match antes de falhar. Se o sufixo não
# ocorre de novo, pode avançar tamanho do padrão.

class BoyerMoore:
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern

        self.occ = {} # criar dicionário

        # criação de listas de tamanho igual ao padrão +1. cada uma inicializada com zeros
        self.f = [0] * (len(self.pattern) + 1)  # lista do tamanho do padrão, inicializada a 0
        self.s = [0] * (len(self.pattern) + 1)  # lista do tamanho do padrão, inicializada a 0

        #correr processamento
        self.process_bcr()
        self.process_gsr()

    def process_bcr(self):
        """
        Método em que um dicionário é criado com todos os símbolos possíveis (occ) como chaves, e os valores definem
        a posição mais à direita em que o símbolo aparece no padrão (-1 significa que não ocorre). Isto permite que
        rapidamente se calcule o número de posições para seguir a procura de acordo com o mismatch no padrão (valor para
        o símbolo no dicionário). De salientar que este valor pode ser negativo, isto quer dizer que a regra neste caso
        não é útil e é ignorada na próxima iteração.
        """
        for s in self.alphabet:  # a cada carater no alfabeto:
            self.occ[s] = -1  # atribuir o valor de -1 no dicionario para cada carater. chave s e valor -1
        for j in range(0, len(self.pattern)):  # para cada indice (j) entre 0 e o tamanho do padrão:
            c = self.pattern[j]  #
            self.occ[c] = j  # procurar entrada no dicionário e atualizar o valor para o indice j

    def process_gsr(self):
        """
        O resultado deste método é gerar uma lista que mantém o número das posições que podem ser seguidas em frente,
        dependendo na posição do mismatch no padrão.
        """
        i = len(self.pattern)  # atribuir i o tamanho do padrão
        j = len(self.pattern) + 1  # atribuir j o tamanho do padrão +1

        self.f[i] = j  # ?

        while i > 0:  # enquanto cobrir o tamanho do padrão
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]: # enquanto j for menor ou igual
                # ao tamanho do padrão e o padrão[i-1] e padrão[j-1] forem diferentes
                if self.s[j] == 0:  # se o valor da lista for igual a 0 no indice j:
                    self.s[j] = j - i  # para esse índice subtrair o valor do tamanho do padrão+1 - iteraçao no padrao(i)
                j = self.f[j]  #
            i -= 1  # ir reduzindo valor de i e j para iteração
            j -= 1
            self.f[i] = j
        j = self.f[0]

        for i in range(0, len(self.pattern)):  # para cada i entre 0 e o tamanho do padrão:
            if self.s[i] == 0:  # se o valor de s[i] estiver igual a 0:
                self.s[i] = j  # novo valor de s[i] passa a ser j
            if i == j:
                j = self.f[j]

    def search_pattern(self, text) -> list[int]:
        """
        Este método permite encontrar um padrão num dado texto, tendo como base o objeto da classe com contém o
        padrão e seu alfabeto.
        :param text: string do texto onde queremos procurar o nosso padrão
        :return: lista com os índices onde começa o padrão
        """
        i = 0 #define a posição inicial como zero
        res = [] #lisra vazia de resultados
        while i <= (len(text) - len(self.pattern)): #enquanto
            j = len(self.pattern) - 1
            while (j >= 0) and (self.pattern[j] == text[j+i]):
                j -= 1
            if j < 0:
                res.append(i)
                i = i + self.s[0]
            else:
                c = text[j+i]
                i += max(self.s[j+1], (j-self.occ[c]))
        return res



