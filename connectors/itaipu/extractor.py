import csv
import io
from datetime import datetime


def parse_csv(text):
    """Parse CSV del ONS con delimitador ';'."""
    reader = csv.DictReader(io.StringIO(text), delimiter=";")
    rows = []
    for row in reader:
        rows.append({
            "din_instante": datetime.fromisoformat(row["din_instante"]),
            "val_itaipu_total": float(row["val_itaipu_total"]),
            "val_itaipu_60hz": float(row["val_itaipu_60hz"]),
            "val_itaipu_50hz": float(row["val_itaipu_50hz"]),
            "val_itaipu_50hz_br": float(row["val_itaipu_50hz_br"]),
            "val_itaipu_br": float(row["val_itaipu_br"]),
        })
    return rows
