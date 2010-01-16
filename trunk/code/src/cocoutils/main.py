'''
Created on 15/01/2010

@author: Robson
'''

from cocoutils.pak.pakfile import * 

if __name__ == '__main__':
    pakf = PAKHeader("d:/king.pak")
    print "%X %X" % (pakf.length, pakf.baseAddress)
    pakf.savefile("d:/k2.pak")
    pak2 = PAKHeader()
    pak2.build(0x4CFF,"AAAAA","BBBBB")
    pak2.savefile("d:/k3.pak")
    
    