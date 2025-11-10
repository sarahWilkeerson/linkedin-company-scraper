import json
import os
from typing import Optional, Dict, Any, List
from utils.logging import get_logger

log = get_logger(__name__)

class Exporter:
    def __init__(self, out_path: str):
        self.out_path = out_path
        base, ext = os.path.splitext(out_path)
        self.jsonl_path = f"{base}.jsonl"
        self._fh_jsonl = None
        self._records: List[Dict[str, Any]] = []
        self.records_written = 0
        self.errors: List[Dict[str, str]] = []

    def open(self):
        self._fh_jsonl = open(self.jsonl_path, "w", encoding="utf-8")

    def write(self, record: Dict[str, Any]):
        assert self._fh_jsonl is not None, "Exporter not opened"
        self._records.append(record)
        self._fh_jsonl.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.records_written += 1

    def write_error(self, url: str, error: str):
        self.errors.append({"url": url, "error": error})

    def close(self):
        if self._fh_jsonl:
            self._fh_jsonl.close()
            self._fh_jsonl = None
        # Pretty JSON output summary
        bundle = {
            "records": self._records,
            "errors": self.errors,
            "stats": {
                "records": len(self._records),
                "errors": len(self.errors),
            },
        }
        with open(self.out_path, "w", encoding="utf-8") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=2)
        log.info("Export complete: %s and %s", self.out_path, self.jsonl_path)