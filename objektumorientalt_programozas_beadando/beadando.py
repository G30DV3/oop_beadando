from abc import ABC, abstractmethod
from datetime import datetime
import time


class Szoba(ABC):
    @abstractmethod
    def __init__(self, szobaszam):
        self.szobaszam = szobaszam
        self.ar = 8000

    @abstractmethod
    def osszkoltseg(self):
        pass


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, emelet, zuhanyvkad, wifi=False):
        super().__init__(szobaszam)
        self.emelet = emelet
        self.zuhanyvkad = zuhanyvkad
        self.wifi = wifi

    def osszkoltseg(self):
        extra_ar = self.ar + self.emelet * 500
        if self.wifi:
            extra_ar += 1500
        return extra_ar


class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, emelet, konyha, erkely):
        super().__init__(szobaszam)
        self.emelet = emelet
        self.konyha = konyha
        self.terasz = erkely

    def osszkoltseg(self):
        extra_ar = self.ar + self.emelet * 1000
        if self.konyha:
            extra_ar += 2000
        if self.terasz:
            extra_ar += 2500
        return extra_ar


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba.osszkoltseg()
        return None


class Foglalas:
    def __init__(self, szoba, honap, nap):
        self.szoba = szoba
        self.honap = honap
        self.nap = nap
        self.foglalva = []

    def foglalas_lemondasa(self, szalloda):
        szalloda.szobak.remove(self)
        print("Foglalás sikeresen lemondva.")


def a_valasz():
    szobaszam = int(input("Kérem adja meg a szoba számát: "))
    foglalhato_szoba = None
    for szoba in szalloda.szobak:
        if isinstance(szoba, Szoba) and szoba.szobaszam == szobaszam:
            foglalhato_szoba = szoba
            break

    if foglalhato_szoba is not None:
        osszkoltseg = szalloda.foglalas(szobaszam)
        if osszkoltseg is not None:
            print("A szoba ára:", osszkoltseg)
            megerosites = input("Biztosan lefoglalja? (igen/nem): ")
            if megerosites.lower() == "igen":
                honap = int(input("Kérem adja meg a foglalás hónapját: "))
                nap = int(input("Kérem adja meg a foglalás napját: "))
                mai_datum = datetime.now().date()
                foglalas_datum = datetime(datetime.now().year, honap, nap).date()

                if foglalas_datum >= mai_datum:
                    foglalas = Foglalas(foglalhato_szoba, honap, nap)
                    szalloda.szoba_hozzaadasa(foglalas)
                    print("Szoba lefoglalva!\n")
                else:
                    print("A megadott dátum korábbi, mint a mai dátum. Foglalás sikertelen.\n")
            else:
                print("Foglalás megszakítva.\n")
        else:
            print("A megadott szoba már foglalt.\n")
    else:
        print("Nincs ilyen szoba a szállodában.\n")


def b_valasz():
    szobaszam = int(input("Kérem adja meg a lemondani kívánt szoba számát: "))
    honap = int(input("Kérem adja meg a foglalás hónapját: "))
    nap = int(input("Kérem adja meg a foglalás napját: "))
    for foglalas in szalloda.szobak:
        if isinstance(foglalas,
                      Foglalas) and foglalas.szoba.szobaszam == szobaszam and foglalas.honap == honap and foglalas.nap == nap:
            foglalas.foglalas_lemondasa(szalloda)
            break
    else:
        print("Nem található ilyen foglalás.\n")


def c_valasz():
    print("Lefoglalt szobák:")
    for foglalas in szalloda.szobak:
        if isinstance(foglalas, Foglalas):
            print(f"Szoba: {foglalas.szoba.szobaszam}, Dátum: {foglalas.honap}.{foglalas.nap}")
    print()


szalloda = Szalloda("Torony Pihenő")
szalloda.szoba_hozzaadasa(EgyagyasSzoba(101, 1, "Kád", True))
szalloda.szoba_hozzaadasa(KetagyasSzoba(201, 2, True, False))
szalloda.szoba_hozzaadasa(KetagyasSzoba(301, 3, True, True))

foglalasok_datumai = {
    101: [(5, 30), (6, 27)],
    201: [(9, 23)],
    301: [(8, 1), (8, 15)]
}

for szoba in szalloda.szobak:
    if isinstance(szoba, Szoba):
        for szobaszam, foglalas_datumok in foglalasok_datumai.items():
            if szoba.szobaszam == szobaszam:
                for honap, nap in foglalas_datumok:
                    foglalas = Foglalas(szoba, honap, nap)
                    szalloda.szoba_hozzaadasa(foglalas)


# --------------------------------------A program fő része--------------------------------------

print("Üdvözöljük a ", szalloda.nev, " szállodában!")

valasz = ""

while valasz != "Kész":
    valasz = input("Mit szeretne tenni?\nSzobát foglalni (a)\nLemondani egy foglalást (b)\nListázni a lefoglalt szobákat (c)\n")
    if valasz == "a":
        a_valasz()
    elif valasz == "b":
        b_valasz()
    elif valasz == "c":
        c_valasz()
    elif valasz == "Kész":
        break
    time.sleep(1.5)
    print('Ha végzett Írja be a "Kész" szót!\n')
    time.sleep(2)
