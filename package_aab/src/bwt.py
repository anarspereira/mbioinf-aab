# criação de matriz de Burrows-Wheeler (M) de uma sequência -> na prática, não se guarda toda a matriz
# mas apenas a 1ª e última colunas
# a 1ª coluna é a ordenação lexicográfica dos caracteres do alfabeto
# a última coluna é também chamada Transformada de Burrows-Wheeler (BWT)
# depois temos que proceder à recuperação da sequência original da BWT utilizando a primeira e ultima coluna guardadas
# para isto temos que numerar as ocorrências de cada símbolo (método: find_ith_occ)
# o método inverse_bwt vai-nos fazer a recuperação da sequência
# além disto, podemos encontrar padrões com a BWT: temos que pensar num algoritmo que só use 1ª e ultima coluna
# O 1º passo passa por identificar o último símbolo do padrão e ver onde ele faz match na última coluna
# , próximo passo: identificar posições desses símbolos na primeira linha, atualizando os índices T (top) e B (bottom)
# próximo passo: procurar nas linhas selecionadas (entre T e B) as ocorrências do segundo símbolo do padrão na última
# coluna, identificá-los na 1º coluna e atualizar T e B; Passo final: identificar o primeiro símbolo do padrão
from typing import List


class BWT:
    """
    Classe para implementação do algoritmo Burrows-Hweeler onde diferentes métodos foram criados. O algoritmo é útil para
    compactar sequências de grande tamanho, reduzindo assim o seu espaço. Além disso, é possível encontrar padrões no
    formato de compactação de forma eficiente.
    """
    def __init__(self, seq='', buildsufarray=False, sa=None):
        self.bwt = self.build_bwt(seq, buildsufarray)
        self.sa = sa

    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text, buildsufarray=False) -> str:
        """
        Método para construir a matriz para transformação de Burrows-Wheeler.
        :param text: sequência que queremos utilizar
        :param buildsufarray: parâmetro para criar vetor de sufixos. Default: False.
        """
        ls = []  # criar lista para as nossas rotaçoes

        for i in range(len(text)):  # dollar ja incluido na sequencia
            ls.append(text[i:] + text[:i]) # adicionar todas as rotacoes possiveis
        ls.sort()  # ordenar alfabeticamente as sequencias obtidas
        #print(ls)
        # obter a transformada de BWT:
        res = ''
        for i in range(len(text)): # a cada caracter na sequencia
            res += ls[i][len(text) - 1]  # obter ultima coluna da matriz, chamada de Transformada de Burrows-Wheeler (BWT)
        # se buildsufarray for True:
        if buildsufarray:
            self.sa = []
            for i in range(len(ls)):  # para cada elemento na lista das rotações:
                stpos = ls[i].index("$")  # dá o index de cada sequência onde o $ está
                self.sa.append(len(text) - stpos - 1)  # adicionar a posição inicial de cada de cada sufixo. Array de sufixos permitem
                # procura da posição de matches com BWT
        return res

    # recuperação da sequencia original
    def inverse_bwt(self) -> str:
        """
        Método para obter a sequência original
        :return: string da sequência original
        """
        # note-se que o 1.º símbolo da sequência deve estar a seguir ao $
        firstcol = self.get_first_col()  # chamar metodo para obter a 1 coluna para indexar
        res = ""
        c = "$"  # $ é primeiro carater
        occ = 1  # primeira ocorrencia
        for i in range(len(self.bwt)):  # percorrer bwt (ultima coluna)
            pos = findithocc(self.bwt, c, occ)  # saber o índice de $ na primeira ocorrência
            c = firstcol[pos]  #na primeira coluna diz-nos a que letra corresponde #dá-nos o valor de "$"
            occ = 1
            k = pos - 1 #posição anterior ao primeiro índice de "$"
            while firstcol[k] == c and k >= 0:  #enquanto o valor da posição anterior a "$" for igual ao valor de $
            #e o índice de k for superior a zero
                occ += 1  # aumentar proxima ocorrencia
                k -= 1  # definir k para o próximo ciclo #k torna-se igual pos - 2
            res += c  # adicionar carater
        return res

    # implementação da procura de padrões a partir da BWT
    def last_to_first(self) -> List:
        """
        Método para criar a tabela com a última coluna e com a primeira
        :return: lista padrões conhecidos
        """
        res = []
        firstcol = self.get_first_col()  # chamar método para obter a primeira coluna
        for i in range(len(firstcol)):  # para cada elemento da primeira coluna
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1
            val = findithocc(firstcol, c, ocs)
            res.append(val)
        return res

    def get_first_col(self) -> List[str]:
        """
        Método para recuperar a primeira coluna. de salientar que a primeira coluna é a ordenação alfabética da transformada

        :return: lista da primeira coluna
        """
        primeira_col = []
        for c in self.bwt:  # para cada simbolo na transformada
            primeira_col.append(c)  # adicionar à lista o caracter a iterar da transformada
        primeira_col.sort()  # colocar por ordem alfabética
        return primeira_col  # temos a nossa primeira coluna

    def bw_matching(self, pattern=str) -> List[int]:
        """
        Método para procurar padrões a partir da trasnformação de Burrows-Wheeler.
        :param pattern: padrão que queremos encontrar
        :return: lista com matches
        """
        lf = self.last_to_first()  # chamar o método para fazer matriz
        res = []
        # O 1.º passo passa por identificar o último símbolo do padrão e ver onde ele faz match na última coluna
        # identificar posições desses símbolos na primeira linha, atualizando os índices T (top) e B (bottom)
        top = 0  # Posiçao inicial na primeira coluna
        bottom = len(self.bwt) - 1  # posiçao final na primeira coluna
        flag = True
        while flag and top <= bottom:  # enquanto o bottom for maior ou igual ao top continuamos:
            if pattern != "":  # se o padrão for diferente de string vazia
                symbol = pattern[-1]  # último símbolo do padrão
                pattern = pattern[:-1]  # todos os elementos menos o último do padrão
                lmat = self.bwt[top:(bottom+1)]  # coluna utilizando top e bottom
                if symbol in lmat:  # para cada carater na coluna (top-bottom) (percorrer a coluna) se o simbolo estiver na matriz:
                    topindex = lmat.index(symbol) + top  # configurar o top na coluna
                    bottomindex = bottom - lmat[::-1].index(symbol)  # configurar o bottom na coluna
                    top = lf[topindex]  # ir fazendo a matriz com os novos top, bot
                    bottom = lf[bottomindex]
                else:
                    flag = False  # caso símbolo não esteja na matriz, abortar
            else: #
                for i in range(top, bottom + 1):
                    res.append(i)
                flag = False
        print("res: ", res)
        return res

    def bw_matching_pos(self, patt) -> List:
        """
        Método que procura os matches de um padrão
        :param patt: padrão que queremos encontrar
        :return: lista com os matches encontrados
        """
        res = []
        matches = self.bw_matching(patt)  # obter matches
        for m in matches:  # para cada match:
            res.append(self.sa[m])  # append para cada array de sufixos
        res.sort()
        return res  # retornar lista com matches encontrados


def findithocc(le, elem, index):
    """
    Método que permite descobrir a posição da i-ésima ocorrência de um símbolo
    numa lista (retorna -1 caso não ocorra).
    :param le: matriz em que vamos procurar
    :param elem: elemento a procurar
    :param index: ocorrência a procurar
    """
    j, k = 0, 0  # j, numero de vezes que já encontrou; k, ndex que percorre a seq.
    while k < index and j < len(le):
        if le[j] == elem:
            k += 1
            if k == index:
                return j
        j += 1
    return -1
