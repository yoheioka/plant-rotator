import seeed_si114x
import time
import signal

def read_metric():
    SI1145 = seeed_si114x.grove_si114x()
    print('Visible %03d UV %.2f IR %03d' % (SI1145.ReadVisible , SI1145.ReadUV/100 , SI1145.ReadIR))

if __name__  == '__main__':
    read_metric()
