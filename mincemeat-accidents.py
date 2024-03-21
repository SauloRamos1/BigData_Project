#!/usr/bin/env python


################################################################################
# Copyright (c) 2010 Michael Fairley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

import asynchat
import asyncore
import cPickle as pickle
import hashlib
import hmac
import logging
import marshal
import optparse
import os
import random
import socket
import sys
import types
import itertools
from time import clock
t1 = clock ()
VERSION = "0.1.2"
print ("PROJETO Regras de Associacao (BigData)- Saulo Ramos - UFABC -Engenharia da Informacao")
print ("\n")
print ("\n")
print ("O  valor do suporte minimo eh de 80% e Confianca 80%")
global suporteminimo
suporteminimo = 340183/1.25
confiancaminima = 0.8
print ("\n")
print ("Digite o numero de partes em que deseja dividir o banco de dados")
global numerodepartes
numerodepartes = int (input())
suporteminimo = suporteminimo/numerodepartes
global contagemtodositemset
contagemtodositemset = []
global itemsetfim
itemsetfim = []

DEFAULT_PORT = 11235

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

class Protocol(asynchat.async_chat):
    def __init__(self, conn=None):
        if conn:
            asynchat.async_chat.__init__(self, conn)
        else:
            asynchat.async_chat.__init__(self)

        self.set_terminator("\n")
        self.buffer = []
        self.auth = None
        self.mid_command = False

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def send_command(self, command, data=None):
        if not ":" in command:
            command += ":"
        if data:
            pdata = pickle.dumps(data)
            command += str(len(pdata))
            logging.debug( "<- %s" % command)
            self.push(command + "\n" + pdata)
        else:
            logging.debug( "<- %s" % command)
            self.push(command + "\n")

    def found_terminator(self):
        if not self.auth == "Done":
            command, data = (''.join(self.buffer).split(":",1))
            self.process_unauthed_command(command, data)
        elif not self.mid_command:
            logging.debug("-> %s" % ''.join(self.buffer))
            command, length = (''.join(self.buffer)).split(":", 1)
            if command == "challenge":
                self.process_command(command, length)
            elif length:
                self.set_terminator(int(length))
                self.mid_command = command
            else:
                self.process_command(command)
        else: # Read the data segment from the previous command
            if not self.auth == "Done":
                logging.fatal("Recieved pickled data from unauthed source")
                sys.exit(1)
            data = pickle.loads(''.join(self.buffer))
            self.set_terminator("\n")
            command = self.mid_command
            self.mid_command = None
            self.process_command(command, data)
        self.buffer = []

    def send_challenge(self):
        self.auth = os.urandom(20).encode("hex")
        self.send_command(":".join(["challenge", self.auth]))

    def respond_to_challenge(self, command, data):
        mac = hmac.new(self.password, data, hashlib.sha1)
        self.send_command(":".join(["auth", mac.digest().encode("hex")]))
        self.post_auth_init()

    def verify_auth(self, command, data):
        mac = hmac.new(self.password, self.auth, hashlib.sha1)
        if data == mac.digest().encode("hex"):
            self.auth = "Done"
            logging.info("Authenticated other end")
        else:
            self.handle_close()

    def process_command(self, command, data=None):
        commands = {
            'challenge': self.respond_to_challenge,
            'disconnect': lambda x, y: self.handle_close(),
            }

        if command in commands:
            commands[command](command, data)
        else:
            logging.critical("Unknown command received: %s" % (command,)) 
            self.handle_close()

    def process_unauthed_command(self, command, data=None):
        commands = {
            'challenge': self.respond_to_challenge,
            'auth': self.verify_auth,
            'disconnect': lambda x, y: self.handle_close(),
            }

        if command in commands:
            commands[command](command, data)
        else:
            logging.critical("Unknown unauthed command received: %s" % (command,)) 
            self.handle_close()
        

class Client(Protocol):
    def __init__(self):
        Protocol.__init__(self)
        self.mapfn = self.reducefn = self.collectfn = None
        
    def conn(self, server, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((server, port))
        asyncore.loop()

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def set_mapfn(self, command, mapfn):
        self.mapfn = types.FunctionType(marshal.loads(mapfn), globals(), 'mapfn')

    def set_collectfn(self, command, collectfn):
        self.collectfn = types.FunctionType(marshal.loads(collectfn), globals(), 'collectfn')

    def set_reducefn(self, command, reducefn):
        self.reducefn = types.FunctionType(marshal.loads(reducefn), globals(), 'reducefn')

    def call_mapfn(self, command, data):
        logging.info("Mapping %s" % str(data[0]))
        results = {}
        for k, v in self.mapfn(data[0], data[1]):
            if k not in results:
                results[k] = []
            results[k].append(v)
        if self.collectfn:
            for k in results:
                results[k] = [self.collectfn(k, results[k])]
        self.send_command('mapdone', (data[0], results))

    def call_reducefn(self, command, data):
        logging.info("Reducing %s" % str(data[0]))
        results = self.reducefn(data[0], data[1])
        self.send_command('reducedone', (data[0], results))
        
    def process_command(self, command, data=None):
        commands = {
            'mapfn': self.set_mapfn,
            'collectfn': self.set_collectfn,
            'reducefn': self.set_reducefn,
            'map': self.call_mapfn,
            'reduce': self.call_reducefn,
            }

        if command in commands:
            commands[command](command, data)
        else:
            Protocol.process_command(self, command, data)

    def post_auth_init(self):
        if not self.auth:
            self.send_challenge()


class Server(asyncore.dispatcher, object):

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.mapfn = None
        self.reducefn = None
        self.collectfn = None
        self.datasource = None
        self.password = None

    def run_server(self, password="", port=DEFAULT_PORT):
        self.password = password
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", port))
        self.listen(1)
        try:
            asyncore.loop()
        except:
            self.close_all()
            raise
        
        return self.taskmanager.results

    def handle_accept(self):
        conn, addr = self.accept()
        sc = ServerChannel(conn, self)
        sc.password = self.password

    def handle_close(self):
        self.close()

    def set_datasource(self, ds):
        self._datasource = ds
        self.taskmanager = TaskManager(self._datasource, self)
    
    def get_datasource(self):
        return self._datasource

    datasource = property(get_datasource, set_datasource)


class ServerChannel(Protocol):
    def __init__(self, conn, server):
        Protocol.__init__(self, conn)
        self.server = server

        self.start_auth()

    def handle_close(self):
        logging.info("Client disconnected")
        self.close()

    def start_auth(self):
        self.send_challenge()

    def start_new_task(self):
        command, data = self.server.taskmanager.next_task(self)
        if command == None:
            return
        self.send_command(command, data)

    def map_done(self, command, data):
        self.server.taskmanager.map_done(data)
        self.start_new_task()

    def reduce_done(self, command, data):
        self.server.taskmanager.reduce_done(data)
        self.start_new_task()

    def process_command(self, command, data=None):
        commands = {
            'mapdone': self.map_done,
            'reducedone': self.reduce_done,
            }

        if command in commands:
            commands[command](command, data)
        else:
            Protocol.process_command(self, command, data)

    def post_auth_init(self):
        if self.server.mapfn:
            self.send_command('mapfn', marshal.dumps(self.server.mapfn.func_code))
        if self.server.reducefn:
            self.send_command('reducefn', marshal.dumps(self.server.reducefn.func_code))
        if self.server.collectfn:
            self.send_command('collectfn', marshal.dumps(self.server.collectfn.func_code))
        self.start_new_task()
    
class TaskManager:
    START = 0
    MAPPING = 1
    REDUCING = 2
    FINISHED = 3

    def __init__(self, datasource, server):
        self.datasource = datasource
        self.server = server
        self.state = TaskManager.START
        self.results = open('reduceresults.txt', 'w')

    def next_task(self, channel):
        if self.state == TaskManager.START:
            self.map_iter = self.datasource #iter(self.datasource)
            self.working_maps = {}
            self.map_results = {}
            #self.waiting_for_maps = []
            self.state = TaskManager.MAPPING
        if self.state == TaskManager.MAPPING:
            try:
                #map_key = self.map_iter.next()
                
                #map_item = map_key, self.datasource[map_key]
                map_item = self.map_iter.next()
                self.working_maps[map_item[0]] = map_item[1]
                return ('map', map_item)
            except StopIteration:
                if len(self.working_maps) > 0:
                    key = random.choice(self.working_maps.keys())
                    return ('map', (key, self.working_maps[key]))
                self.state = TaskManager.REDUCING
                self.reduce_iter = self.map_results.iteritems()
                self.working_reduces = {}
                #self.results = {}
        if self.state == TaskManager.REDUCING:
            try:
                reduce_item = self.reduce_iter.next()
                self.working_reduces[reduce_item[0]] = reduce_item[1]
                return ('reduce', reduce_item)
            except StopIteration:
                if len(self.working_reduces) > 0:
                    key = random.choice(self.working_reduces.keys())
                    return ('reduce', (key, self.working_reduces[key]))
                self.state = TaskManager.FINISHED
        if self.state == TaskManager.FINISHED:
            self.server.handle_close()
            return ('disconnect', None)
    
    def map_done(self, data):
        # Don't use the results if they've already been counted
        if not data[0] in self.working_maps:
            return

        for (key, values) in data[1].iteritems():
            if key not in self.map_results:
                self.map_results[key] = []
            self.map_results[key].extend(values)
        del self.working_maps[data[0]]
                                
    def reduce_done(self, data):
        # Don't use the results if they've already been counted
        if not data[0] in self.working_reduces:
            return

        #self.results[data[0]] = data[1]
        self.results.write(str(data[0])+'\n'+str(data[1])+'\n')
        tempodeexecucao = clock() - t1
        fileobj = open ("tempodeexecucao.txt",'w')
        fileobj.write(str (tempodeexecucao))
        fileobj.close()
        del self.working_reduces[data[0]]

def run_client():
    parser = optparse.OptionParser(usage="%prog [options]", version="%%prog %s"%VERSION)
    parser.add_option("-p", "--password", dest="password", default="", help="password")
    parser.add_option("-P", "--port", dest="port", type="int", default=DEFAULT_PORT, help="port")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true")
    parser.add_option("-V", "--loud", dest="loud", action="store_true")

    (options, args) = parser.parse_args()
                      
    if options.verbose:
        logging.basicConfig(level=logging.INFO)
    if options.loud:
        logging.basicConfig(level=logging.DEBUG)

    client = Client()
    client.password = options.password
    client.conn(args[0], options.port)
                      

if __name__ == '__main__':
    run_client()
