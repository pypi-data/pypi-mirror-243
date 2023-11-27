from typing import Dict, List
import os.path as jalur
import json


# buat jalur baru berdasarkan berkas saat ini 
def jalur_berkas(nama: str) -> str:
    objek = jalur.abspath(__file__)
    utama = jalur.dirname(objek)
    return jalur.join(utama, "{}.json".format(nama))

class DataSelatan:
    def __init__(self):
        with open(jalur_berkas('amerika_selatan')) as data:
            self.data_json: Dict[str, str] = json.load(data)
        self.data_indeks: List[str] = [k for data in range(len(self.data_json)) for k in self.data_json[data].keys()]

    def huruf(self, abjat: str) -> List[Dict[str, str]]:
        besar = abjat.upper()
        indeks = self.data_indeks.index(besar)
        return self.data_json[indeks][besar]

class BidangSelatan:
    def __init__(self, huruf: str):
        data = DataSelatan().huruf(huruf)
        self.negara: List[str] = [data[i]["Negara"] for i in range(len(data))]
        self.iso4217: List[str] = [data[i]["ISO"] for i in range(len(data))]

class AmerikaSelatan:
    def __init__(self):
        indeks = DataSelatan().data_indeks
        self.negara : List[str]= tuple([negara for j in indeks for negara in BidangSelatan(j).negara])
        self.iso4217: List[str] = tuple([iso for j in indeks for iso in BidangSelatan(j).iso4217])

    def huruf(self, abjat: str) -> List[Dict[str, str]]:
        return DataSelatan().huruf(abjat)


