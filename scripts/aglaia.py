#!/usr/bin/env python3
"""Portable, cooperative local governance tools for Aglaia (Python 3.9+)."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / "ops" / "session-governance"
CLAIMS = ROOT / ".aglaia" / "claims"
SENSITIVE = (re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"),
             re.compile(r"\b(?:g" + "hp|github" + r"_pat|sk-[A-Za-z0-9_-]{16,})\b"))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def safe_id(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}", value):
        raise ValueError("run-id must be 3-64 safe characters")
    return value


def display_path(path):
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def append_event(run, event, **data):
    run = safe_id(run)
    folder = GOV / run
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "events.jsonl"
    existing = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()] if path.exists() else []
    if event == "session.start" and existing:
        raise ValueError("run-id already exists; choose a new run-id")
    if existing and existing[-1].get("event") == "session.close":
        raise ValueError("session is closed; append a correction in a new session")
    record = {"at": now(), "run_id": run, "event": event, **data}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def start(args):
    run = safe_id(args.run_id or dt.datetime.now().strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    path = append_event(run, "session.start", objective=args.objective,
                        scope=args.scope, delegated_decisions=args.decisions,
                        resources=args.resources, stop_conditions=args.stop,
                        acceptance=args.acceptance, host=socket.gethostname(), pid=os.getpid())
    print(run)
    print(display_path(path))


def event(args):
    path = append_event(args.run_id, "session.note", kind=args.kind,
                        fact=args.fact, evidence=args.evidence, decision=args.decision,
                        action=args.action, consumer=args.consumer,
                        status=args.status)
    print(display_path(path))


def close(args):
    run = safe_id(args.run_id)
    path = GOV / run / "events.jsonl"
    if not path.exists():
        raise ValueError("session does not exist")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows or rows[0].get("event") != "session.start":
        raise ValueError("session must begin with session.start")
    if rows[-1].get("event") == "session.close":
        raise ValueError("session is already closed")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    append_event(run, "session.close", status=args.status, summary=args.summary,
                 evidence=args.evidence, prior_events_sha256=digest)
    print(display_path(path))


def claim(args):
    name = safe_id(args.resource)
    if args.ttl < 1 or args.ttl > 86400:
        raise ValueError("claim TTL must be between 1 and 86400 seconds")
    CLAIMS.mkdir(parents=True, exist_ok=True)
    path = CLAIMS / (name + ".json")
    payload = {"resource": name, "owner": args.owner, "pid": os.getpid(),
               "host": socket.gethostname(), "created_at": time.time(),
               "expires_at": time.time() + args.ttl}
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        try:
            previous = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            raise ValueError("claim exists but is unreadable; reconcile manually")
        if previous.get("expires_at", float("inf")) > time.time():
            raise ValueError("claim is held; no automatic takeover")
        raise ValueError("claim expired; inspect owner/process and remove explicitly before retry")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(payload, f, sort_keys=True)
        f.write("\n")
    print(display_path(path))


def release(args):
    path = CLAIMS / (safe_id(args.resource) + ".json")
    if not path.exists():
        raise ValueError("claim does not exist")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("owner") != args.owner:
        raise ValueError("claim owner does not match")
    path.unlink()
    print("released")


def verify(args):
    errors = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or ".aglaia" in p.parts or "__pycache__" in p.parts:
            continue
        try:
            raw = p.read_bytes()
        except OSError as exc:
            errors.append(f"cannot read {p.relative_to(ROOT)}: {exc}")
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            errors.append(f"UTF-8 BOM: {p.relative_to(ROOT)}")
        if b"\r" in raw:
            errors.append(f"CR character: {p.relative_to(ROOT)}")
        if raw.endswith(b"\n\n"):
            errors.append(f"multiple trailing newlines: {p.relative_to(ROOT)}")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if args.profile != "fast" or p.suffix.lower() in {".md", ".py", ".yml", ".yaml", ".json", ".txt"}:
            for pattern in SENSITIVE:
                if pattern.search(text):
                    errors.append(f"possible sensitive material: {p.relative_to(ROOT)}")
                    break
        if p.name.endswith(".jsonl"):
            for n, line in enumerate(text.splitlines(), 1):
                try:
                    json.loads(line)
                except json.JSONDecodeError:
                    errors.append(f"invalid JSONL {p.relative_to(ROOT)}:{n}")
    if args.profile in {"impact", "full"}:
        for p in ROOT.rglob("*.md"):
            if ".git" in p.parts or ".aglaia" in p.parts:
                continue
            content = p.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]*\]\(([^)#]+)(?:#[^)]*)?\)", content):
                if "://" in target or target.startswith("mailto:") or target.startswith("/"):
                    continue
                if not (p.parent / target).resolve().exists():
                    errors.append(f"broken local link in {p.relative_to(ROOT)}: {target}")
        sessions = GOV.glob("*/events.jsonl") if GOV.exists() else []
        for path in sessions:
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if rows and rows[0].get("event") != "session.start":
                errors.append(f"session does not start with session.start: {path.relative_to(ROOT)}")
            if sum(r.get("event") == "session.start" for r in rows) > 1:
                errors.append(f"multiple starts: {path.relative_to(ROOT)}")
            if sum(r.get("event") == "session.close" for r in rows) > 1:
                errors.append(f"multiple closes: {path.relative_to(ROOT)}")
            if any(r.get("event") == "session.close" for r in rows[:-1]):
                errors.append(f"events appear after close: {path.relative_to(ROOT)}")
    if args.profile == "full":
        required = ["README.md", "README.en.md", "LICENSE", "NOTICE", "CONTRIBUTING.md",
                    "SECURITY.md", "docs/origem/GENESIS.md", "docs/BRIEFING.md",
                    "docs/governanca/METODO-E-GOVERNANCA.md", "docs/ESTADO.md",
                    "docs/ROADMAP.md", "docs/pesquisa/FERRAMENTAS.md",
                    "docs/fases/fase-0/PLANO.md", "scripts/aglaia.py",
                    ".github/workflows/ci.yml"]
        for item in required:
            if not (ROOT / item).is_file():
                errors.append(f"required foundation file missing: {item}")
        if (ROOT / "README.md").is_file() and (ROOT / "README.en.md").is_file():
            if "## English" not in (ROOT / "README.md").read_text(encoding="utf-8"):
                errors.append("Portuguese README is missing English mirror pointer")
            if "## License" not in (ROOT / "README.en.md").read_text(encoding="utf-8"):
                errors.append("English README is missing license section")
    if errors:
        print("\n".join("ERROR: " + e for e in errors), file=sys.stderr)
        return 1
    print(f"verify {args.profile}: PASS")
    return 0


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("session-start")
    s.add_argument("--run-id")
    s.add_argument("--objective", required=True)
    s.add_argument("--scope", required=True)
    s.add_argument("--decisions", required=True)
    s.add_argument("--resources", required=True)
    s.add_argument("--stop", required=True)
    s.add_argument("--acceptance", required=True)
    s.set_defaults(func=start)
    e = sub.add_parser("event")
    e.add_argument("run_id")
    e.add_argument("--kind", required=True)
    e.add_argument("--fact", required=True)
    e.add_argument("--evidence", required=True)
    e.add_argument("--decision", required=True)
    e.add_argument("--action", required=True)
    e.add_argument("--consumer", required=True)
    e.add_argument("--status", choices=["VERIFIED", "NOT_VERIFIED", "PENDING"], required=True)
    e.set_defaults(func=event)
    c = sub.add_parser("session-close")
    c.add_argument("run_id")
    c.add_argument("--status", choices=["CLOSED", "RECONCILIATION_CLOSED"], required=True)
    c.add_argument("--summary", required=True)
    c.add_argument("--evidence", required=True)
    c.set_defaults(func=close)
    cl = sub.add_parser("claim")
    cl.add_argument("resource")
    cl.add_argument("--owner", required=True)
    cl.add_argument("--ttl", type=int, default=1800)
    cl.set_defaults(func=claim)
    rel = sub.add_parser("release")
    rel.add_argument("resource")
    rel.add_argument("--owner", required=True)
    rel.set_defaults(func=release)
    v = sub.add_parser("verify")
    v.add_argument("--profile", choices=["fast", "impact", "full"], default="fast")
    v.set_defaults(func=verify)
    return p


if __name__ == "__main__":
    try:
        parsed = parser().parse_args()
        sys.exit(parsed.func(parsed))
    except (ValueError, OSError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(2)
