import sys,math
from itertools import izip_longest, chain
from struct import pack

# 40 and 20 were chosen 
onda = [int(32000.0 * math.sin(float(k) / 20.0 * math.pi)) for k in range(40)]
onda_2 = [int(32000.0 * math.sin(float(k) / 11.0 * math.pi)) for k in range(22)]
onda_bytes = (bytearray(chain.from_iterable([pack("h",n) * 2 for n in onda])),
              bytearray(chain.from_iterable([pack("h",n) * 2 for n in onda_2])))
    
def cas_to_wav(arq, modo="wb"):
    return Cas2Wav(arq)
    
class Cas2Wav(object):
    def __init__(self, filename="cassette.wav"):
        self.__file = open(filename,"wb")
                
    def __enter__(self):
        # Header
        self.__file.write(bytearray("RIFF") + bytearray([0]*4) + bytearray("WAVE"))
        self.__file.write(bytearray("fmt ") + bytearray([16,0,0,0,1,0,2,0, 0x44,0xAC,0,0,0x10,0xB1,0x02,0,4,0,16,0]))
        self.__file.write(bytearray("data") + bytearray([0]*4))
        self.__sc2s = 0
        return self
        
        
    def write(self, data):
        for b in bytearray(data):
            baite = b
            for _ in range(8):
                bloco = onda_bytes[baite & 1]
                self.__sc2s += len(bloco)
                self.__file.write(bloco)
                baite >>= 1
    
    def __exit__(self,type,val,tb):
        try:
            self.__file.seek(4)
            self.__file.write(bytearray(pack("I",self.__sc2s + 36)))
            self.__file.seek(40)
            self.__file.write(bytearray(pack("I",self.__sc2s)))
        finally:
            self.__file.close()

class Bloco(object):
    def __init__(self, tipo, dados):
        self.__tipo = tipo
        self.__tamanho = len(dados)
        self.__dados = dados
        
    def write(self, out):
        soma = self.__tipo + self.__tamanho
        for d in self.__dados:
            if d != None: soma += d
        soma = soma % 256
        out.write(bytearray([0x55,0x3C,self.__tipo,self.__tamanho]) + bytearray(self.__dados) + bytearray([soma,0x55]))
        

class BlocoArquivo(Bloco):
#   def __init__(self, tipo, nome, ascii = False, staddr = 0x1F0B, ldaddr = 0x1F0B):
    def __init__(self, tipo, nome, ascii = False, staddr = 0x3000, ldaddr = 0x3000):
        Bloco.__init__(self, 0, bytearray(nome.upper()[:8] + " " * (max(0, 8-len(nome)))) + bytearray([tipo, {False: 0, True: 0xFF}[ascii], 0]) + bytearray(pack(">H",staddr)) + bytearray(pack(">H",ldaddr))) 

class BlocoEOF(Bloco):
    def __init__(self):
        Bloco.__init__(self, 0xFF, []) 


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)        


if __name__ == "__main__":
    if sys.argv[1] == "-w":
        nome = sys.argv[2]
        fn = cas_to_wav
        saida = nome.replace(".rom",".wav")
    else:
        nome = sys.argv[1]
        fn = open
        saida = nome.replace(".rom",".cas")      
        
    nf = nome.replace(".rom","")
    with open(nome,"r") as arq:
        dados = bytearray(arq.read())
    print len(dados)    
    leader = bytearray("U" * 128)
    q = len(dados) // 255
    u  = len(dados) % 255
    print q,u
    with fn(saida,"wb") as s:    
        s.write(leader)
        BlocoArquivo(2,nf).write(s)
        s.write(leader)
        a = 0
        for b in grouper(255, dados):        
            a = a + 1
            if a == q: b = b[:u]
            Bloco(1, b).write(s)
            if a == q: break
        BlocoEOF().write(s)

    
