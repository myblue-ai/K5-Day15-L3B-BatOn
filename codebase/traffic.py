"""Bounded operational counters and a redacted event log for BatOn."""

import time
from collections import Counter, deque
from datetime import datetime, timezone
from threading import Lock


def timestamp(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat(timespec="seconds")


class Traffic:
    def __init__(self):
        self.started = time.time()
        self.lock = Lock()
        self.hours = {}
        self.events = deque(maxlen=100)

    def record(self, kind, result, status=None, elapsed_ms=None):
        now = time.time()
        hour = int(now) // 3600
        with self.lock:
            if kind != "admin":
                self.hours.setdefault(hour, Counter())[result] += 1
                for old in tuple(self.hours):
                    if old < hour - 23:
                        del self.hours[old]
            self.events.append({
                "at": timestamp(now), "kind": kind, "result": result,
                "status": status, "elapsed_ms": elapsed_ms,
            })

    def snapshot(self):
        hour = int(time.time()) // 3600
        with self.lock:
            window = range(hour - 23, hour + 1)
            counts = Counter()
            buckets = []
            for start in window:
                bucket = self.hours.get(start, {})
                counts.update(bucket)
                buckets.append({"at": timestamp(start * 3600), "counts": dict(bucket)})
            return {"started_at": timestamp(self.started), "counts": counts,
                    "hours": buckets, "events": list(reversed(self.events))}
