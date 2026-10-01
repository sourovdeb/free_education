#!/usr/bin/env python3
"""Story Factory: deterministic, bounded media handoff. Python 3.10+; no pip dependencies.

This is a still-image animatic runner, NOT a character-animation engine.
Blender-native construction is a separate, explicitly invoked adapter.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EFFECTS = ("still", "push_in", "pan_right")
SIZES = {"preview": (640, 360), "hd": (1280, 720), "fullhd": (1920, 1080)}


def safe_path(root: Path, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute():
        raise ValueError("Use a relative path inside the kit.")
    target = (root / p).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("Path escapes the kit directory.")
    return target


def load_catalog(root: Path = ROOT) -> dict:
    catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
    if catalog.get("schema_version") not in ("1.0", 1, "1", "1.0.0"):
        raise ValueError(f"Unsupported catalogue schema: {catalog.get('schema_version')!r}")
    return catalog


def find_item(catalog: dict, item_id: str) -> dict:
    matches = [x for x in catalog["assets"] + catalog["scenes"] if x["id"] == item_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one catalogue item for {item_id!r}; found {len(matches)}.")
    return matches[0]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def build_plan(catalog: dict, item_id: str, seconds: float = 12, fps: int = 25,
               size: str = "preview", effect: str = "still", root: Path = ROOT) -> dict:
    if not math.isfinite(seconds) or not 1 <= seconds <= 60:
        raise ValueError("This pilot runner accepts 1–60 seconds; assemble longer work as separate shots.")
    if fps not in (24, 25, 30) or size not in SIZES or effect not in EFFECTS:
        raise ValueError("Unsupported FPS, size or effect. Use --help for accepted values.")
    item = find_item(catalog, item_id)
    image = safe_path(root, item["png"])
    if not image.is_file():
        raise FileNotFoundError(f"Missing image: {item['png']}")
    frames = round(seconds * fps)
    plan = {"schema_version": "1.0", "kit_version": catalog.get("kit_version"),
            "item_id": item_id, "image": item["png"], "image_sha256": digest(image),
            "effect": effect, "fps": fps, "frames": frames, "seconds": frames / fps,
            "size": list(SIZES[size]), "mode": "STILL_IMAGE_ANIMATIC",
            "limitations": "No limb animation; PNG detail is limited by source size. Not a Blender render."}
    encoded = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()
    plan["job_id"] = hashlib.sha256(encoded).hexdigest()[:16]
    return plan


def command_output(args: list[str], timeout: int = 10) -> str:
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return (p.stdout or p.stderr).strip()[:1500]
    except (OSError, subprocess.TimeoutExpired) as e:
        return f"UNAVAILABLE: {type(e).__name__}: {e}"


def doctor() -> dict:
    result = {"python": sys.version.split()[0], "platform": platform.platform(),
              "tools": {}, "resolve_api": "NOT_PROBED: use the installed Scripting README; manual import remains available.",
              "network": "No network calls or installations are performed."}
    for name in ("ffmpeg", "ffprobe", "blender"):
        exe = shutil.which(name)
        result["tools"][name] = {"path": exe, "version": command_output([exe, "--version" if name == "blender" else "-version"]).splitlines()[:1] if exe else [],
                                 "available": bool(exe)}
    if platform.system() == "Windows" and not result["tools"]["blender"]["available"]:
        base = Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Blender Foundation"
        result["blender_candidates"] = [str(p) for p in base.glob("Blender*/blender.exe")] if base.exists() else []
    nvidia = shutil.which("nvidia-smi")
    result["gpu"] = command_output([nvidia, "--query-gpu=name,memory.total,memory.free", "--format=csv,noheader,nounits"]) if nvidia else "UNKNOWN; no GPU memory guarantee is made."
    usage = shutil.disk_usage(ROOT)
    result["free_disk_bytes"] = usage.free
    return result


def validate_catalog(root: Path = ROOT) -> dict:
    c = load_catalog(root)
    errors, ids = [], set()
    for item in c["assets"] + c["scenes"]:
        if item["id"] in ids:
            errors.append("Duplicate ID: " + item["id"])
        ids.add(item["id"])
        for ext in ("glb", "png", "svg"):
            if ext not in item:
                continue
            try:
                p = safe_path(root, item[ext])
                if not p.is_file() or not p.stat().st_size:
                    errors.append("Missing/empty: " + item[ext])
            except ValueError as e:
                errors.append(str(e))
    asset_ids = {a["id"] for a in c["assets"]}
    for scene in c["scenes"]:
        for ref in scene["asset_ids"]:
            if ref not in asset_ids:
                errors.append(f"Unknown asset reference {ref} in {scene['id']}")
    return {"status": "PASS" if not errors else "FAIL", "assets": len(c["assets"]),
            "scenes": len(c["scenes"]), "errors": errors, "scope": "Catalogue references only; not application compatibility."}


def video_command(plan: dict, destination: Path, ffmpeg: str, root: Path = ROOT) -> list[str]:
    w, h = plan["size"]
    motion = "null"
    denom = max(1, plan["frames"] - 1)
    if plan["effect"] == "push_in":
        motion = f"zoompan=z='1+0.055*on/{denom}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={w}x{h}:fps={plan['fps']}"
    elif plan["effect"] == "pan_right":
        motion = f"zoompan=z=1.06:x='(iw-iw/zoom)*on/{denom}':y='ih/2-ih/zoom/2':d=1:s={w}x{h}:fps={plan['fps']}"
    # Flatten alpha over a real background BEFORE removing the alpha channel.
    filters = (f"[0:v]format=rgba,scale={w}:{h}:force_original_aspect_ratio=decrease,"
               f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x00000000[fit];"
               f"color=c=0xF2E9DB:s={w}x{h}:r={plan['fps']}[bg];"
               f"[bg][fit]overlay=shortest=1:format=auto,format=rgb24,{motion},format=yuv420p[v]")
    return [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n", "-loop", "1", "-framerate", str(plan["fps"]),
            "-i", str(safe_path(root, plan["image"])), "-filter_complex_threads", "2", "-filter_complex", filters, "-map", "[v]", "-frames:v", str(plan["frames"]),
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "2", "-movflags", "+faststart", str(destination)]


def render_video(plan: dict, root: Path = ROOT) -> dict:
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("FFmpeg and ffprobe must both be installed and on PATH. Nothing installed automatically; use manual Resolve import instead.")
    job_dir = safe_path(root, "output/" + plan["job_id"])
    job_dir.mkdir(parents=True, exist_ok=True)
    movie, receipt = job_dir / "preview.mp4", job_dir / "complete.json"
    if receipt.is_file() and movie.is_file():
        old = json.loads(receipt.read_text())
        if old.get("video_sha256") == digest(movie) and old.get("job_id") == plan["job_id"]:
            return {**old, "status": "REUSED_VERIFIED_OUTPUT"}
        raise RuntimeError("Existing output does not match its receipt; preserve it and choose a different job.")
    lock = job_dir / "render.lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError("This job is already locked. Verify that no render is active before manually removing render.lock.") from None
    os.close(fd)
    temp = job_dir / "preview.partial.mp4"
    try:
        if temp.exists() or movie.exists():
            raise RuntimeError("An unverified output exists. It was not overwritten; inspect this job folder.")
        (job_dir / "plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
        p = subprocess.run(video_command(plan, temp, ffmpeg, root), capture_output=True, text=True, timeout=600, check=False)
        if p.returncode:
            raise RuntimeError(f"FFmpeg exit {p.returncode}: {p.stderr[-1800:]}")
        probe = subprocess.run([ffprobe, "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=width,height,nb_read_frames,r_frame_rate", "-of", "json", str(temp)], capture_output=True, text=True, timeout=30, check=True)
        stream = json.loads(probe.stdout)["streams"][0]
        num, den = map(int, stream["r_frame_rate"].split("/"))
        if [stream["width"], stream["height"]] != plan["size"] or int(stream["nb_read_frames"]) != plan["frames"] or num / den != plan["fps"]:
            raise RuntimeError("Rendered dimensions, duration or FPS did not match the plan.")
        os.replace(temp, movie)
        record = {"status": "PASS_STILL_ANIMATIC", "job_id": plan["job_id"], "video_sha256": digest(movie), "frames": plan["frames"], "fps": plan["fps"], "size": plan["size"], "video": str(movie.relative_to(root)), "native_blender_test": "NOT_RUN", "resolve_test": "NOT_RUN"}
        receipt.write_text(json.dumps(record, indent=2), encoding="utf-8")
        return record
    except Exception as exc:
        (job_dir / "failure.json").write_text(json.dumps({"status": "FAILED", "error": str(exc)}, indent=2), encoding="utf-8")
        raise
    finally:
        lock.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("doctor")
    sub.add_parser("validate")
    for action in ("plan", "video"):
        p = sub.add_parser(action)
        p.add_argument("--id", required=True, help="ID shown in START_HERE.html")
        p.add_argument("--seconds", type=float, default=12)
        p.add_argument("--fps", type=int, choices=(24, 25, 30), default=25)
        p.add_argument("--size", choices=SIZES, default="preview")
        p.add_argument("--effect", choices=EFFECTS, default="still")
    args = parser.parse_args(argv)
    try:
        if args.action == "doctor": result = doctor()
        elif args.action == "validate": result = validate_catalog()
        else:
            result = build_plan(load_catalog(), args.id, args.seconds, args.fps, args.size, args.effect)
            if args.action == "video": result = render_video(result)
        print(json.dumps(result, indent=2))
        return 1 if result.get("status") == "FAIL" else 0
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, KeyError) as e:
        print(json.dumps({"status": "FAILED", "error": str(e)}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
