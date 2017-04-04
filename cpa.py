import struct
from binascii import hexlify, unhexlify


sboxes = [
   [0x01010400, 0x00000000, 0x00010000, 0x01010404,
    0x01010004, 0x00010404, 0x00000004, 0x00010000,
    0x00000400, 0x01010400, 0x01010404, 0x00000400,
    0x01000404, 0x01010004, 0x01000000, 0x00000004,
    0x00000404, 0x01000400, 0x01000400, 0x00010400,
    0x00010400, 0x01010000, 0x01010000, 0x01000404,
    0x00010004, 0x01000004, 0x01000004, 0x00010004,
    0x00000000, 0x00000404, 0x00010404, 0x01000000,
    0x00010000, 0x01010404, 0x00000004, 0x01010000,
    0x01010400, 0x01000000, 0x01000000, 0x00000400,
    0x01010004, 0x00010000, 0x00010400, 0x01000004,
    0x00000400, 0x00000004, 0x01000404, 0x00010404,
    0x01010404, 0x00010004, 0x01010000, 0x01000404,
    0x01000004, 0x00000404, 0x00010404, 0x01010400,
    0x00000404, 0x01000400, 0x01000400, 0x00000000,
    0x00010004, 0x00010400, 0x00000000, 0x01010004],

   [0x80108020, 0x80008000, 0x00008000, 0x00108020,
    0x00100000, 0x00000020, 0x80100020, 0x80008020,
    0x80000020, 0x80108020, 0x80108000, 0x80000000,
    0x80008000, 0x00100000, 0x00000020, 0x80100020,
    0x00108000, 0x00100020, 0x80008020, 0x00000000,
    0x80000000, 0x00008000, 0x00108020, 0x80100000,
    0x00100020, 0x80000020, 0x00000000, 0x00108000,
    0x00008020, 0x80108000, 0x80100000, 0x00008020,
    0x00000000, 0x00108020, 0x80100020, 0x00100000,
    0x80008020, 0x80100000, 0x80108000, 0x00008000,
    0x80100000, 0x80008000, 0x00000020, 0x80108020,
    0x00108020, 0x00000020, 0x00008000, 0x80000000,
    0x00008020, 0x80108000, 0x00100000, 0x80000020,
    0x00100020, 0x80008020, 0x80000020, 0x00100020,
    0x00108000, 0x00000000, 0x80008000, 0x00008020,
    0x80000000, 0x80100020, 0x80108020, 0x00108000],

   [0x00000208, 0x08020200, 0x00000000, 0x08020008,
    0x08000200, 0x00000000, 0x00020208, 0x08000200,
    0x00020008, 0x08000008, 0x08000008, 0x00020000,
    0x08020208, 0x00020008, 0x08020000, 0x00000208,
    0x08000000, 0x00000008, 0x08020200, 0x00000200,
    0x00020200, 0x08020000, 0x08020008, 0x00020208,
    0x08000208, 0x00020200, 0x00020000, 0x08000208,
    0x00000008, 0x08020208, 0x00000200, 0x08000000,
    0x08020200, 0x08000000, 0x00020008, 0x00000208,
    0x00020000, 0x08020200, 0x08000200, 0x00000000,
    0x00000200, 0x00020008, 0x08020208, 0x08000200,
    0x08000008, 0x00000200, 0x00000000, 0x08020008,
    0x08000208, 0x00020000, 0x08000000, 0x08020208,
    0x00000008, 0x00020208, 0x00020200, 0x08000008,
    0x08020000, 0x08000208, 0x00000208, 0x08020000,
    0x00020208, 0x00000008, 0x08020008, 0x00020200],

   [0x00802001, 0x00002081, 0x00002081, 0x00000080,
    0x00802080, 0x00800081, 0x00800001, 0x00002001,
    0x00000000, 0x00802000, 0x00802000, 0x00802081,
    0x00000081, 0x00000000, 0x00800080, 0x00800001,
    0x00000001, 0x00002000, 0x00800000, 0x00802001,
    0x00000080, 0x00800000, 0x00002001, 0x00002080,
    0x00800081, 0x00000001, 0x00002080, 0x00800080,
    0x00002000, 0x00802080, 0x00802081, 0x00000081,
    0x00800080, 0x00800001, 0x00802000, 0x00802081,
    0x00000081, 0x00000000, 0x00000000, 0x00802000,
    0x00002080, 0x00800080, 0x00800081, 0x00000001,
    0x00802001, 0x00002081, 0x00002081, 0x00000080,
    0x00802081, 0x00000081, 0x00000001, 0x00002000,
    0x00800001, 0x00002001, 0x00802080, 0x00800081,
    0x00002001, 0x00002080, 0x00800000, 0x00802001,
    0x00000080, 0x00800000, 0x00002000, 0x00802080],

   [0x00000100, 0x02080100, 0x02080000, 0x42000100,
    0x00080000, 0x00000100, 0x40000000, 0x02080000,
    0x40080100, 0x00080000, 0x02000100, 0x40080100,
    0x42000100, 0x42080000, 0x00080100, 0x40000000,
    0x02000000, 0x40080000, 0x40080000, 0x00000000,
    0x40000100, 0x42080100, 0x42080100, 0x02000100,
    0x42080000, 0x40000100, 0x00000000, 0x42000000,
    0x02080100, 0x02000000, 0x42000000, 0x00080100,
    0x00080000, 0x42000100, 0x00000100, 0x02000000,
    0x40000000, 0x02080000, 0x42000100, 0x40080100,
    0x02000100, 0x40000000, 0x42080000, 0x02080100,
    0x40080100, 0x00000100, 0x02000000, 0x42080000,
    0x42080100, 0x00080100, 0x42000000, 0x42080100,
    0x02080000, 0x00000000, 0x40080000, 0x42000000,
    0x00080100, 0x02000100, 0x40000100, 0x00080000,
    0x00000000, 0x40080000, 0x02080100, 0x40000100],

   [0x20000010, 0x20400000, 0x00004000, 0x20404010,
    0x20400000, 0x00000010, 0x20404010, 0x00400000,
    0x20004000, 0x00404010, 0x00400000, 0x20000010,
    0x00400010, 0x20004000, 0x20000000, 0x00004010,
    0x00000000, 0x00400010, 0x20004010, 0x00004000,
    0x00404000, 0x20004010, 0x00000010, 0x20400010,
    0x20400010, 0x00000000, 0x00404010, 0x20404000,
    0x00004010, 0x00404000, 0x20404000, 0x20000000,
    0x20004000, 0x00000010, 0x20400010, 0x00404000,
    0x20404010, 0x00400000, 0x00004010, 0x20000010,
    0x00400000, 0x20004000, 0x20000000, 0x00004010,
    0x20000010, 0x20404010, 0x00404000, 0x20400000,
    0x00404010, 0x20404000, 0x00000000, 0x20400010,
    0x00000010, 0x00004000, 0x20400000, 0x00404010,
    0x00004000, 0x00400010, 0x20004010, 0x00000000,
    0x20404000, 0x20000000, 0x00400010, 0x20004010],

   [0x00200000, 0x04200002, 0x04000802, 0x00000000,
    0x00000800, 0x04000802, 0x00200802, 0x04200800,
    0x04200802, 0x00200000, 0x00000000, 0x04000002,
    0x00000002, 0x04000000, 0x04200002, 0x00000802,
    0x04000800, 0x00200802, 0x00200002, 0x04000800,
    0x04000002, 0x04200000, 0x04200800, 0x00200002,
    0x04200000, 0x00000800, 0x00000802, 0x04200802,
    0x00200800, 0x00000002, 0x04000000, 0x00200800,
    0x04000000, 0x00200800, 0x00200000, 0x04000802,
    0x04000802, 0x04200002, 0x04200002, 0x00000002,
    0x00200002, 0x04000000, 0x04000800, 0x00200000,
    0x04200800, 0x00000802, 0x00200802, 0x04200800,
    0x00000802, 0x04000002, 0x04200802, 0x04200000,
    0x00200800, 0x00000000, 0x00000002, 0x04200802,
    0x00000000, 0x00200802, 0x04200000, 0x00000800,
    0x04000002, 0x04000800, 0x00000800, 0x00200002],

   [0x10001040, 0x00001000, 0x00040000, 0x10041040,
    0x10000000, 0x10001040, 0x00000040, 0x10000000,
    0x00040040, 0x10040000, 0x10041040, 0x00041000,
    0x10041000, 0x00041040, 0x00001000, 0x00000040,
    0x10040000, 0x10000040, 0x10001000, 0x00001040,
    0x00041000, 0x00040040, 0x10040040, 0x10041000,
    0x00001040, 0x00000000, 0x00000000, 0x10040040,
    0x10000040, 0x10001000, 0x00041040, 0x00040000,
    0x00041040, 0x00040000, 0x10041000, 0x00001000,
    0x00000040, 0x10040040, 0x00001000, 0x00041040,
    0x10001000, 0x00000040, 0x10000040, 0x10040000,
    0x10040040, 0x10000000, 0x00040000, 0x10001040,
    0x00000000, 0x10041040, 0x00040040, 0x10000040,
    0x10040000, 0x10001000, 0x10001040, 0x00000000,
    0x10041040, 0x00041000, 0x00041000, 0x00001040,
    0x00001040, 0x00040040, 0x10000000, 0x10041000],
]

initial_permutation = [
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16,  8, 0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6]

def des_ip(data):
    data = struct.unpack("<Q", data)[0]
    ret = 0x0
    for i in xrange(64):
        j = initial_permutation[i]
        ret |= (((data >> i) & 0x1) << j)

    return struct.pack("<Q", ret)

def hamming_weight(x):
    hw = 0
    while x:
        if x & 1:
            hw += 1
        x = x >> 1
    return hw

def des_test(plain, sbox):
    p = des_ip(plain)
    l = struct.unpack("<I", p[:4])[0]
    r = struct.unpack("<I", p[4:])[0]

    ll = ((l << 28) | (l >> 4)) & 0xffffffff

    if sbox == 0:
        x = (l  >> 24) & 0x3f
    if sbox == 1:
        x = (ll >> 24) & 0x3f
    if sbox == 2:
        x = (l  >> 16) & 0x3f
    if sbox == 3:
        x = (ll >> 16) & 0x3f
    if sbox == 4:
        x = (l  >>  8) & 0x3f
    if sbox == 5:
        x = (ll >>  8) & 0x3f
    if sbox == 6:
        x = (l       ) & 0x3f
    if sbox == 7:
        x = (ll      ) & 0x3f
    
    return hamming_weight(x)
    

def des_predict(plain, sbox, k):
    p = des_ip(plain)
    l = struct.unpack("<I", p[:4])[0]
    r = struct.unpack("<I", p[4:])[0]

    ll = ((l << 28) | (l >> 4)) & 0xffffffff

    if sbox == 0:
        x = sboxes[sbox][((l  >> 24) ^ k) & 0x3f]
    if sbox == 1:
        x = sboxes[sbox][((ll >> 24) ^ k) & 0x3f]
    if sbox == 2:
        x = sboxes[sbox][((l  >> 16) ^ k) & 0x3f]
    if sbox == 3:
        x = sboxes[sbox][((ll >> 16) ^ k) & 0x3f]
    if sbox == 4:
        x = sboxes[sbox][((l  >>  8) ^ k) & 0x3f]
    if sbox == 5:
        x = sboxes[sbox][((ll >>  8) ^ k) & 0x3f]
    if sbox == 6:
        x = sboxes[sbox][((l       ) ^ k) & 0x3f]
    if sbox == 7:
        x = sboxes[sbox][((ll      ) ^ k) & 0x3f]
    
    return hamming_weight(x)

from random import *
def des_rand_challenge(count):
    ret = []
    for i in xrange(count):
        with open("/dev/urandom", "rb") as f:
            ret += [hexlify(f.read(8))]
        
    #ret = []
    #for i in xrange(count):
    #    ret += [choice(["0000000000000000", "1111111111111111", "aaaaaaaaaaaaaaaa", "7777777777777777", "ffffffffffffffff"])]
    return ret
    
import os
import traceback
import sys

from config import config_get, config_reload, args
from capture import *
from random import choice, randrange

class cpa:
    def __init__(self):
        self.trend = []
        self.n = 0
        self.X  = None
        self.XX = None
        self.XY = []
        self.YY = []
        self.Y  = []

    def add(self, trace, prediction):
        if self.n == 0:
            self.n  = 1
            self.X  = trace
            self.XX = trace * trace
            for p in prediction:
                self.XY += [trace * p]
                self.YY += [p*p]
                self.Y  += [p]
                self.trend += [[]]
        else:
            self.n  += 1
            self.X  += trace
            self.XX += trace * trace
            for i in xrange(len(prediction)):
                p = prediction[i]
                self.XY[i] += trace*p
                self.YY[i] += p*p
                self.Y[i]  += p


    def cpa(self):
        ret = []
        #computing pearson correlation coefficient
        for i in xrange(len(self.XY)):
            Z = self.n*self.XY[i] - self.X*self.Y[i]
            N = np.sqrt(self.n*self.XX - self.X**2) * np.sqrt(self.n*self.YY[i] - self.Y[i]**2)
            ret += [Z/N]
            np.save("%s/cpa-%d" % ("/tmp", i), Z/N)

        return ret

    def update_trend(self):
        if self.n < 2:
            return

        res = self.cpa()
        for i in xrange(len(res)):
            self.trend[i] += [np.max(res[i])]

            #plot(res[i],
            #    blocking=False,
            #    title="CFPA run %d" % cpa.n,
            #    f0=cap.demod_frequency,
            #    samp_rate=cap.demod_samp_rate,
            #    fft_step=128,
            #    png="/tmp/cpa-%d.png" % i)

        plot(np.array(self.trend),
            title="CFPA Trend run %d" % cpa.n,
            blocking=False,
            png="/tmp/cpa-trend.png")

import glob
import os
def read_old_traces(path):
    files = glob.glob(path)
    shuffle(files)
    for fname in files[:10]:
        p,c,k = os.path.basename(fname).split("-")
        with open(fname, "rb") as f:
            data = f.read()
            trace = np.frombuffer(data, dtype=np.dtype('f4'))

        yield p, trace
        
            
if __name__ == "__main__":
    sbox = 0
    count = 30
    cpa = cpa()
    cap = capture()
    
    while True:
        for chal, trace in cap.capture(values=des_rand_challenge(count), count=count):
            trace = stft(trace, 512, 128)

            #compute prediction
            #prediction = []
            #for k in xrange(64):
            #    p = des_predict(unhexlify(chal), sbox, k)
            #    prediction += [p]
            #cpa.add(trace, prediction)
               
            #p = hamming_weight(struct.unpack("<Q", unhexlify(chal))[0])
            p = des_test(unhexlify(chal),0)
            cpa.add(trace, [p])
        #cpa.update_trend()

        plot(cpa.cpa()[0],
            blocking=False,
            title="CFPA run %d" % cpa.n,
            f0=cap.demod_frequency,
            samp_rate=cap.demod_samp_rate,
            fft_step=128,
            png="/tmp/cpa.png",)

