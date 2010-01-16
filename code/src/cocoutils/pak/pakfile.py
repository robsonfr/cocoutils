'''
Created on 16/01/2010
The PAK's header
@author: Robson
'''

from struct import *; 


class PAKHeader:
    
    __hdr="<HH"
    
    def __init__(self, filen = None):
        if filen != None:   
            self.loadfile(filen)
    
    def build(self, baseAddress, data, extra):
        self.length = len(data)
        self.baseAddress = baseAddress
        self.data = data
        self.extra = extra
    
    def load(self, data):
        tam=calcsize(PAKHeader.__hdr)
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
        
    def savefile(self, outfile):
        arq2=open(outfile,"wb")
        dt=pack(PAKHeader.__hdr, self.length, self.baseAddress)
        arq2.write(dt)
        arq2.write(self.data)
        arq2.write(self.extra)
        arq2.close()
    