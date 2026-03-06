#!/usr/bin/env python3
"""
Minimal stigmergy signal bus for Codex/Claude swarm runs.

Default behavior:
- Agents emit/read signals via shared filesystem footprints.
- `close` emits run.closed and removes run signals by default.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


SIGNAL_TYPES = {
    "run.started",
    "task.offer",
    "task.claim",
    "task.progress",
    "task.blocked",
    "artifact.published",
    "vote.cast",
    "verdict.final",
    "run.closed",
}

PRIORITIES = {"low", "medium", "high", "critical"}
EMISSION_MODES = {"auto", "manual_debug"}
RUNTIMES = {"codex", "claude"}


@dataclass
class SignalRecord:
    path: Path
    signal: Dict[str, Any]


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_utc_iso() -> str:
    return now_utc().isoformat().replace("+00:00", "Z")


def epoch_ms() -> int:
    return int(time.time() * 1000)


def parse_iso_utc(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def hidden_runtime_dir(runtime: str) -> str:
    return ".codex" if runtime == "codex" else ".claude"


def signal_day_dir(base_dir: Path, runtime: str, project_id: str, day: Optional[str] = None) -> Path:
    day_part = day or now_utc().strftime("%Y-%m-%d")
    return base_dir / hidden_runtime_dir(runtime) / "project" / "signal" / project_id / day_part


def signal_project_root(base_dir: Path, runtime: str, project_id: str) -> Path:
    return base_dir / hidden_runtime_dir(runtime) / "project" / "signal" / project_id


def json_load_file(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def json_dump_atomic(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def validate_runtime(value: str) -> str:
    if value not in RUNTIMES:
        raise ValueError(f"runtime must be one of {sorted(RUNTIMES)}")
    return value


def parse_tags(value: str) -> List[str]:
    if not value.strip():
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_payload(payload_json: str, payload_file: str) -> Dict[str, Any]:
    if payload_file:
        with open(payload_file, "r", encoding="utf-8") as f:
            payload = json.load(f)
    else:
        payload = json.loads(payload_json or "{}")
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    return payload


def is_expired(signal: Dict[str, Any], at_time: Optional[datetime] = None) -> bool:
    ref_time = at_time or now_utc()
    timestamp = signal.get("timestamp_utc")
    ttl_seconds = int(signal.get("ttl_seconds", 0))
    if not timestamp or ttl_seconds <= 0:
        return False
    created = parse_iso_utc(str(timestamp))
    return created + timedelta(seconds=ttl_seconds) < ref_time


def collect_records(
    project_root: Path,
    run_id: str = "",
    topic: str = "",
    trace_id: str = "",
    include_expired: bool = True,
) -> List[SignalRecord]:
    if not project_root.exists():
        return []

    out: List[SignalRecord] = []
    for path in sorted(project_root.rglob("*.json")):
        try:
            signal = json_load_file(path)
        except Exception:
            continue

        if run_id and str(signal.get("run_id", "")) != run_id:
            continue
        if topic and str(signal.get("topic", "")) != topic:
            continue
        refs = signal.get("refs", {})
        if trace_id and str(refs.get("trace_id", "")) != trace_id:
            continue
        if not include_expired and is_expired(signal):
            continue

        out.append(SignalRecord(path=path, signal=signal))

    def sort_key(rec: SignalRecord) -> Tuple[str, str]:
        return (str(rec.signal.get("timestamp_utc", "")), rec.path.name)

    out.sort(key=sort_key)
    return out


def make_signal(args: argparse.Namespace) -> Dict[str, Any]:
    signal_id = args.signal_id or f"sig_{uuid.uuid4().hex[:12]}"
    tags = parse_tags(args.tags)
    payload = parse_payload(args.payload_json, args.payload_file)
    if args.signal_type not in SIGNAL_TYPES:
        raise ValueError(f"signal_type must be one of {sorted(SIGNAL_TYPES)}")
    if args.priority not in PRIORITIES:
        raise ValueError(f"priority must be one of {sorted(PRIORITIES)}")
    if args.emission_mode not in EMISSION_MODES:
        raise ValueError(f"emission_mode must be one of {sorted(EMISSION_MODES)}")
    if not (0.0 <= args.confidence <= 1.0):
        raise ValueError("confidence must be in [0,1]")

    trace_id = args.trace_id or f"trace_{args.run_id}"
    pheromone_key = args.pheromone_key or args.topic
    pheromone_strength = args.pheromone_strength
    if pheromone_strength is None:
        pheromone_strength = args.confidence
    pheromone_strength = min(max(float(pheromone_strength), 0.0), 1.0)

    refs: Dict[str, str] = {"trace_id": trace_id}
    if args.parent_signal_id:
        refs["parent_signal_id"] = args.parent_signal_id

    return {
        "signal_id": signal_id,
        "project_id": args.project_id,
        "run_id": args.run_id,
        "timestamp_utc": now_utc_iso(),
        "runtime": args.runtime,
        "agent_id": args.agent_id,
        "signal_type": args.signal_type,
        "emission_mode": args.emission_mode,
        "topic": args.topic,
        "priority": args.priority,
        "confidence": float(args.confidence),
        "ttl_seconds": int(args.ttl_seconds),
        "tags": tags,
        "refs": refs,
        "pheromone": {
            "key": pheromone_key,
            "strength": pheromone_strength,
            "evaporation_half_life_seconds": int(args.half_life_seconds),
        },
        "payload": payload,
    }


def emit_signal(args: argparse.Namespace) -> Dict[str, Any]:
    signal = make_signal(args)
    signal_dir = signal_day_dir(Path(args.base_dir), args.runtime, args.project_id)
    filename = (
        f"{epoch_ms()}__{args.signal_type}__{args.agent_id}__{signal['signal_id']}.json"
    )
    path = signal_dir / filename
    json_dump_atomic(path, signal)
    return {"status": "ok", "path": str(path), "signal_id": signal["signal_id"], "signal": signal}


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_emit(args: argparse.Namespace) -> int:
    out = emit_signal(args)
    print_json(out)
    return 0


def cmd_tail(args: argparse.Namespace) -> int:
    root = signal_project_root(Path(args.base_dir), args.runtime, args.project_id)
    records = collect_records(
        root,
        run_id=args.run_id,
        topic=args.topic,
        trace_id=args.trace_id,
        include_expired=args.include_expired,
    )
    if args.limit > 0:
        records = records[-args.limit :]
    payload = [{"path": str(rec.path), "signal": rec.signal} for rec in records]
    print_json(payload)
    return 0


def cmd_trace(args: argparse.Namespace) -> int:
    if not args.trace_id:
        print("--trace-id is required for trace.", file=sys.stderr)
        return 2
    root = signal_project_root(Path(args.base_dir), args.runtime, args.project_id)
    records = collect_records(
        root,
        run_id=args.run_id,
        topic=args.topic,
        trace_id=args.trace_id,
        include_expired=args.include_expired,
    )
    if args.limit > 0:
        records = records[-args.limit :]
    payload = [{"path": str(rec.path), "signal": rec.signal} for rec in records]
    print_json(payload)
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    root = signal_project_root(Path(args.base_dir), args.runtime, args.project_id)
    seen: set[str] = set()
    start = time.time()

    while True:
        records = collect_records(
            root,
            run_id=args.run_id,
            topic=args.topic,
            trace_id=args.trace_id,
            include_expired=args.include_expired,
        )
        for rec in records:
            sid = str(rec.signal.get("signal_id", ""))
            key = f"{sid}:{rec.path}"
            if key in seen:
                continue
            seen.add(key)
            print_json({"path": str(rec.path), "signal": rec.signal})

        if args.once:
            break
        if args.duration_seconds > 0 and (time.time() - start) >= args.duration_seconds:
            break
        time.sleep(args.interval_seconds)

    return 0


def summarize_stats(records: Iterable[SignalRecord]) -> Dict[str, Any]:
    by_type: Counter[str] = Counter()
    by_topic: Counter[str] = Counter()
    by_agent: Counter[str] = Counter()
    blocked_topics: Counter[str] = Counter()
    expired = 0

    for rec in records:
        signal = rec.signal
        stype = str(signal.get("signal_type", ""))
        topic = str(signal.get("topic", ""))
        agent = str(signal.get("agent_id", ""))
        by_type[stype] += 1
        by_topic[topic] += 1
        by_agent[agent] += 1
        if stype == "task.blocked":
            blocked_topics[topic] += 1
        if is_expired(signal):
            expired += 1

    return {
        "total_signals": sum(by_type.values()),
        "expired_signals": expired,
        "by_type": dict(by_type),
        "by_topic": dict(by_topic),
        "by_agent": dict(by_agent),
        "blocked_topics": dict(blocked_topics),
    }


def cmd_stats(args: argparse.Namespace) -> int:
    root = signal_project_root(Path(args.base_dir), args.runtime, args.project_id)
    records = collect_records(
        root,
        run_id=args.run_id,
        topic=args.topic,
        trace_id=args.trace_id,
        include_expired=True,
    )
    print_json(summarize_stats(records))
    return 0


def delete_records(
    records: Iterable[SignalRecord],
    dry_run: bool = False,
    skip_paths: Optional[set[Path]] = None,
) -> Dict[str, Any]:
    skip = skip_paths or set()
    deleted = 0
    kept = 0
    deleted_paths: List[str] = []

    for rec in records:
        if rec.path in skip:
            kept += 1
            continue
        if dry_run:
            deleted += 1
            deleted_paths.append(str(rec.path))
            continue
        try:
            rec.path.unlink(missing_ok=True)
            deleted += 1
            deleted_paths.append(str(rec.path))
        except Exception:
            kept += 1

    return {"deleted": deleted, "kept": kept, "paths": deleted_paths}


def remove_empty_dirs(root: Path) -> None:
    if not root.exists():
        return
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass
    try:
        root.rmdir()
    except OSError:
        pass


def cmd_cleanup(args: argparse.Namespace) -> int:
    root = signal_project_root(Path(args.base_dir), args.runtime, args.project_id)
    if not root.exists():
        print_json({"status": "ok", "deleted": 0, "kept": 0, "paths": []})
        return 0

    if not args.run_id and not args.all_runs:
        print("Either --run-id or --all-runs is required for cleanup.", file=sys.stderr)
        return 2

    records = collect_records(
        root,
        run_id=args.run_id,
        topic=args.topic,
        trace_id=args.trace_id,
        include_expired=True,
    )
    out = delete_records(records, dry_run=args.dry_run)
    if not args.dry_run and args.remove_empty_dirs:
        remove_empty_dirs(root)
    print_json({"status": "ok", **out})
    return 0


def cmd_close(args: argparse.Namespace) -> int:
    # emit run.closed first
    args.signal_type = "run.closed"
    args.topic = args.topic or "run_lifecycle"
    args.priority = args.priority or "medium"
    args.emission_mode = "auto"
    args.signal_id = ""
    args.confidence = 0.8
    args.ttl_seconds = 300
    args.tags = "swarm,run.closed"
    args.parent_signal_id = ""
    args.pheromone_key = args.topic
    args.pheromone_strength = None
    args.half_life_seconds = 600
    close_payload = {"summary": args.summary}
    if args.payload_json:
        close_payload["extra"] = json.loads(args.payload_json)
    args.payload_json = json.dumps(close_payload, ensure_ascii=False)
    args.payload_file = ""
    emitted = emit_signal(args)
    emitted_path = Path(emitted["path"])

    cleanup_result = {"deleted": 0, "kept": 0, "paths": []}
    if args.cleanup:
        root = signal_project_root(Path(args.base_dir), args.runtime, args.project_id)
        records = collect_records(root, run_id=args.run_id, include_expired=True)
        skip = {emitted_path} if args.keep_closed_signal else set()
        cleanup_result = delete_records(records, dry_run=args.dry_run, skip_paths=skip)
        if not args.dry_run and args.remove_empty_dirs:
            remove_empty_dirs(root)

    print_json(
        {
            "status": "ok",
            "closed_signal": emitted,
            "cleanup": cleanup_result,
            "cleanup_enabled": args.cleanup,
            "keep_closed_signal": args.keep_closed_signal,
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stigmergy signal runtime helper.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--runtime", required=True, choices=sorted(RUNTIMES))
        p.add_argument("--project-id", required=True)
        p.add_argument("--base-dir", default=".")
        p.add_argument("--run-id", default="")
        p.add_argument("--topic", default="")
        p.add_argument("--trace-id", default="")

    # emit
    p_emit = sub.add_parser("emit", help="Emit one signal.")
    add_common(p_emit)
    p_emit.add_argument("--agent-id", required=True)
    p_emit.add_argument("--signal-type", required=True, choices=sorted(SIGNAL_TYPES))
    p_emit.add_argument("--signal-id", default="")
    p_emit.add_argument("--priority", default="medium", choices=sorted(PRIORITIES))
    p_emit.add_argument("--confidence", type=float, default=0.5)
    p_emit.add_argument("--ttl-seconds", type=int, default=1800)
    p_emit.add_argument("--tags", default="")
    p_emit.add_argument("--parent-signal-id", default="")
    p_emit.add_argument("--pheromone-key", default="")
    p_emit.add_argument("--pheromone-strength", type=float, default=None)
    p_emit.add_argument("--half-life-seconds", type=int, default=3600)
    p_emit.add_argument("--payload-json", default="{}")
    p_emit.add_argument("--payload-file", default="")
    p_emit.add_argument("--emission-mode", default="auto", choices=sorted(EMISSION_MODES))
    p_emit.set_defaults(func=cmd_emit)

    # tail
    p_tail = sub.add_parser("tail", help="Read latest signals.")
    add_common(p_tail)
    p_tail.add_argument("--limit", type=int, default=20)
    p_tail.add_argument("--include-expired", action="store_true")
    p_tail.set_defaults(func=cmd_tail)

    # watch
    p_watch = sub.add_parser("watch", help="Watch signal stream.")
    add_common(p_watch)
    p_watch.add_argument("--interval-seconds", type=float, default=3.0)
    p_watch.add_argument("--duration-seconds", type=int, default=0)
    p_watch.add_argument("--include-expired", action="store_true")
    p_watch.add_argument("--once", action="store_true")
    p_watch.set_defaults(func=cmd_watch)

    # trace
    p_trace = sub.add_parser("trace", help="Read signals for one trace.")
    add_common(p_trace)
    p_trace.add_argument("--limit", type=int, default=50)
    p_trace.add_argument("--include-expired", action="store_true")
    p_trace.set_defaults(func=cmd_trace)

    # stats
    p_stats = sub.add_parser("stats", help="Summarize signals.")
    add_common(p_stats)
    p_stats.set_defaults(func=cmd_stats)

    # cleanup
    p_cleanup = sub.add_parser("cleanup", help="Delete signals by run or project.")
    add_common(p_cleanup)
    p_cleanup.add_argument("--all-runs", action="store_true")
    p_cleanup.add_argument("--dry-run", action="store_true")
    p_cleanup.add_argument("--remove-empty-dirs", action="store_true")
    p_cleanup.set_defaults(func=cmd_cleanup)

    # close
    p_close = sub.add_parser(
        "close", help="Emit run.closed and cleanup run signals (default cleanup enabled)."
    )
    add_common(p_close)
    p_close.add_argument("--agent-id", required=True)
    p_close.add_argument("--summary", default="run completed")
    p_close.add_argument("--priority", default="medium", choices=sorted(PRIORITIES))
    p_close.add_argument("--payload-json", default="")
    p_close.add_argument("--cleanup", action="store_true", default=True)
    p_close.add_argument("--no-cleanup", dest="cleanup", action="store_false")
    p_close.add_argument("--keep-closed-signal", action="store_true")
    p_close.add_argument("--dry-run", action="store_true")
    p_close.add_argument("--remove-empty-dirs", action="store_true")
    p_close.set_defaults(func=cmd_close)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.run_id and args.cmd in {"emit", "tail", "watch", "stats", "cleanup", "close"}:
        if args.cmd in {"emit", "close"}:
            parser.error("--run-id is required for emit/close")
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
