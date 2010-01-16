'''
Created on 16/01/2010
The PAK's header
@author: Robson
'''

from struct import *; 


class PAKHeader:
    
    __hdr="!HH"
    
    def __init__(self, filen):
        self.loadfile(filen)
    
    def load(self, data):
        tam=calcsize(PAKHeader.__header)
        dados=unpack(PAKHeader.__hdr, data[0:tam])
        self.length = dados[0]
        self.baseAddress = dados[1]
        self.data = data[tam:tam+self.length]
        self.extra = data[tam+self.length:]

    def loadfile(self, file):
        arq=open(file,"rb")
        dt=arq.read()
        self.load(dt)
        arq.close()
    