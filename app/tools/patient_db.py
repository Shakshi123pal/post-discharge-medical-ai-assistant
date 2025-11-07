import json, datetime
from typing import Optional, Dict, List, Tuple

class PatientDB:
    def __init__(self, path="data/patients.jsonl"):
        self.path = path
        self._cache = None

    def _load(self) -> List[Dict]:
        if self._cache is None:
            self._cache = [json.loads(x) for x in open(self.path,encoding="utf-8").read().splitlines()]
        return self._cache

    def lookup(self, name:str) -> Tuple[str, Optional[Dict]]:
        data = self._load()
        matches = [r for r in data if r["patient_name"].lower()==name.strip().lower()]
        if len(matches)==0:
            return ("not_found", None)
        if len(matches)>1:
            return ("multiple", {"candidates":[m["patient_name"] for m in matches]})
        return ("ok", matches[0])
