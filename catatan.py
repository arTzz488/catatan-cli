#!/usr/bin/env python3
"""Catatan CLI: aplikasi catatan sederhana di terminal."""
import argparse
import json
from datetime import datetime
from pathlib import Path

FILE = Path("catatan.json")


def muat():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    return []


def simpan(data):
    FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def tambah(teks):
    data = muat()
    data.append({"teks": teks, "waktu": datetime.now().strftime("%Y-%m-%d %H:%M")})
    simpan(data)
    print(f"Tersimpan (#{len(data)})")


def daftar():
    data = muat()
    if not data:
        print("Belum ada catatan.")
    for i, c in enumerate(data, 1):
        print(f"{i}. [{c['waktu']}] {c['teks']}")


def hapus(nomor):
    data = muat()
    if not 1 <= nomor <= len(data):
        print("Nomor tidak ditemukan.")
        return
    dihapus = data.pop(nomor - 1)
    simpan(data)
    print(f"Dihapus: {dihapus['teks']}")


def cari(kata):
    hasil = [c for c in muat() if kata.lower() in c["teks"].lower()]
    if not hasil:
        print("Tidak ada hasil.")
    for c in hasil:
        print(f"[{c['waktu']}] {c['teks']}")


def main():
    p = argparse.ArgumentParser(description="Catatan CLI")
    sub = p.add_subparsers(dest="perintah", required=True)

    a = sub.add_parser("tambah", help="tambah catatan")
    a.add_argument("teks")
    sub.add_parser("daftar", help="lihat semua catatan")
    h = sub.add_parser("hapus", help="hapus catatan by nomor")
    h.add_argument("nomor", type=int)
    c = sub.add_parser("cari", help="cari catatan")
    c.add_argument("kata")

    args = p.parse_args()
    if args.perintah == "tambah":
        tambah(args.teks)
    elif args.perintah == "daftar":
        daftar()
    elif args.perintah == "hapus":
        hapus(args.nomor)
    elif args.perintah == "cari":
        cari(args.kata)


if __name__ == "__main__":
    main()
