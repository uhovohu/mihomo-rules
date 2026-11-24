#!/usr/bin/env python3
"""mihomo-rules 生成脚本（算法、输出、检查见 build-spec.md）

本地：python3 scripts/build.py --upstream <上游目录> --out <输出目录> [--prev <上一版 geo 目录>]
线上：python3 scripts/build.py --out <输出目录> --prev <上一版 geo 目录> --mihomo <mihomo 程序>
"""
import argparse, os, re, subprocess, sys, tempfile, urllib.request
from pathlib import Path
import yaml

UPSTREAM_URL = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/{tree}/{kind}/{name}.list"  # tree: geo，或 geo-lite（lite: true）
KINDS = {"geosite": "domain", "geoip": "ipcidr"}  # 目录名 → mihomo convert-ruleset 的类型
ENTRY = re.compile(r"^\s*-\s*['\"]?([^'\"#\s]+)['\"]?")  # 规则文件里的一条


def fail(msg):
    sys.exit(f"✗ {msg}")


# ── 读文件 ──

def read_rule_file(path):
    """返回 (条目列表, 原文行)；add / remove / own 都是 payload: 列表，备注原样保留"""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [m.group(1) for l in lines if (m := ENTRY.match(l))], lines


def read_list(path):
    text = path.read_text(encoding="utf-8")
    if "<html" in text[:1000].lower() or "<!doctype" in text[:1000].lower():
        fail(f"上游是网页不是规则：{path.name}")
    return [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]


def download(url, dest):
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                dest.write_bytes(r.read())
                return
        except Exception as e:
            err = e
    fail(f"拉不到：{url}（{err}）")


# ── 覆盖 ──

def covers(index, e):
    """index = (全部条目, 所有 +. 后缀)；e 被覆盖 = 一模一样，或某个 +.c 是它本身或上级"""
    exact, suffixes = index
    if e in exact:
        return True
    d = e[2:] if e.startswith("+.") else e
    parts = d.split(".")
    return any(".".join(parts[i:]) in suffixes for i in range(len(parts)))


def make_index(entries):
    entries = set(entries)
    return entries, {e[2:] for e in entries if e.startswith("+.")}


# ── 计算每个成品 ──

class Builder:
    def __init__(self, root, upstream, kind, spec):
        self.root, self.upstream, self.kind, self.spec = root, upstream, kind, spec
        self.done, self.visiting = {}, set()
        self.normal = [n for n, s in spec.items() if not s.get("collection") and not s.get("fallback") and "url" not in s]

    def file(self, sub, name):
        p = self.root / sub / self.kind / f"{name}.yaml"
        return p if p.exists() else None

    def build(self, name):
        if name in self.done:
            return self.done[name]
        if name in self.visiting:
            fail(f"minus 循环：{name}")
        if name not in self.spec:
            fail(f"minus 指向不存在的成品：{name}")
        self.visiting.add(name)
        s = self.spec[name]
        if s.get("own"):
            p = self.file("own", name) or fail(f"缺 own/{self.kind}/{name}.yaml")
            entries, lines = read_rule_file(p)
            body = [l for l in lines if not l.startswith("payload")]
            entries = list(dict.fromkeys(entries))
            r = {"entries": entries, "ours": set(entries), "source": "自己维护", "body": body}
        else:
            r = self.compose(name, s)
        self.visiting.discard(name)
        self.done[name] = r
        return r

    def compose(self, name, s):
        src = s.get("from", name)
        base = read_list(self.upstream / self.kind / f"{src}.list")
        source = f"上游 {src}"

        # − remove（文件名用成品名或上游名都认）
        removes = set()
        for n in dict.fromkeys([name, src]):
            if p := self.file("remove", n):
                removes |= set(read_rule_file(p)[0])
        if removes:
            for e in removes - set(base):
                print(f"  ! {self.kind}/{name}：remove 里的 {e} 上游没有")
            base = [e for e in base if e not in removes]
            source += " − 删减"

        # − minus 成品 − 合集自动减（geoip 不做覆盖计算）
        minus = list(s.get("minus", []))
        if s.get("collection"):
            minus += [n for n in self.normal if n != name and n not in minus and n not in s.get("except", [])]
            source += "".join(f" − {m}" for m in s.get("minus", [])) + " − 其他所有规则集"
        else:
            source += "".join(f" − {m}" for m in minus)
        if self.kind == "geosite" and minus:
            idx = make_index(e for m in minus for e in self.build(m)["entries"])
            base = [e for e in base if not covers(idx, e)]
        base = sorted(set(base))

        # + add：本文件其他条目已覆盖的去掉
        body = [f"  # ── 上游 {src} ──"] + [f"  - {e}" for e in base]
        entries, ours = list(base), set()
        if p := self.file("add", name):
            add, lines = read_rule_file(p)
            add = list(dict.fromkeys(add))
            keep = set()
            for e in add:
                pool = base + [x for x in add if x != e]
                if covers(make_index(pool) if self.kind == "geosite" else (set(pool), set()), e):
                    print(f"  · {self.kind}/{name}：add 里的 {e} 已被覆盖，去掉")
                else:
                    keep.add(e)
            for l in lines:  # add 原样的分组和备注，每条只出一次
                m = ENTRY.match(l)
                if m and m.group(1) in keep:
                    entries.append(m.group(1))
                    ours.add(m.group(1))
                    keep.discard(m.group(1))
                    body.append(l)
                elif not m and l.strip() and not l.startswith("payload"):
                    body.append(l)
            source += " + 补充"
        return {"entries": entries, "ours": ours, "source": source, "body": body}


# ── 检查 ──

def count_prev(path):
    return sum(1 for l in path.read_text(encoding="utf-8").splitlines() if ENTRY.match(l)) if path.exists() else 0


def check_overlap(kind, results, spec):
    """我们写的条目（add、own）跟别的成品一模一样 → 返回列表；后缀覆盖只打印
    上游跟上游之间不查；check: false 的（拦截、只用于嗅探的）有意重叠，不查"""
    owner, bad = {}, []
    names = [n for n in results if not spec[n].get("fallback") and spec[n].get("check", True)]
    for n in names:
        for e in results[n]["entries"]:
            if e in owner and (e in results[n]["ours"] or e in results[owner[e]]["ours"]):
                bad.append(f"{kind}: {e}  在 {owner[e]} 和 {n}")
            owner.setdefault(e, n)
    if kind == "geosite":
        sfx = {}
        for n in names:
            for e in results[n]["entries"]:
                if e.startswith("+."):
                    sfx.setdefault(e[2:], n)
        for n in names:
            for e in results[n]["ours"]:
                parts = (e[2:] if e.startswith("+.") else e).split(".")
                for i in range(len(parts)):
                    c = ".".join(parts[i:])
                    if c in sfx and sfx[c] != n and e != f"+.{c}":
                        print(f"  后缀覆盖：{n} 的 {e} ⊂ {sfx[c]} 的 +.{c}")
                        break
    return bad


# ── 主流程 ──

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=Path(__file__).resolve().parent.parent, type=Path, help="仓库目录")
    ap.add_argument("--upstream", type=Path, help="本地上游目录；不给就联网拉（线上模式）")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--prev", type=Path, help="上一版的 geo 目录（70%% 检查用）")
    ap.add_argument("--allow-shrink", default="", help="这次允许条数大减的成品，逗号分隔，如 geosite/xxx（有意精简时用）")
    ap.add_argument("--mihomo", help="mihomo 程序路径（线上模式转 mrs）")
    a = ap.parse_args()
    online = a.upstream is None
    sources = yaml.safe_load((a.root / "sources.yaml").read_text(encoding="utf-8"))

    upstream = a.upstream
    if online:
        upstream = Path(tempfile.mkdtemp())
        for kind, spec in sources.items():
            (upstream / kind).mkdir()
            for name, s in spec.items():
                src, tree = s.get("from", name), "geo-lite" if s.get("lite") else "geo"
                if not s.get("own") and "url" not in s and not (upstream / kind / f"{src}.list").exists():
                    download(UPSTREAM_URL.format(tree=tree, kind=kind, name=src), upstream / kind / f"{src}.list")

    errors = []
    for kind, spec in sources.items():
        spec = {n: s or {} for n, s in spec.items()}
        b = Builder(a.root, upstream, kind, spec)
        order = b.normal + [n for n in spec if n not in b.normal and "url" not in spec[n]]
        results = {n: b.build(n) for n in order}
        outdir = a.out / "geo" / kind
        outdir.mkdir(parents=True, exist_ok=True)

        for name, s in spec.items():
            if "url" in s:  # 别的上游的 mrs，原样转发
                if online:
                    download(s["url"], outdir / f"{name}.mrs")
                    if b"<html" in (outdir / f"{name}.mrs").read_bytes()[:1000].lower():
                        errors.append(f"{name}：拿到的是网页")
                print(f"{kind}/{name}: 原样转发")
                continue
            r = results[name]
            n = len(r["entries"])
            yml = outdir / f"{name}.yaml"
            yml.write_text(f"# 来源：{r['source']}\n# 条数：{n}\n"
                           + ("payload:\n" + "\n".join(r["body"]) + "\n" if n else "payload: []\n"), encoding="utf-8")
            prev = count_prev(a.prev / kind / f"{name}.yaml") if a.prev else 0
            if prev and n < prev * 0.7 and f"{kind}/{name}" not in a.allow_shrink.split(","):
                errors.append(f"{kind}/{name}：{n} 条，上一版 {prev} 条，少于 70%")
            print(f"{kind}/{name}: {n}" + (f"（上一版 {prev}）" if prev else ""))
            if online:
                subprocess.run([a.mihomo, "convert-ruleset", KINDS[kind], "yaml", yml, outdir / f"{name}.mrs"],
                               check=True, capture_output=True)

        errors += check_overlap(kind, results, spec)

    for p in filter(None, os.environ.get("PRIVATE_PATTERNS", "").splitlines()):
        for f in a.out.rglob("*.yaml"):
            if p.strip() and p.strip() in f.read_text(encoding="utf-8"):
                errors.append(f"私人内容出现在 {f.relative_to(a.out)}")

    if errors:
        print(f"\n✗ 检查不过（{len(errors)} 项），不发布：", *errors, sep="\n  ")
        sys.exit(1)
    print("\n✓ 检查全部通过")


if __name__ == "__main__":
    main()
