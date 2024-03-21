def apriori (contagemtodositemset,divisao,suporteminimo):
    """ GERAR UMITEMSET """
    global numeroitemset
    global repete
    print ("------------1 - ITEMSET-------------")
    print ("\n")
    print ("Gerando 1-itemset")
    umitemset = [[0 for coluna in range (0,2) ] for linha in range(0,469)]
    """ PERCORRE BANCO PRA CONTAGEM DE 1-ITEMSET"""
    itens = []
    print ("Percorrendo banco e contando (1-itemset)")
    for line in divisao:
        #print (b)
        for x in line.split(' '):
            if x != ('\n'):
                c = int(x)
            for a in range (0,469):
                umitemset [a][0]=a
                if c == a:
                    umitemset [a][1] += 1
    """ SEPARA ITENS QUE ESTAO ACIMA DO SUPORTE"""

    a=0
    print ("Eliminando itens abaixo do suporte minimo (1-itemset)")
    podaumitemset=[]
    for line in umitemset:
        c = umitemset[a][1]
        #print (c)
        if c >= suporteminimo:
            itens.append(umitemset[a][0])
            podaumitemset.append(line)
            contagemtodositemset.append(line)
        a+=1
    #print (podaumitemset)

    doisitemset = []
    #---------------------------------------------------Inicio 2-itemset
    #print (itens)
    print ("\n")
    print ("------------2 - ITEMSET-------------")
    print ("\n")
    print ("Gerando 2-itemset")
    a = len (itens) * len (itens)
    geradoisitemset = [[0 for coluna in range (0,2) ] for linha in range(a)]
    e=0
    for a in itens:
        item1 = a
        for i in itens:
            item2 = i
            if item1 != item2:
                geradoisitemset[e][0]=item1
                geradoisitemset[e][1]=item2
                e+=1
    for a in geradoisitemset:
        b = set (a)
        if 0 not in b and b not in doisitemset:
            doisitemset.append(b)

    #print ("DOISITEMSET")

    #print (doisitemset)
    print ("Percorrendo banco e contando (2-itemset)")
    #f = open ("bancodedadosreduzido2.txt",'r')
    contagemitemset = [[0 for coluna in range (0,2) ] for linha in range (len(doisitemset))]
    for line in divisao:
        linha = []
        for x in line.split(' '):
            if x != ('\n'):
                linha.append(int(x))
        #print (linha)
        linha = set (linha)
        a=0
        for x in doisitemset:
            x = set (x)
        #print (x)
            z = set.issubset( x, linha)
        #print (z)
            if z == True:
                contagemitemset [a][1] +=1
                contagemitemset [a][0] = x                
            a +=1
    itens = []
    print ("Eliminando itens abaixo do suporte minimo (2-itemset)")
    for a in range (len(contagemitemset)):
        c = contagemitemset[a][1]
        if c >= suporteminimo:
            itens.append(list (contagemitemset[a][0]))
    itemsetanterior = itens

    podadoisitemset = [[0 for coluna in range (0,2) ] for linha in range (len(itens))]
    d=0
    for a in range (len(contagemitemset)):
        c = contagemitemset[a][1]
        if c >= suporteminimo  :
            podadoisitemset [d][0] = contagemitemset [a][0]
            podadoisitemset [d][1] = contagemitemset [a][1]
            d +=1
    for line in podadoisitemset:
        contagemtodositemset.append(line)
#----------------------------------------------------------Termino 2-itemset
#----------------------------------------------------------Inicio 3-itemset
    print ("\n")
    print ("------------3 - ITEMSET-------------")
    print ("\n")
    itensseparados = []
    for linha in itens:
        for elemento in linha:
            itensseparados.append(elemento)
    print ("Gerando 3-itemset")
    tamanhopragerar = len (podadoisitemset) *len (podadoisitemset)
    geraitemset = [[0 for coluna in range (0,2) ] for linha in range (tamanhopragerar)]
    geratresitemset = []
    for a in range (len(podadoisitemset)):
        item1 = podadoisitemset [a][0]
        for i in range (len(podadoisitemset)):
            item2 = podadoisitemset [i][0]
            if item1 != item2:
                #print (geratresitemset)
                a = set (item1 | item2)
                if a not in geratresitemset:
                    geratresitemset.append (a)
                    
    print ("Removendo 4-itemset de 3-itemset e itemsets repetidos")            
    tresitemset = []
    for line in geratresitemset:
        if len (line) == 3:
            tresitemset.append (line)

    print ("Percorrendo banco e contando (3-itemset)")

    #f = open ("bancodedadosreduzido2.txt",'r')
    contagemitemset = [[0 for coluna in range (0,2) ] for linha in range (len(tresitemset))]
    for line in divisao:
        linha = []
        for x in line.split(' '):
            if x != ('\n'):
                linha.append(int(x))
        #print (linha)
        linha = set (linha)
        a=0
        for x in tresitemset:
            x = set (x)
            z = set.issubset( x, linha)
            if z == True:
                contagemitemset [a][1] +=1
                contagemitemset [a][0] = x                
            a +=1
    #print (contagemitemset)
    print ("Eliminando itens abaixo do suporte minimo (3-itemset)")
    itens = []
    for a in range (len(contagemitemset)):
        c = contagemitemset[a][1]
        if c >= suporteminimo:
            itens.append(list (contagemitemset[a][0]))

    podaitemset = [[0 for coluna in range (0,2) ] for linha in range (len(itens))]
    d=0
    for a in range (len(contagemitemset)):
        c = contagemitemset[a][1]
        if c >= suporteminimo:
            podaitemset [d][0] = contagemitemset [a][0]
            podaitemset [d][1] = contagemitemset [a][1]
            d +=1
    for line in podaitemset:
        contagemtodositemset.append(line)




#-------------------------------------------------- Calcular Confiancaa

#---------------------- Fim do calculo de confianca
    
 #----------------------------------------------------------Termino 3-itemset

    numeroitemset = 3
    repete = 1
    continua = True
    while repete==1:
        itemsetanterior = podaitemset
        numeroitemset+=1
        geraitemsets (divisao,itemsetanterior,numeroitemset,contagemtodositemset,confiancaminima)
        if continua == True:
            continua = False
        else:
            repete = 0
    return (contagemtodositemset,numeroitemset)
def geraregras (conjunto,numeroitensconjunto):
    A =  [list(x) for x in itertools.combinations(conjunto, numeroitensconjunto)]
    global regras
    regras = [[0 for coluna in range (0,2) ] for linha in range (len(A))]
    a=0
    for x in A:
        x = set (x)
        itemparagerarregra = conjunto.difference(set (x))
        regras [a][0] = itemparagerarregra
        regras [a][1] = x
        a+=1
        
    return (regras)
def geraitemsets (divisao,itemsetanterior,numeroitemset,contagemtodositemset,confiancaminima):
    print ("\n")
    print ('----------------------  ' + str (numeroitemset)+ ' - ITEMSET----------------- ')
    print ("\n")

    print ('Gerando ' +str (numeroitemset)+' -itemset')
    #tamanhopragerar = len (itemsetanterior) *len (itemsetanterior)
    #geraitemset = [[0 for coluna in range (0,2) ] for linha in range (tamanhopragerar)]
    geraitemset = []
    for a in range (len(itemsetanterior)):
        item1 = itemsetanterior [a][0]
        for i in range (len(itemsetanterior)):
            item2 = itemsetanterior [i][0]
            if item1 != item2:
                #print (geratresitemset)
                a = set (item1 | item2)
                if a not in geraitemset and len (a) == numeroitemset:
                    geraitemset.append (a)
                    #print (b)
    print ('Removendo ' + str (numeroitemset+1) +'-itemset de '+str (numeroitemset)+'-itemset e itemsets repetidos ')     
    itemsetanterior = []
    print ('Percorrendo banco e contando ' +str (numeroitemset)+' ')

    #f = open ("bancodedadosreduzido2.txt",'r')
    contagemitemset = [[0 for coluna in range (0,2) ] for linha in range (len(geraitemset))]
    for line in divisao:
        linha = []
        for x in line.split(' '):
            if x != ('\n'):
                linha.append(int(x))
        #print (linha)
        linha = set (linha)
        a=0
        for x in geraitemset:
            x = set (x)
            z = set.issubset( x, linha)
            if z == True:
                contagemitemset [a][1] +=1
                contagemitemset [a][0] = x                
            a +=1
#print (contagemitemset)
    print ('Eliminando itens abaixo do suporte minimo (' +str (numeroitemset)+'-itemset)')
    itens = []
    for a in range (len(contagemitemset)):
        c = contagemitemset[a][1]
        if c >= suporteminimo:
            itens.append(list (contagemitemset[a][0]))

    podaitemset = [[0 for coluna in range (0,2) ] for linha in range (len(itens))]
    d=0
    for a in range (len(contagemitemset)):
        c = contagemitemset[a][1]
        if c >= suporteminimo:
            podaitemset [d][0] = contagemitemset [a][0]
            podaitemset [d][1] = contagemitemset [a][1]
            d +=1
            continua=True
    for line in podaitemset:
        contagemtodositemset.append(line)

    return (repete,podaitemset,contagemtodositemset,numeroitemset)


# --------------------------------------------------------PROGRAMA-------------------------------------------------------------------------------------------------------------------------------
import time
import itertools
from time import clock
import os
t1 = clock()
print ("PROJETO Regras de Associacao (BigData)- Saulo Ramos - UFABC -Engenharia da Informacao")
print ("\n")

print ("\n")
f = open ("accidents.dat",'r')
fileobj = open("SON - Suporte + Confianca em %.txt",'w')
global contagemtodositemset
contagemtodositemset = []
a=0
b=0
c=0
numerodetransacoes=0
mylist = []
z=0
print ("Digite o  valor do suporte minimo ")
suporteminimo = int ( input())
print ("Digite o  valor da confianca minima  em %")
confiancaminima = int (input())
confiancaminima = confiancaminima/100

print ("Digite o numero de partes em que deseja dividir o banco de dados")
numerodepartes = int (input())
suporteminimo = suporteminimo/numerodepartes
""" DIVIDIR BANCO"""
for line in f:
    numerodetransacoes +=1
transacaodedivisao = numerodetransacoes/numerodepartes

divisao=[]
f = open ("accidents.dat",'r')
parte = 0
nt=0
for line in f:
    nt+=1
    if numerodetransacoes==nt:
        divisao.append (line)
        apriori (contagemtodositemset,divisao,suporteminimo)
        divisao = []

    else:
        if len(divisao) < transacaodedivisao:
            divisao.append(line)
        else:        
            apriori (contagemtodositemset,divisao,suporteminimo)

            divisao = []
            divisao.append (line)
      
print (" ------------------ FIM DO SON ---------------")
#print (contagemtodositemset)


#-----------SEPARA ITENS
separaitens = []
for line in range (len(contagemtodositemset)):
    if type(contagemtodositemset[line][0]) == int:
        separaitens.append(contagemtodositemset[line])
tamanhoconjunto = 0
for line in range (len(contagemtodositemset)):
    if type (contagemtodositemset[line][0]) == set:
        if len (contagemtodositemset[line][0]) >tamanhoconjunto:
            tamanhoconjunto = len(contagemtodositemset[line][0])
    
for a in range (2,tamanhoconjunto+1):
    for line in range (len(contagemtodositemset)):
        if type (contagemtodositemset[line][0]) == set and len(contagemtodositemset[line][0]) == a:
            separaitens.append (contagemtodositemset[line])
#-----------------FIM SEPARA ITENS
#-------ENXUGA MATRIZ
enxugamatriz =[]
for a in range (len(separaitens)):
    if separaitens[a][0] not in enxugamatriz:
        enxugamatriz.append (separaitens[a][0])
somageral =  [[0 for coluna in range (0,2) ] for linha in range (len(enxugamatriz))]
for line in range (len(enxugamatriz)):
    somageral[line][0] = enxugamatriz [line]
    for a in range (len(separaitens)):
        if separaitens[a][0] == somageral[line][0]:
            somageral[line][1] += separaitens [a][1]
suporteminimo = suporteminimo*numerodepartes
poda = []
for line in range (len(somageral)):
    if somageral [line][1]>=suporteminimo:
        poda.append (somageral[line])
#Regras itens sets
geratabelaconfianca = []
regrasfim=[]
for line in range (len(poda)):
    if type (poda[line][0]) != int:
        conjunto = poda[line][0]
        numeroitensconjunto = len (poda[line][0])
        while numeroitensconjunto != 1:
            numeroitensconjunto -=1
            #if numeroitensconjunto == 0:
             #   break
            geraregras (conjunto,numeroitensconjunto)
            regrasfim.append (regras)
    
tabelaregras = []
print ("Calculando Confianca ")
for b in regrasfim:
    for x in b:
        tabelaregras.append (x)

#print (tabelaregras)
tabelaconfiancafim = [[0 for coluna in range (0,4) ] for linha in range (len(tabelaregras))]
for line in range (len (tabelaregras)):
    tabelaconfiancafim [line][0] = tabelaregras [line][0]
    tabelaconfiancafim [line][1] = tabelaregras [line][1]
    #print (tabelaconfiancafim[line])
    conjunto = set (tabelaconfiancafim [line][0] | tabelaconfiancafim [line][1])
    for a in range (len(somageral)):
        if somageral [a][0] == conjunto:
            suporteconjunto = somageral [a][1]
            tabelaconfiancafim [line][2] = suporteconjunto
            tabelaconfiancafim [line][3] = suporteconjunto

for numero in range (0,469):
    for line in range (len(tabelaconfiancafim)):
        for linha in range (len(somageral)):
            if len (tabelaconfiancafim [line][0]) == 1 and numero in tabelaconfiancafim [line][0] :
                #print (numero)
                if numero == somageral[linha][0]:
                    tabelaconfiancafim[line][3] = tabelaconfiancafim[line][3]/somageral[linha][1]

for line in range (len(tabelaconfiancafim)):
    for linha in range (len(somageral)):
        if tabelaconfiancafim [line][0] == somageral[linha][0]:
            tabelaconfiancafim[line][3] = tabelaconfiancafim[line][3]/somageral[linha][1]
                
        
"""                
        if tabelaconfiancafim [a][0]==somageral[b][0]:
            tabelaconfiancafim [a][3] = tabelaconfiancafim[a][2]/somageral [b][1]
for line in tabelaconfiancafim:
    print (line)
    os.system('pause')"""
"""for c in range (len(somageral)):
                z = []
                z.append(somageral [c][0])
                #print ("aqui")
                print (z)
                for i in tabelaconfiancafim:
                    print (i)
                    print ("whats")
                    os.system('pause')
                if z == (list (int(i) for i in tabelaconfiancafim [line][0])):
                    # ("FOI")
                    suporteitem = somageral[c][1]
                    print ('Contagem item' +str( suporteitem )+' -- Contagem Conjunto' + str(suporteconjunto) +'')
                    os.system('pause')
                    #print (suporteitem)
                    confianca = suporteconjunto/suporteitem
                    tabelaconfiancafim [line][3] = confianca"""
podatabelaconfianca = [[0 for coluna in range (0,4) ] for linha in range (len(tabelaconfiancafim))]
print ("Eliminando itens abaixo da Confianca minima ")
for line in range (len (tabelaconfiancafim)):
    if tabelaconfiancafim [line][3] >= confiancaminima:
        podatabelaconfianca [line][0] = tabelaconfiancafim [line][0]
        podatabelaconfianca [line][1] = tabelaconfiancafim [line][1]
        podatabelaconfianca [line][2] = tabelaconfiancafim [line][2]
        podatabelaconfianca [line][3] = tabelaconfiancafim [line][3]

fileobj.write ("---------------FREQUENCIA DOS ITENS-------------")
fileobj.write("\n")
for line in poda:
    fileobj.write(str(line))
    fileobj.write("\n")
fileobj.write ("---------------REGRAS DE ASSOCIACAO-------------")
fileobj.write("\n")
for line in range (len(podatabelaconfianca)):
    fileobj.write (' ' + str (podatabelaconfianca[line][0])+ ' => ' + str (podatabelaconfianca[line][1])+' (sup = '+str (podatabelaconfianca[line][2])+'),(conf = '  + str (podatabelaconfianca[line][3]) +')')
    fileobj.write("\n")

#print (divisao)

tempodeexecucao=clock()-t1
fileobj.write(str(tempodeexecucao))
fileobj.close()
#----------------------------------------------------------Termino 2-itemset


print ("\n")
print ("-----------------------PROGRAMA FINALIZADO-------------------")
print ("-----------------------Os resultados estao em resultados.txt-------------------")

#geratresitemset = [list(x) for x in itertools.combinations(range(1,469), 3)]
#geraquatroitemset = [list(x) for x in itertools.combinations(range(1,469), 4)]


# FALTA GERAR TABELA E ELIMINAR ITENS PARA 4-itemset em diante


print ("Pressione Enter para Sair")
a = input()
