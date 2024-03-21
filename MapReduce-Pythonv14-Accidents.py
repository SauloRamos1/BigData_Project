#!/usr/bin/env python
# -*- coding: cp1252 -*-
import mincemeat
import glob
from itertools import *
import os
global contagemtodositemset
contagemtodositemset = []

"""def geraregras (conjunto,numeroitensconjunto):
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
        
    return (regras)"""



def datasource():
    f = open("accidents.dat",'r')
    numerodetransacoes=0
    for line in f:
        numerodetransacoes +=1
    transacaodedivisao = numerodetransacoes/numerodepartes
    parte = 0
    nt=0
    f = open("accidents.dat",'r')
    bloco=[]
    listablocos=[]
    for line in f:
        nt+=1
        if numerodetransacoes==nt:
            bloco.append (line)
            listablocos.append(bloco)
            bloco = []
        else:
            if len(bloco) < transacaodedivisao:
                bloco.append(line)
            else:        
                listablocos.append(bloco)
                bloco = []
                bloco.append (line)
    print ("Lista Blocos Criada")
    
    return (listablocos)            


#for line in ds:
#    for a in line:
#        print (a)

def mapfn(k, divisao):
    contagemtodositemset =[]
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
            if x != ("\n"):
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
    #f = open ("accidents.dat",'r')
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

    #f = open ("accidents.dat",'r')
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
    
    yield k, contagemtodositemset
def reducefn(k, contagemtodositemset):
    for line in contagemtodositemset:
        for x in line:
            itemsetfim.append (x)
    if k+1 != numerodepartes :
        podatabelaconfianca = []
    else:
        #-----------SEPARA ITENS
        print ("\n")
        print ("--------------- Soma, Poda e Calculo de Confianca para os itens-----------")
        print ("\n")
        separaitens = []

        for line in range (len(itemsetfim)):
            if type(itemsetfim[line][0]) == int:
                separaitens.append(itemsetfim[line])
        tamanhoconjunto = 0
        for line in range (len(itemsetfim)):
            if type (itemsetfim[line][0]) == set:
                if len (itemsetfim[line][0]) >tamanhoconjunto:
                    tamanhoconjunto = len(itemsetfim[line][0])
            
        for a in range (2,tamanhoconjunto+1):
            for line in range (len(itemsetfim)):
                if type (itemsetfim[line][0]) == set and len(itemsetfim[line][0]) == a:
                    separaitens.append (itemsetfim[line])
        #-----------------FIM SEPARA ITENS
        #-------ENXUGA MATRIZ
        enxugamatriz =[]
        for a in range (len(separaitens)):
            if separaitens[a][0] not in enxugamatriz:
                enxugamatriz.append (separaitens[a][0])
        global somageral
        somageral =  [[0 for coluna in range (0,2) ] for linha in range (len(enxugamatriz))]
        for line in range (len(enxugamatriz)):
            somageral[line][0] = enxugamatriz [line]
            for a in range (len(separaitens)):
                if separaitens[a][0] == somageral[line][0]:
                    somageral[line][1] += separaitens [a][1]

        global suporteminimo
        suporteminimo = 340183/1.25
        poda = []
        for line in range (len(somageral)):
            if somageral [line][1]>=suporteminimo:
                poda.append (somageral[line])
        #Regras itens sets
        geratabelaconfianca = []
        regrasfim=[]
        #print (poda)
        print ("Gerando Regras de Associacao")
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
        for b in regrasfim:
            for x in b:
                tabelaregras.append (x)
        #print (regrasfim)
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

        print ("Calculando Confianca ")
        for line in range (len(tabelaconfiancafim)):
            for linha in range (len(somageral)):
                if tabelaconfiancafim [line][0] == somageral[linha][0]:
                    tabelaconfiancafim[line][3] = float (tabelaconfiancafim[line][3])/float (somageral[linha][1])
        for numero in range (0,469):
            for line in range (len(tabelaconfiancafim)):
                for linha in range (len(somageral)):
                    if len (tabelaconfiancafim [line][0]) == 1 and numero in tabelaconfiancafim [line][0] :
                        #print (numero)
                        if numero == somageral[linha][0]:
                            tabelaconfiancafim[line][3] = float (tabelaconfiancafim[line][3])/float (somageral[linha][1])

        podatabelaconfianca = []
        print ("Eliminando itens abaixo da Confianca minima ")
        for line in range (len (tabelaconfiancafim)):
            if tabelaconfiancafim [line][3] >= confiancaminima:
                podatabelaconfianca.append (tabelaconfiancafim [line])
        test = open ("RESULTADOS.txt","w")
        for line in range (len(podatabelaconfianca)):
            test.write (' ' + str (podatabelaconfianca[line][0])+ ' => ' + str (podatabelaconfianca[line][1])+ ' , (sup = ' + str (podatabelaconfianca[line][2]) +'),(conf = ' + str (podatabelaconfianca[line][3])+')')
            test.write("\n")
        test.close()

            
              
    return (k, podatabelaconfianca)

print ("Digite o numero de partes em que deseja dividir o banco de dados")
global numerodepartes
numerodetransacoes = 0
f = open ("accidents.dat",'r')
for line in f:
    numerodetransacoes +=1
global suporteminimo
suporteminimo = numerodetransacoes/1.25
confiancaminima = 0.8
numerodepartes = int (input())

suporteminimo = suporteminimo/numerodepartes
global itemsetfim
itemsetfim = []
ds = enumerate(datasource())
s = mincemeat.Server()
s.datasource = ds
s.mapfn = mapfn
s.reducefn = reducefn



results = s.run_server(password="changeme")


results.close()
