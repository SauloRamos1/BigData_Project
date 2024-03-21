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
def geraitemsets (itemsetanterior,numeroitemset,contagemtodositemset,confiancaminima):
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
                    b=a
                    geraitemset.append (a)
                    #print (b)
    print ('Removendo' + str (numeroitemset+1) +' -itemset de '+str (numeroitemset)+'-itemset e itemsets repetidos ')     

    print ('Percorrendo banco e contando ' +str (numeroitemset)+' ')

    f = open ("accidents.dat",'r')
    contagemitemset = [[0 for coluna in range (0,2) ] for linha in range (len(geraitemset))]
    for line in f:
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
    print ('Eliminando itens abaixo do suporte mínimo (' +str (numeroitemset)+'-itemset)')
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
# ------- Calcular Confianca
    regrasfim=[]
    numeroitensconjunto = numeroitemset
    for line in range (len(podaitemset)):
        conjunto =podaitemset[line][0]
        numeroitensconjunto -=1
        if numeroitensconjunto == 0:
            break
        geraregras (conjunto,numeroitensconjunto) #CHAMA SUB - ROTINA
        regrasfim.append (regras)
        

    tabelaregras = []
    for b in regrasfim:
        for x in b:
            tabelaregras.append (x)
    tabelaconfiancafim = [[0 for coluna in range (0,4) ] for linha in range (len(tabelaregras))]
    for line in range (len (tabelaregras)):
        tabelaconfiancafim [line][0] = tabelaregras [line][0]
        tabelaconfiancafim [line][1] = tabelaregras [line][1]
        conjunto = set (tabelaconfiancafim [line][0] | tabelaconfiancafim [line][1])
        #mudei aqui(identaca0)
        for a in range (len(contagemtodositemset)):
            if contagemtodositemset [a][0] == conjunto:
                suporteconjunto = contagemtodositemset [a][1]
                tabelaconfiancafim [line][2] = suporteconjunto
                #for b in range (len (tabelaconfiancafim)):
                for c in range (len(contagemtodositemset)):
                    if contagemtodositemset [c][0] == tabelaconfiancafim [line][0]:
                        suporteitem = contagemtodositemset [c][1]
                        confianca = suporteconjunto/suporteitem
                        tabelaconfiancafim [line][3] = confianca
    podatabelaconfianca = [] 
    for line in range (len (tabelaconfiancafim)):
        if tabelaconfiancafim [line][3] >= confiancaminima:
            podatabelaconfianca.append(tabelaconfiancafim[line])
            
    print ('Gravando ' +str (numeroitemset)+ '-itemset+contagem no arquivo')
    fileobj.write ('------------ ' +str (numeroitemset)+ ' - ITEMSET-------------')
    fileobj.write ('\n')
    for line in podaitemset:
        fileobj.write (str(line))
        fileobj.write ('\n')
    fileobj.write ('------------ ' +str (numeroitemset)+ ' - ITEMSET-------------(confiança)')
    fileobj.write ('\n')    
    for line in range (len(podatabelaconfianca)):
        fileobj.write (' ' + str (podatabelaconfianca[line][0])+ ' => ' + str (podatabelaconfianca[line][1])+' (sup = '+str (podatabelaconfianca[line][2])+'),(conf = '  + str (podatabelaconfianca[line][3]) +')')
        fileobj.write("\n")
        
    return (repete,podaitemset)


# --------------------------------------------------------PROGRAMA-------------------------------------------------------------------------------------------------------------------------------
import time
import itertools
from time import clock

print ("PROJETO Regras de Associação (BigData)- Saulo Ramos - UFABC -Engenharia da Informação")
print ("\n")

print ("\n")
f = open ("accidents.dat",'r')
fileobj = open("Apriori Fim - Suporte + Confianca em %.txt",'w')
contagemtodositemset = []
a=0
b=0
c=0
numerodetransacoes=0
mylist = []
z=0
print ("Digite o  valor do suporte mínimo ")
suporteminimo = int ( input())
print ("Digite o  valor da confianca mínima  em %")
confiancaminima = int (input())
confiancaminima = confiancaminima/100
print ("------------1 - ITEMSET-------------")
t1 = clock()
""" GERAR UMITEMSET """
print ("Gerando 1-itemset")
umitemset = [[0 for coluna in range (0,2) ] for linha in range(0,469)]
""" PERCORRE BANCO PRA CONTAGEM DE 1-ITEMSET"""
itens = []
print ("Percorrendo banco e contando (1-itemset)")
for line in f:
    numerodetransacoes +=1
    #print (b)
    for x in line.split(' '):
        if x != ('\n'):
            c = int(x)
        for a in range (0,469):
            umitemset [a][0]=a
            if c == a:
                umitemset [a][1] += 1
""" SEPARA ITENS QUE ESTÃO ACIMA DO SUPORTE"""

a=0
print ("Eliminando itens abaixo do suporte mínimo (1-itemset)")
podaumitemset=[]
for line in umitemset:
    c = umitemset[a][1]
    #print (c)
    if c >= suporteminimo:
        itens.append(umitemset[a][0])
        podaumitemset.append(line)
    a+=1
#print (podaumitemset)
print ("Gravando 1-itemset+contagem no arquivo")
fileobj.write ("------------UMITEMSET-------------")
fileobj.write ('\n')
for line in podaumitemset:
    contagemtodositemset.append(line)
    fileobj.write (str(line))
    fileobj.write ('\n')
doisitemset = []
#---------------------------------------------------Início 2-itemset
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
f = open ("accidents.dat",'r')
contagemitemset = [[0 for coluna in range (0,2) ] for linha in range (len(doisitemset))]
for line in f:
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
print ("Eliminando itens abaixo do suporte mínimo (2-itemset)")
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
print ("Calculando Confiança")


#--- Calcular Confiança


geratabelaconfianca =[]
for line in range (len(podadoisitemset)):
    a = podadoisitemset [line][0]
    geratabelaconfianca.append (list (a))
tabelaconfianca = [[0 for coluna in range (0,4) ] for linha in range ((len(geratabelaconfianca))*2)]
# = [[0 for coluna in range (0,2) ] for linha in range (len(itens))]
b=0
for a in range (len (geratabelaconfianca)):
    tabelaconfianca[a][0]=geratabelaconfianca[a][0]
    tabelaconfianca[a][1]=geratabelaconfianca[a][1]
    tabelaconfianca[a][2]=podadoisitemset[a][1]
    for c in range (len(umitemset)):
        if umitemset[c][0] == tabelaconfianca[a][0]:
            tabelaconfianca[a][3]=podadoisitemset[a][1]/umitemset[c][1]
    b+=1
for a in range (len (geratabelaconfianca)):
    tabelaconfianca[b][0]=geratabelaconfianca[a][1]
    tabelaconfianca[b][1]=geratabelaconfianca[a][0]
    tabelaconfianca[b][2]=podadoisitemset[a][1]
    for c in range (len(umitemset)):
        if umitemset[c][0] == tabelaconfianca[b][0]:
            tabelaconfianca[b][3]=podadoisitemset[a][1]/umitemset[c][1]
    b+=1
tabelaconfiancafim=[]
for line in range (len(tabelaconfianca)):
    if tabelaconfianca[line][3] > confiancaminima:
        tabelaconfiancafim.append(tabelaconfianca[line])


print ("Gravando 2-itemset + Suporte + Confiança no arquivo")
fileobj.write ('----------------2 - ITEMSET----------------(Suporte)-')
fileobj.write ('\n')
for line in podadoisitemset:
    fileobj.write (str (line))
    fileobj.write("\n")
fileobj.write ('----------------2 - ITEMSET----------------(Confiança)-')
fileobj.write ('\n')
for line in range (len (tabelaconfiancafim)):
    fileobj.write (' ' + str (tabelaconfiancafim[line][0])+ ' => ' + str (tabelaconfiancafim[line][1])+ ' (sup = ' + str (tabelaconfiancafim[line][2]) +'),(conf = ' + str (tabelaconfiancafim[line][3])+')')
    fileobj.write("\n")

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
        interseccao = set.issubset( line, linha)
        if len (line) == 3:
            tresitemset.append (line)

print ("Pronto")
print ("Percorrendo banco e contando (3-itemset)")

f = open ("accidents.dat",'r')
contagemitemset = [[0 for coluna in range (0,2) ] for linha in range (len(tresitemset))]
for line in f:
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
print ("Eliminando itens abaixo do suporte mínimo (3-itemset)")
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

print ("Calculando Confiança")


#-------------------------------------------------- Calcular Confiança

geratabelaconfianca =[]
for line in range (len(podaitemset)):
    a = podaitemset [line][0]
    geratabelaconfianca.append (list (a))
#print (geratabelaconfianca)
tabelaconfianca = [[0 for coluna in range (0,5) ] for linha in range ((len(geratabelaconfianca))*3)]
# = [[0 for coluna in range (0,2) ] for linha in range (len(itens))]
b=0
for a in range (len (geratabelaconfianca)):
    tabelaconfianca[a][0]=geratabelaconfianca[a][0]
    tabelaconfianca[a][1]=geratabelaconfianca[a][1]
    tabelaconfianca[a][2]=geratabelaconfianca[a][2]
    tabelaconfianca[a][3]=podaitemset[a][1]
    for c in range (len(umitemset)):
        if umitemset[c][0] == tabelaconfianca[a][2]:
            tabelaconfianca[a][4]=tabelaconfianca[a][3]/umitemset[c][1]
    b+=1
for a in range (len (geratabelaconfianca)):
    tabelaconfianca[b][0]=geratabelaconfianca[a][0]
    tabelaconfianca[b][1]=geratabelaconfianca[a][2]
    tabelaconfianca[b][2]=geratabelaconfianca[a][1]
    tabelaconfianca[b][3]=podaitemset[a][1]
    for c in range (len(umitemset)):
        if umitemset[c][0] == tabelaconfianca[a][2]:
            tabelaconfianca[b][4]=tabelaconfianca[a][3]/umitemset[c][1]   
    b+=1
for a in range (len (geratabelaconfianca)):
    tabelaconfianca[b][0]=geratabelaconfianca[a][1]
    tabelaconfianca[b][1]=geratabelaconfianca[a][2]
    tabelaconfianca[b][2]=geratabelaconfianca[a][0]
    tabelaconfianca[b][3]=podaitemset[a][1]
    for c in range (len(umitemset)):
        if umitemset[c][0] == tabelaconfianca[a][2]:
            tabelaconfianca[b][4]=tabelaconfianca[a][3]/umitemset[c][1]   
    b+=1
tabelaconfiancafim =[]
for line in range (len(tabelaconfianca)):
    if tabelaconfianca[line][4] >= confiancaminima:
        tabelaconfiancafim.append(tabelaconfianca[line])
tabelaconfiancainverso =  [[0 for coluna in range (0,5) ] for linha in range ((len(geratabelaconfianca))*3)]
b=0
for a in range (len(tabelaconfianca)):
    tabelaconfiancainverso[a][0] = tabelaconfianca [a][2]
    tabelaconfiancainverso[a][1] = tabelaconfianca [a][1]
    tabelaconfiancainverso[a][2] = tabelaconfianca [a][0]
    tabelaconfiancainverso[a][3] = tabelaconfianca [a][3]
    for c in range (len(podadoisitemset)):
        if tabelaconfiancainverso[a][1] in podadoisitemset[c][0] and tabelaconfiancainverso [a][2] in podadoisitemset[c][0]:
            tabelaconfiancainverso[a][4] = tabelaconfiancainverso[a][3]/podadoisitemset [c][1]
tabelaconfiancainversofim=[]
for line in range (len(tabelaconfiancainverso)):
    if tabelaconfiancainverso[line][4] >= confiancaminima:
        tabelaconfiancainversofim.append(tabelaconfiancainverso[line])

#---------------------- Fim do calculo de confiança
print ("Gravando 3-itemset + Suporte + Confiança no arquivo")
fileobj.write ('----------------3 - ITEMSET----------------(Suporte)-')
fileobj.write ('\n')
for line in podaitemset:
    fileobj.write (str (line))
    fileobj.write("\n")
fileobj.write ('----------------3 - ITEMSET----------------(Confiança)-')
fileobj.write ('\n')
for line in range (len(tabelaconfiancafim)):
    fileobj.write (' ' + str (tabelaconfiancafim[line][0])+ ' , ' + str (tabelaconfiancafim[line][1])+ '  => '+str (tabelaconfiancafim[line][2])+' (sup = ' + str (tabelaconfiancafim[line][3]) +'),(conf = ' + str (tabelaconfiancafim[line][4])+')')
    fileobj.write("\n")
for line in range (len(tabelaconfiancainversofim)):
    fileobj.write (' ' + str (tabelaconfiancainversofim[line][0])+ ' => ' + str (tabelaconfiancainversofim[line][1])+ ' , ' +str (tabelaconfiancainversofim[line][2])+' (sup = ' + str (tabelaconfiancainversofim[line][3]) +'),(conf = ' + str (tabelaconfiancainversofim[line][4])+')')
    fileobj.write("\n")
#----------------------------------------------------------Termino 3-itemset

numeroitemset = 3
repete = 1
continua = True
while repete==1:
    itemsetanterior = podaitemset
    numeroitemset+=1
    geraitemsets (itemsetanterior,numeroitemset,contagemtodositemset,confiancaminima)
    if continua == True:
        continua = False
    else:
        repete = 0

tempodeexecucao=clock()-t1
fileobj.write(str(tempodeexecucao))
fileobj.close()
#----------------------------------------------------------Termino 2-itemset


print ("\n")
print ("-----------------------PROGRAMA FINALIZADO-------------------")
print ("-----------------------Os resultados estão em:  Apriori Fim - Suporte + Confianca em %.txt -------------------")

#geratresitemset = [list(x) for x in itertools.combinations(range(1,469), 3)]
#geraquatroitemset = [list(x) for x in itertools.combinations(range(1,469), 4)]




print ("Pressione Enter para Sair")
a = input()
