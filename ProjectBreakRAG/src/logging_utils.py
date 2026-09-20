from datetime import datetime
import json
from pathlib import Path


LOG_PATH = Path("logs")
LOG_FILE = LOG_PATH / "queries.log"


def guardar_log(pregunta, k, chunks, modelo, tiempo):
    """
    Guarda información de cada consulta realizada al sistema RAG.
    """

    LOG_PATH.mkdir(exist_ok=True)

    registro = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "pregunta": pregunta,
        "k": k,
        "chunks": chunks,
        "modelo": modelo,
        "tiempo_segundos": round(tiempo, 3)
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False))
        f.write("\n")