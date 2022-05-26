class BoyerMoore:
    def __int__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.occ = {}

        # criação de listas de tamanho igual ao padrão +1. cada uma inicializada com zeros
        self.f = [0] * (len(self.pattern) + 1)  # lista do tamanho do padrão, inicializada a 0
        self.s = [0] * (len(self.pattern) + 1)  # lista do tamanho do padrão, inicializada a 0

        #correr processamento
        self.process_bcr()
        self.process_gsr()

    def process_bcr(self):
        for s in self.alphabet:  # a cada carater no alfabeto:
            self.occ[s] = -1  # atribuir o valor de -1 no dicionario para cada carater. chave s e valor -1
        for j in range(0, len(self.pattern)):  # para cada indice (j) entre 0 e o tamanho do padrão:
            self.occ[self.pattern[j]] = j  # procurar entrada no dicionário e atualizar o valor para o indice j

    def process_gsr(self):
        i = len(self.pattern)  # inicializar i com tamanho do padrão
        j = len(self.pattern) + 1  # inicializar j com tamanho do padrão +1

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

        :param text:
        :return: lista com valores
        """
        i = 0
        res = []
        while i <= len(text) - len(self.pattern):
            j = len(self.pattern) - 1
            while (j >= 0) and (self.pattern[j] == text[j+i]):
                j -= 1
            if j < 0:
                res.append(i)
                i += self.s[0]
            else:
                c = text[j+i]
                i = max(self.s[j+1],(j-self.occ[c]))
        return res

##

