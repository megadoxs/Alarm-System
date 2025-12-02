import csv
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class LOGS_Controller:
    def __init__(self, dir):
        try:
            self.dir = os.path.join(BASE_DIR, dir)
            os.makedirs(self.dir, exist_ok=True)
        except Exception as e:
            self.connected = False

    def save(self, file, message):
        filename = self._getFile(file)
        file_exists = os.path.exists(filename)

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["timestamp", "message"])

            writer.writerow([datetime.now().strftime('%H:%M:%S'), message])

    def getLatest(self, file):
        filename = self._getFile(file)

        if not os.path.exists(filename):
            return None

        last_value = None
        with open(filename, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                if len(row) > 1:
                    last_value = row[1]
        return last_value

    def _getFile(self, file):
        return os.path.join(str(self.dir), f"{datetime.now().strftime('%Y-%m-%d')}_{file}.csv")