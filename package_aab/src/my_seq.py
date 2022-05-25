# -*- coding: utf-8 -*-
"""
Package dos algoritmos implementados em aula
Algoritmos Avançados de Bioinformática
"""

"""
Class:MySeq
"""
import re

class MySeq:
    """
    Classe que apresenta os métodos que permitem a manipulação de sequências de ADN, RNA e proteínas.
    """

    def __init__(self, seq: str, seq_type: str):
        """
        Método que guarda os valores utilizados nos restantes métodos.
        :param seq: sequência introduzida
        :param seq_type: tipo de sequênia introduzida
        """
        self.seq = seq.upper()
        self.seq_type = seq_type

    def __len__(self) -> int:
        """
        Método que devolve o comprimento da sequência introduzida.
        :return: comprimento da sequência introduzida
        """
        return len(self.seq)

    def __getitem__(self, n: int) -> str:
        """
        Método que permite devolver um item a partir da indexação de uma instância.
        :param n: posição do valor que queremos devolver.
        :return:
        """
        return self.seq[n]

    def __str__(self) -> str:
        """
        Método que devolve os objetos da classe como strings.
        :return: devolve o tipo da sequência e a sequência como strings.
        """
        return self.seq_type + ":" + self.seq

    def __repr__(self) -> str:
        """
        Método que representa os objetos da classe como strings.
        :return: objetos como strings.
        """
        return str(self.seq)

    def printSeq(self):
        """
        Método que imprime as sequências introduzidas.
        """
        print(self.seq)

    def checkSeqType(self):
        """
        Método que verifica o tipo de sequências.
        :return: devolve os possíveis caracteres das sequências.
        """
        if (self.seq_type == "dna"):
            return "ACGT"
        elif (self.seq_type == "rna"):
            return "ACGU"
        elif (self.seq_type == "protein"):
            return "ACDEFGHIKLMNPQRSTVWY"
        else:
            return None

    def validateSeqRE(self) -> bool:
        """
        Método que valida as sequência de acordo com o tipo de caracteres presentes através de expressões regulares.
        :return: valor de "False" ou "True" se as sequências forem inválidas ou válidas, respetivamente.
        """
        if (self.seq_type == "dna"):
            if re.search("[^ACTGactg]", self.seq) != None:
                return False
            else:
                return True
        elif (self.seq_type == "rna"):
            if re.search("[^ACUGacug]", self.seq) != None:
                return False
            else:
                return True
        elif (self.seq_type == "protein"):
            if re.search("[^ACDEFGHIKLMNPQRSTVWY_acdefghiklmnpqrstvwy]", self.seq) != None:
                return False
            else:
                return True
        else:
            return False

    def transcription(self):
        """
        Método que devolve a sequência transcrita.
        :return: sequência transcrita.
        """
        if (self.seq_type == "dna"): #se a sequência for do tipo DNA
            return MySeq(self.seq.upper().replace("T", "U"), "rna") #troca o nucleótido Timina (T) por Uracilo (U)
        else:
            return None

    def reverseComplement(self):
        """
        Método que transforma a sequência introduzida no seu complemento inverso
        :return: sequência do complemento inverso
        """
        if (self.seq_type != "dna"): #aplica o método apenas para sequências do tipo DNA
            return None
        else:
            self.seq = self.seq[::-1].lower()
            inv_comp = self.seq.replace("a","T").replace("g","C").replace("c","G").replace("t","A")
        return inv_comp

    def rnaCodon(self) -> list:
        """
        Método que procura os codões da sequência, i.e, devolve a sequência de três em três nucleótidos.
        """
        codon = re.findall(r'...', self.seq)
        return codon

    def seqTranslation(self, initial_pos: int = 0):
        """
        Método que processa a tradução da sequência.
        :param initial_pos: determina a posição inicial da leitura da sequência
        :return:
        """
        if (self.seq_type != "dna"): #verifica se a sequência é do tipo DNA.
            return None
        seq = self.seq.upper()
        seq_amino = "" #inicia uma string vazia
        for pos in range(initial_pos, len(seq) - 2, 3): #leitura de cada caractér da posição
            #inicia na posição inicial e para dois nucleótidos antes do final da sequência,
            # de forma a ler o último codão inteiro
            # incrementa 3 nucleótidos (codões)
            codon = seq[pos:pos+3] #leitura de codões
            seq_amino += self.codonTranslate(codon) #adiciona a proteína correspondente ao codão
        return MySeq(seq_amino, "protein")

    def orfs(self):
        """
        Método que determina as open reading frames (ORF), i.e, as sequências compreendidas entre o codão de iniciação
        e o codão STOP. Gera seis reading frames da sequência de DNA e do complemento inverso.
        :return: devolve as ORF's
        """
        if (self.seq_type != "dna"):
            return None
        frames = [] #lista de frames
        frames.append(self.seqTranslation(0)) #inicia a leitura da frame na primeira posição
        frames.append(self.seqTranslation(1)) #inicia a leitura da frame na segunda posição
        frames.append(self.seqTranslation(2)) #inicia a leitura da frame na terceira posição
        inv_comp = self.reverseComplement() #determina o complemento inverso
        frames.append(inv_comp.seqTranslation(0)) #inicia a leitura da frame na última posição
        frames.append(inv_comp.seqTranslation(1)) #inicia a leitura da frame na penúltima posição
        frames.append(inv_comp.seqTranslation(2)) #inicia a leitura da frame na antepenúltima posição
        return frames

    def codonTranslate(self, cod: str) -> str:
        """
        Método que traduz os codões nos respetivos aminoácidos.
        :param cod: codão a procurar na tabela de codões
        :return: sequência de aminoácidos
        """
        codon_table = {"GCT": "A", "GCA": "A", "GCC": "A", "TGT": "C", "TGC": "C",
              "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "TTT": "F", "TTC": "F",
              "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G", "CAT": "H", "CAC": "H",
              "ATA": "I", "ATT": "I", "ATC": "I",
              "AAA": "K", "AAG": "K",
              "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
              "ATG": "M", "AAT": "N", "AAC": "N",
              "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
              "CAA": "Q", "CAG": "Q",
              "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
              "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
              "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
              "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
              "TGG": "W",
              "TAT": "Y", "TAC": "Y",
              "TAA": "_", "TAG": "_", "TGA": "_"} #dicionário em que as chaves são os codões e os valores os aminoácidos
        if cod in codon_table:
            amin = codon_table[cod] #guarda o aminoácido correspondente ao codão
        else:
            amin = "X"  #marca erros de procura com um X
        return amin

    def longestProteinSeq(self):
        """
        Método que procura a sequência proteíca mais comprida.
        :return: maior sequência proteíca.
        """
        if (self.seq_type != "prot"): #determina se o tipo de sequência é uma proteína
            return None
        seq_amin = self.seq.upper()
        current_prot = "" #string vazia para guardar a sequência que está a ser lida
        longest_prot = "" #string vazia para guardar a sequência da maior proteina
        for aa in seq_amin: #lê cada aminoácido na sequência
            if aa == "_": #verifica se é um codão stop
                if len(current_prot) > len(longest_prot): #verifica se a proteína que está a ser lida é superior
                    #à última proteina gaurdada na lista de maior proteínas
                    longest_prot = current_prot #se for, guarda a proteína atual como a mais longa
                current_prot = "" #volta a zerar a lista de proteínas atuais
            else:
                if len(current_prot) > 0 or aa == "M": #verifica se a proteina tem um cumprimento superior a zero
                    #e começa a ler se o aminoácido for uma metionina.
                    current_prot += aa #adiciona o aminoácido à lista
        return MySeq(longest_prot, "protein")

    def allProtein(self):
        """
        Método que procura todas as proteínas encontradas na sequência.
        :return:
        """
        if (self.seq_type != "prot"): #verifica se a sequência é uma proteína
            return None
        seq_aa = self.seq.upper()
        current_prot = [] #lista da proteína a ser lida
        prot_list = [] #lista de proteínas totais
        for aa in seq_aa: #lê os aminoácidos da sequência
            if aa == "_": #verifica se é um codão stop
                if current_prot:
                    for p in current_prot:
                        prot_list.append(MySeq(p, "protein")) #adiciona as proteínas lidas na lista de proteínas totais
                    current_prot = [] #zera a lista de proteínas lidas
            else:
                if aa == "M": #verifica se é um codão de iniciação
                    current_prot.append("")
                for i in range(len(current_prot)):
                    current_prot[i] += aa #adiciona os aminoácidos à lista
        return prot_list

    def largestOrfProtein(self):
        """
        Método procura a maior proteina nas open reading frames (ORF).
        :return: devolve a maior proteina das ORF.
        """
        if (self.seq_type != "prot"): #verifica se a sequência é do tipo proteina
            return None
        larg_prot = MySeq("", "prot")
        for orf in self.orfs(): #lê as ORF
            prot = orf.largestOrfProtein() #define as ORF como proteinas
            if len(prot.seq) > len(larg_prot.seq): #verifica se a proteina a ler tem um comprimento superior
                # à maior proteina.
                larg_prot = prot #se sim, define a proteina como a maior proteina
        return larg_prot