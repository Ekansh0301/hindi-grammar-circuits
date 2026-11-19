#!/usr/bin/env python3
"""
Run-record helper. Every experiment script writes one Markdown record under
Results/ alongside whatever data it produces, so a result is never only in a
terminal scrollback or a chat window.

Usage
-----
    from runlog import RunLog

    with RunLog("rq1_masking_equivalence", __file__, args) as log:
        log.h2("Setup")
        log.p("3,000 sentences, news/Training.")
        log.table(["model", "r"], [["mBERT", 0.998]])
        log.kv("n sentences", 3000)
        log.output(path_to_csv)

Everything passed to the log is also printed to stdout, so an interactive run
looks the same as before; the Markdown is a by-product, not a second call.

The record carries provenance deliberately: the exact command line, the
SHA-256 of the script that produced it, library versions, host, and the
size + SHA-256 of every output file. A number in Results/ can therefore be
traced back to the code that made it even after the code changes.
"""
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(os.environ.get("HUTB_RESULTS_DIR", Path(__file__).resolve().parent.parent / "Results"))
_OPEN = []      # RunLogs open in this process, innermost last


def register_output(path, description=""):
    """Checksum `path` into the innermost open RunLog.

    For scripts that print instead of keeping a RunLog and are run under run_with_record.py: the
    wrapper's record is the one that lists the file. Outside any RunLog this only says so."""
    if _OPEN:
        _OPEN[-1].output(path, description)
    else:
        print(f"[!] {path} written outside any run record: no checksum kept", flush=True)


def sha256(path, limit=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _versions():
    out = {"python": sys.version.split()[0]}
    for mod in ("torch", "transformers", "pandas", "numpy", "sklearn", "minicons", "kenlm"):
        try:
            m = __import__(mod)
            out[mod] = getattr(m, "__version__", "?")
        except Exception:
            pass
    try:
        g = subprocess.run(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                           capture_output=True, text=True, timeout=10)
        if g.returncode == 0 and g.stdout.strip():
            out["gpu"] = " | ".join(sorted(set(g.stdout.split("\n")))).strip(" |")
    except Exception:
        pass
    return out


class RunLog:
    def __init__(self, tag, script, args=None, purpose=None, results_dir=None):
        self.tag = tag
        self.script = Path(script).resolve()
        self.args = args
        self.purpose = purpose
        self.dir = Path(results_dir) if results_dir else RESULTS_DIR
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"{tag}.md"
        self.body = []
        self.outputs = []
        self.t0 = time.time()
        self.failed = None

    # ---- emitters -------------------------------------------------
    def _emit(self, console, md):
        if console is not None:
            print(console, flush=True)
        self.body.append(md)

    def h2(self, text):
        self._emit(f"\n=== {text} ===", f"\n## {text}\n")

    def h3(self, text):
        self._emit(f"\n-- {text} --", f"\n### {text}\n")

    def p(self, text):
        self._emit(text, f"{text}\n")

    def note(self, text):
        """A caveat or interpretation, visually separated in the record."""
        self._emit(f"NOTE: {text}", f"\n> {text}\n")

    def kv(self, key, value):
        self._emit(f"    {key}: {value}", f"- **{key}**: {value}")

    def bullet(self, text):
        self._emit(f"  - {text}", f"- {text}")

    def code(self, text, lang=""):
        self._emit(text, f"\n```{lang}\n{text}\n```\n")

    def table(self, headers, rows, floatfmt="{:.4f}"):
        def fmt(v):
            if isinstance(v, float):
                return floatfmt.format(v)
            return "" if v is None else str(v)
        rows = [[fmt(c) for c in r] for r in rows]
        widths = [max(len(str(h)), *(len(r[i]) for r in rows)) if rows else len(str(h))
                  for i, h in enumerate(headers)]
        line = "  ".join(str(h).ljust(w) for h, w in zip(headers, widths))
        print("\n" + line, flush=True)
        print("  ".join("-" * w for w in widths), flush=True)
        for r in rows:
            print("  ".join(c.ljust(w) for c, w in zip(r, widths)), flush=True)
        md = ["", "| " + " | ".join(str(h) for h in headers) + " |",
              "|" + "|".join("---" for _ in headers) + "|"]
        md += ["| " + " | ".join(r) + " |" for r in rows]
        self.body.append("\n".join(md) + "\n")

    def output(self, path, description=""):
        p = Path(path)
        if p.exists():
            self.outputs.append((p, p.stat().st_size, sha256(p), description))
            print(f"[+] wrote {p} ({p.stat().st_size:,} bytes)", flush=True)
        else:
            self.outputs.append((p, None, None, description + " (MISSING)"))
            print(f"[!] expected output missing: {p}", flush=True)

    # ---- context manager -----------------------------------------
    def __enter__(self):
        print(f"[runlog] {self.tag}  ->  {self.path}", flush=True)
        _OPEN.append(self)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self in _OPEN:
            _OPEN.remove(self)
        if exc_type is not None:
            self.failed = f"{exc_type.__name__}: {exc}"
        self.write()
        return False

    def write(self):
        dur = time.time() - self.t0
        v = _versions()
        head = [
            f"# {self.tag}",
            "",
            (f"_{self.purpose}_" if self.purpose else ""),
            "",
            "| provenance | |",
            "|---|---|",
            f"| run (UTC) | {datetime.now(timezone.utc):%Y-%m-%d %H:%M} |",
            f"| script | `{self.script.name}` (sha256 `{sha256(self.script)}`) |",
            f"| host | {socket.gethostname()} ({platform.system()}) |",
            f"| duration | {dur/60:.1f} min |",
            f"| versions | {', '.join(f'{k} {x}' for k, x in v.items())} |",
        ]
        if self.args is not None:
            a = vars(self.args) if hasattr(self.args, "__dict__") else self.args
            head.append(f"| args | `{json.dumps(a, default=str, sort_keys=True)}` |")
        head.append(f"| command | `{' '.join(sys.argv)}` |")
        if self.failed:
            head.append(f"| **STATUS** | **FAILED — {self.failed}** |")
        parts = ["\n".join(head), "\n"] + self.body
        if self.outputs:
            parts.append("\n## Output files\n")
            parts.append("| file | bytes | sha256 | note |")
            parts.append("|---|---|---|---|")
            for p, size, h, d in self.outputs:
                parts.append(f"| `{p.name}` | {size:,} | `{h}` | {d} |" if size is not None
                             else f"| `{p.name}` | — | — | {d} |")
            parts.append("")
        self.path.write_text("\n".join(parts), encoding="utf-8")
        print(f"[runlog] record -> {self.path}", flush=True)
