class BWT:
    def __init__(self, seq=""):
        self.bwt = self.buildbwt(seq)

    def buildbwt(self, text):
        rot = []  # criar lista com as nossas rotaçoes
        for char in range(len(text)):
            rot.append(text[char:] + text[:char])  # adicionar todas as rotacoes possiveis
        rot.sort()  # ordenar alfabeticamente as sequencias obtidas
        # print(rot)

        # obter a transformada de BWT:
        res = ''
        for i in range(len(text)):  # a cada caracter na sequencia
            res += rot[i][
                len(text) - 1]  # obter ultima coluna da matriz, chamada de Transformada de Burrows-Wheeler (BWT)
        return res

    # recuperação da sequencia original

    def inverse_bwt(self):
        firstcol = self.get_first_col()  # chamar metodo para obter a 1 coluna para indexar
        res = ""
        c = "$"  # $ é primeiro carater
        occ = 1  # primeira ocorrencia
        for i in range(len(self.bwt)):  # percorrer bwt, ultima coluna
            pos = find_ith_occ(self.bwt, c, occ)  # indexação do $ no incio
            c = firstcol[pos]  # vai buscar a primeira coluna a que letra corresponde
            occ = 1
            k = pos - 1
            while firstcol[
                k] == c and k >= 0:  # serve para ver se quantos mais carateres desses ha na priemria comuna antes
                occ += 1
                k -= 1  # define o k e occ para o priximo for
            res += c
        return res

    # implementação da procura de padrões a partir da BWT

    def last_to_first(self):
        """método para ligar a última coluna com a primeira
        :return: lista """
        res = []

        firstcol = self.get_first_col()  # chamar método para obter a primeira coluna
        for i in range(len(firstcol)):  # para cada elemento da primeira coluna
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1
            val = find_ith_occ(firstcol, c, ocs)
            res.append(val)
        return res

    def get_first_col(self):
        """
        método para recuperar a primeira coluna. de salientar que a primeira coluna é a ordenação alfabética da transformada

        :return:
        """
        primeira_col = []
        for c in self.bwt:  # para cada simbolo na transformada
            primeira_col.append(c)  # adicionar à lista o caracter a iterar da transformada
        primeira_col.sort()  # colocar por ordem alfabética
        return primeira_col  # temos a nossa primeira coluna

#    @staticmethod
#def find_ith_occ(bwt, elem, index):
"""
#função para descobrir posição da i-ésima ocorrência de um símbolo numa lista
#:param bwt:
#:param elem:
#:param index:
#:return: (retorna -1 se não ocorre) """
 #   j, k = 0, 0
 #   while k < index and j < len(bwt):
 #       if bwt[j] == elem:
 #           k = k + 1
 #           if k == index:
 #               return j
#       j += 1
#    return -1  # ão encontradon

def find_ith_occ(l, elem, index):#index da x occorrencia na bwt

    j, k = 0, 0
    while k < index and j < len(l):
        if l[j] == elem:
            k = k + 1
            if k == index:
                return j
        j += 1
    return -1

# def test():
#  seq = " TAGACAGAGA$"
#  bw = BWT(seq)
#   print(bw.bwt)
#   bw.get_first_col()
# test()

def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print(bw.bwt)
    print(bw.last_to_first())


test()
