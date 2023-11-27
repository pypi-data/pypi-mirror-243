from pycurrencyid.mata_uang import mataUang
import pprint


data = mataUang()

if __name__=="__main__":    
    pprint.pprint(data.semua, sort_dicts=False)
    print()
    pprint.pprint(data.cari("idr"), sort_dicts=False)
    print()
    print(len(data.semua))
