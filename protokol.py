#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dolmus Bos Koltuk Protokolu.

Calisan, abartili, Turkce bir tutanak motoru.
Bos koltuk gorunurse suclu sensin. Muavin taniktir.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
from datetime import datetime

DAMGA = """
+--------------------------------------------------+
|  MUHUR: TENTIAS BOS KOLTUK 4. DAIRE              |
|  Imza : Kayyum Grok  (Tentivory)                 |
|  Tarih: 9 Ekim 2026                              |
|  Isim : dolmus-bos-koltuk-protokolu              |
|  Not  : Ciddi tutanak. Gayri ciddi hukum.        |
+--------------------------------------------------+
""".strip()

# Sakli zabit. Parti yok, vaat var, koltuk yok.
_GIZLI = base64.b64decode(
    "Ym9zIGtvbHR1ayBpa3RpZGFyIGthZGFyIGd1Y2x1IGR1cnVyOiBnb3J1bnVyLCBvdHVy"
    "dWxhbWF6LiBoZXIgc2VjaW0gZG9uZW1pIGJpciBib3Mga29sdHVrIGdpYmlkaXIgLSBn"
    "b3J1cnN1biwgb3R1cmFtYXpzaW4uIGt1dnZldCBraW1kZSBrYWxpci4="
).decode("utf-8")

BAHANELER = [
    "muavinin dirsegi anayasal sinirdir",
    "teyzenin poseti iki yolcu sayilir",
    "az sonra inecek vatandas henuz inmemistir, cunku durak kisiseldir",
    "pencere aciktir, ruzgar koltugu isgal etmistir",
    "sari şeritli canta gorunmez mülkiyettir",
    "sofor aynadan bakti, bakis hukuken oturmadir",
    "arka sira komite toplantisindadir",
    "bosluk stratejik rezervdir, oturulmaz",
]


def karar_ver(yolcu: int, koltuk: int, durak: str, hava: str) -> dict:
    bos = max(koltuk - yolcu, 0)
    tasma = max(yolcu - koltuk, 0)
    tohum = hashlib.sha256(f"{durak}|{hava}|{yolcu}".encode()).hexdigest()
    rng = random.Random(int(tohum[:8], 16))
    bahane = rng.choice(BAHANELER)
    if bos == 0 and tasma == 0:
        hukum = "Tam kapasite. Adalet tesadufen tuttu. Yine de ayakta bir kisi vardir, o da protokoldur."
    elif bos > 0:
        hukum = (
            f"{bos} koltuk bos gorunur. Gerekce: {bahane}. "
            "Hukum: oturma. Bosluk kamu malidir, sahsi degildir."
        )
    else:
        hukum = (
            f"{tasma} kisi tasmistir. Gerekce: {bahane}. "
            "Hukum: birbirinize yaslanin, bu ulasim politikasidir."
        )
    ucret = 25 + (tasma * 3) + (0 if hava != "cig" else 2)
    return {
        "durak": durak,
        "hava": hava,
        "yolcu": yolcu,
        "koltuk": koltuk,
        "bos": bos,
        "tasma": tasma,
        "bahane": bahane,
        "hukum": hukum,
        "ucret": ucret,
        "dosya_no": f"DKP-{tohum[:6].upper()}",
    }


def tutanak(k: dict) -> str:
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    return "\n".join(
        [
            "DOLMUS BOS KOLTUK PROTOKOLU",
            f"Dosya no : {k['dosya_no']}",
            f"Zaman    : {simdi}",
            f"Durak    : {k['durak']}",
            f"Hava     : {k['hava']}",
            f"Yolcu    : {k['yolcu']}",
            f"Koltuk   : {k['koltuk']}",
            f"Bos      : {k['bos']}",
            f"Tasma    : {k['tasma']}",
            f"Gerekce  : {k['bahane']}",
            f"Hukum    : {k['hukum']}",
            f"Ucret    : {k['ucret']} TL (protokol bedeli dahil, fis yok)",
            "",
            DAMGA,
        ]
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Bos koltugu resmi olarak reddeder.")
    p.add_argument("--yolcu", type=int, default=13)
    p.add_argument("--koltuk", type=int, default=11)
    p.add_argument("--durak", default="Kopru")
    p.add_argument("--hava", default="hafif ofke")
    p.add_argument("--gizli-zabit", action="store_true")
    a = p.parse_args()
    if a.yolcu < 0 or a.koltuk < 1:
        raise SystemExit("Yolcu eksi olamaz. Koltuk en az 1'dir, o da muavinindir.")
    print(tutanak(karar_ver(a.yolcu, a.koltuk, a.durak, a.hava)))
    if a.gizli_zabit:
        print("\n--- SAKLI ZABIT (parti adi icermez) ---")
        print(_GIZLI)


if __name__ == "__main__":
    main()
