#!/usr/bin/env python3
"""Appendix tables of the paper (paper/tables/*.tex), generated from course_runs/records and paper_numbers.json.

Each file holds one tabular; the captions and labels stay in paper/main.tex. Run scripts/mi_paper_numbers.py first.

usage: python3 scripts/mi_paper_tables.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REC = ROOT / "course_runs" / "records"
OUT = ROOT / "paper" / "tables"
NUM = json.loads((ROOT / "course_runs" / "outputs" / "paper_numbers.json").read_text())
MODELS = ("muril", "xlmrlarge")
NAME = {"muril": "MuRIL", "xlmrlarge": "XLM-R"}


def r2(x):
    """Two decimals, halves rounded up in magnitude (as the figures quoted in the text)."""
    from decimal import Decimal, ROUND_HALF_UP
    return Decimal(repr(round(x, 6))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def f2(x):
    """Two decimals, with a typeset minus."""
    t = str(r2(x))
    if t in ("-0.00", "0.00"):
        t = "0.00"
    return t.replace("-", "$-$")


def read(name):
    return (REC / name).read_text().splitlines()


def write(name, lines):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text("\n".join(lines) + "\n")


def setsize_tables():
    Ks = ("5", "10", "20", "40")
    rows = ["\\begin{tabular}{@{}llcccc@{}}", "\\toprule", "Task & Model & $K=5$ & $K=10$ & $K=20$ & $K=40$ \\\\", "\\midrule"]
    z = ["\\begin{tabular}{@{}llcccc@{}}", "\\toprule", " & & \\multicolumn{2}{c}{Zero ablation} & \\multicolumn{2}{c}{LM cost (nats)} \\\\",
         "Task & Model & $K=10$ & $K=40$ & $K=10$ & $K=40$ \\\\", "\\midrule"]
    for task, tn in (("object", "Agr."), ("wordorder", "Order")):
        for i, m in enumerate(MODELS):
            d = NUM["setsize"][task][m]
            cells = [f"{f2(d[k]['faithfulness']['share'])} / {f2(d[k]['necessity']['share'])}" for k in Ks]
            rows.append(f"{tn if i == 0 else ''} & {NAME[m]} & " + " & ".join(cells) + " \\\\")
            rec = "\n".join(read(f"mi_paper_setsize_{task}_{m}.md"))
            lm = re.search(r"\| mean \| [^|]+\| [^|]+\| [^|]+\| [^|]+\| \w+ \| ([\d.]+) / ([\d.]+) \|", rec)
            z.append(f"{tn if i == 0 else ''} & {NAME[m]} & {f2(d['10']['necessity_zero']['share'])} & {f2(d['40']['necessity_zero']['share'])}"
                     f" & {lm.group(1)} & {lm.group(2)} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    z += ["\\bottomrule", "\\end{tabular}"]
    write("setsize.tex", rows)
    write("zero.tex", z)


def mlpsets_table():
    rows = ["\\begin{tabular}{@{}llccrcc@{}}", "\\toprule", " & & \\multicolumn{3}{c}{Faithfulness} & \\multicolumn{2}{c}{Necessity} \\\\",
            "\\cmidrule(lr){3-5}\\cmidrule(lr){6-7}", "Task & Model & top 5 & others & rank & top 5 & others \\\\", "\\midrule"]
    for task, tn in (("object", "Agr."), ("wordorder", "Order")):
        for i, m in enumerate(MODELS):
            d = NUM["mlpsets"][task][m]
            f, n = d["faith"], d["necessity"]
            nec = ("n/a", "n/a") if (task == "object" and m == "muril") else (f2(n["share"]), f2(n["others_mean"]))
            rows.append(f"{tn if i == 0 else ''} & {NAME[m]} & {f2(f['share'])} & {f2(f['others_mean'])} & {f['rank']}/{f['n_others'] + 1} & {nec[0]} & {nec[1]} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    write("mlpsets.tex", rows)


def ci(text):
    m = re.search(r"([-\d.]+) \| \[([-\d.]+), ([-\d.]+)\]", text)
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def fmt_ci(v):
    return f"{f2(v[0])} [{f2(v[1])}, {f2(v[2])}]"


def kind_table():
    rows = ["\\begin{tabular}{@{}llrl@{}}", "\\toprule", "Control & Model & Pairs & Difference [95\\% CI] \\\\", "\\midrule"]
    for label, fname, header, npairs in (("Other words", "mi_followup_case_wordorder_{m}.md", "| mean difference (bits)", None),
                                         ("Postpositions", "mi_paper_kind_{m}.md", "## Primary (ctlk)", None),
                                         ("Same strings", "mi_paper_kind_{m}.md", "## Secondary (ctls)", None)):
        for i, m in enumerate(MODELS):
            lines = read(fname.format(m=m))
            txt = "\n".join(lines)
            if label == "Other words":
                k = next(j for j, l in enumerate(lines) if l.startswith("| mean difference"))
                v = ci(lines[k + 2])
                n = re.search(r"pairs entering[^:]*\*\*: (\d+)", txt).group(1)
            else:
                k = next(j for j, l in enumerate(lines) if l.startswith(header))
                kk = next(j for j in range(k, len(lines)) if lines[j].startswith("| mean difference"))
                v = ci(lines[kk + 2])
                n = re.search(r"entering the primary test[^:]*: (\d+) / (\d+)", txt).group(1 if label == "Postpositions" else 2)
            rows.append(f"{label if i == 0 else ''} & {NAME[m]} & {n} & {fmt_ci(v)} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    write("kind.tex", rows)


def cues_table():
    rows = ["\\begin{tabular}{@{}llcccc@{}}", "\\toprule", "Model & Cue favours & Pairs & Written & Gap & Heads \\\\", "\\midrule"]
    for m in MODELS:
        txt = read(f"mi_paper_cues_{m}.md")
        ag = next(l for l in txt if l.startswith("| agrees (cue favours written)"))
        dis = next(l for l in txt if l.startswith("| disagrees (cue favours reordered)"))
        for k, (label, line) in enumerate((("written", ag), ("reordered", dis))):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            pairs, written, gap, heads = c[1], c[4].rstrip("%"), c[5], c[6].split(" ")[0]
            rows.append(f"{NAME[m] if k == 0 else ''} & {label} & {pairs} & {written} & {r2(float(gap))} & {r2(float(heads))} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    write("cues.tex", rows)


def size_table():
    rows = ["\\begin{tabular}{@{}lccccc@{}}", "\\toprule", " & & \\multicolumn{2}{c}{MuRIL} & \\multicolumn{2}{c}{XLM-R} \\\\", "Moves & Pairs & gap & share & gap & share \\\\", "\\midrule"]
    data = {}
    for m in MODELS:
        txt = read(f"mi_followup_size_{m}.md")
        k = next(j for j, l in enumerate(txt) if "three size groups" in l)
        for l in txt[k:k + 12]:
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if c[0] in ("1", "2-3", "4+"):
                data.setdefault(c[0], {})[m] = (c[1], float(c[4]), float(c[5].split(" ")[0]))
    for key, lab in (("1", "1"), ("2-3", "2--3"), ("4+", "4 or more")):
        d = data[key]
        rows.append(f"{lab} & {d['muril'][0]} & {r2(d['muril'][1])} & {r2(d['muril'][2])} & {r2(d['xlmrlarge'][1])} & {r2(d['xlmrlarge'][2])} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    write("size.tex", rows)


def halves_table():
    txt = read("mi_swap_compare.md")
    rows = ["\\begin{tabular}{@{}llccccc@{}}", "\\toprule", " & & \\multicolumn{2}{c}{Faithfulness} & \\multicolumn{2}{c}{Necessity} & Shared \\\\",
            "Task & Model & main & swap & main & swap & heads / MLPs \\\\", "\\midrule"]
    shared = {}
    for l in txt:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) == 7 and c[0] in ("object", "wordorder") and c[1] in MODELS:
            shared[(c[0], c[1])] = (c[5], c[6])
    sec = None
    vals = {}
    for l in txt:
        mm = re.match(r"## (object|wordorder), (\w+)", l)
        if mm:
            sec = (mm.group(1), mm.group(2))
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if sec and len(c) >= 3 and c[0] in ("faithfulness", "necessity") and c[1] in ("step 4", "swapped"):
            vals[(sec, c[0], c[1])] = float(c[2])
    for task, tn in (("object", "Agr."), ("wordorder", "Order")):
        for i, m in enumerate(MODELS):
            v = lambda a, b: f2(vals[((task, m), a, b)])
            h, mlp = shared[(task, m)]
            rows.append(f"{tn if i == 0 else ''} & {NAME[m]} & {v('faithfulness', 'step 4')} & {v('faithfulness', 'swapped')} & "
                        f"{v('necessity', 'step 4')} & {v('necessity', 'swapped')} & {h} / {mlp} \\\\")
    rows += ["\\bottomrule", "\\end{tabular}"]
    write("halves.tex", rows)


if __name__ == "__main__":
    setsize_tables()
    mlpsets_table()
    kind_table()
    cues_table()
    size_table()
    halves_table()
    print("wrote tables in", OUT)
