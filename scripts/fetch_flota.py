#!/usr/bin/env python3
"""
Renfe Cercanías Archiver — CSV edition
Descarga https://tiempo-real.renfe.com/renfe-visor/flota.json
y añade los datos al CSV diario en data/YYYY/MM/flota-YYYY-MM-DD.csv
Solo escribe filas nuevas si el contenido ha cambiado respecto a la captura anterior.
"""

import os
import csv
import json
import hashlib
import urllib.request
import datetime
import sys
import time

BASE_URL = "https://tiempo-real.renfe.com/renfe-visor/flota.json"

COLUMNAS = [
    "timestamp_utc",
    "tripId",
    "codTren",
    "codLinea",
    "retrasoMin",
    "codEstAct",
    "codEstSig",
    "horaLlegadaSigEst",
    "codEstDest",
    "codEstOrig",
    "porAvanc",
    "latitud",
    "longitud",
    "nucleo",
    "accesible",
    "via",
    "nextVia",
]


def get_url() -> str:
    ts = int(time.time() * 1000)
    return f"{BASE_URL}?v={ts}"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch() -> bytes:
    req = urllib.request.Request(
        get_url(),
        headers={
            "User-Agent": "renfe-cercanias-archiver/1.0",
            "Referer": "https://tiempo-real.renfe.com/",
            "Accept": "application/json, */*",
        },
        method="GET",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"HTTP {resp.status}")
                return resp.read()
        except Exception as e:
            if attempt == 2:
                print(f"ERROR tras 3 intentos: {e}", file=sys.stderr)
                sys.exit(1)
            print(f"Intento {attempt + 1} fallido: {e}. Reintentando...", file=sys.stderr)
            time.sleep(5)


def last_hash_path(out_dir: str) -> str:
    return os.path.join(out_dir, ".last_hash")


def load_last_hash(out_dir: str):
    p = last_hash_path(out_dir)
    if os.path.exists(p):
        with open(p) as f:
            return f.read().strip()
    return None


def save_hash(out_dir: str, h: str):
    with open(last_hash_path(out_dir), "w") as f:
        f.write(h)


def append_csv(out_path: str, timestamp_utc: str, trenes: list):
    file_exists = os.path.exists(out_path)
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        if not file_exists:
            writer.writeheader()
        for t in trenes:
            writer.writerow({
                "timestamp_utc":      timestamp_utc,
                "tripId":             t.get("tripId", ""),
                "codTren":            t.get("codTren", ""),
                "codLinea":           t.get("codLinea", ""),
                "retrasoMin":         t.get("retrasoMin", ""),
                "codEstAct":          t.get("codEstAct", ""),
                "codEstSig":          t.get("codEstSig", ""),
                "horaLlegadaSigEst":  t.get("horaLlegadaSigEst", ""),
                "codEstDest":         t.get("codEstDest", ""),
                "codEstOrig":         t.get("codEstOrig", ""),
                "porAvanc":           t.get("porAvanc", ""),
                "latitud":            t.get("latitud", ""),
                "longitud":           t.get("longitud", ""),
                "nucleo":             t.get("nucleo", ""),
                "accesible":          t.get("accesible", ""),
                "via":                t.get("via", ""),
                "nextVia":            t.get("nextVia", ""),
            })


def main():
    now_utc = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    out_dir = os.path.join("data", now_utc.strftime("%Y"), now_utc.strftime("%m"))
    os.makedirs(out_dir, exist_ok=True)

    data = fetch()
    h = sha256(data)

    if load_last_hash(out_dir) == h:
        print("Sin cambios respecto a la captura anterior. No se escriben filas.")
        sys.exit(0)

    parsed = json.loads(data)
    trenes = parsed.get("trenes", [])
    timestamp_utc = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    csv_filename = f"flota-{now_utc.strftime('%Y-%m-%d')}.csv"
    csv_path = os.path.join(out_dir, csv_filename)

    append_csv(csv_path, timestamp_utc, trenes)
    save_hash(out_dir, h)

    print(f"Anadido a  : {csv_path}")
    print(f"Timestamp  : {timestamp_utc}")
    print(f"Trenes     : {len(trenes)}")
    print(f"Actualizado: {parsed.get('fechaActualizacion', '?')}")


if __name__ == "__main__":
    main()
