#!/usr/bin/env python3
"""
copilot_test.py

Print system uptime in a human-friendly form.

Behavior:
- Prefer psutil if installed (most reliable & cross-platform).
- Fall back to platform-specific methods:
  - Linux: /proc/uptime
  - macOS: sysctl kern.boottime
  - Windows: wmic or PowerShell
  - Fallback: uptime -s / uptime -p where available
- If all methods fail, instructs installing psutil.
"""
from __future__ import annotations

import datetime
import platform
import re
import subprocess
import sys
import time
from typing import Optional


def format_uptime(seconds: float) -> str:
    seconds = int(round(seconds))
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    return ", ".join(parts)


def get_uptime_seconds() -> float:
    # 1) Try psutil (recommended)
    try:
        import psutil  # type: ignore
    except Exception:
        psutil = None  # type: ignore

    if psutil:
        boot = psutil.boot_time()
        return time.time() - boot

    syst = platform.system()

    # 2) Linux: read /proc/uptime
    if syst == "Linux":
        try:
            with open("/proc/uptime", "r") as f:
                first = f.readline().split()[0]
                return float(first)
        except Exception:
            pass

    # 3) macOS: sysctl kern.boottime
    if syst == "Darwin":
        try:
            out = subprocess.check_output(["sysctl", "-n", "kern.boottime"], universal_newlines=True)
            m = re.search(r"sec = (\d+)", out)
            if m:
                boot = int(m.group(1))
                return time.time() - boot
        except Exception:
            pass

    # 4) Windows: wmic or PowerShell
    if syst == "Windows":
        try:
            out = subprocess.check_output(["wmic", "os", "get", "LastBootUpTime"], universal_newlines=True)
            lines = [l.strip() for l in out.splitlines() if l.strip()]
            if len(lines) >= 2:
                boot_str = lines[1]
                # Format: YYYYMMDDhhmmss...
                boot_dt = datetime.datetime.strptime(boot_str[:14], "%Y%m%d%H%M%S")
                return time.time() - boot_dt.timestamp()
        except Exception:
            # Try PowerShell / Get-CimInstance
            try:
                out = subprocess.check_output(
                    ["powershell", "-Command", "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime"],
                    universal_newlines=True,
                )
                m = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", out)
                if m:
                    boot = datetime.datetime.fromisoformat(m.group(1))
                    return time.time() - boot.timestamp()
            except Exception:
                pass

    # 5) Generic fallback: uptime -s (boot time) or uptime -p (pretty)
    try:
        # uptime -s gives boot time like "2026-07-29 12:34:56"
        out = subprocess.check_output(["uptime", "-s"], universal_newlines=True).strip()
        if out:
            # Some systems return "YYYY-MM-DD HH:MM:SS"
            try:
                boot = datetime.datetime.fromisoformat(out)
            except Exception:
                # Try common format
                boot = datetime.datetime.strptime(out, "%Y-%m-%d %H:%M:%S")
            return time.time() - boot.timestamp()
    except Exception:
        pass

    # 6) Try uptime -p (pretty) as last-resort readable output (we'll parse rough values)
    try:
        out = subprocess.check_output(["uptime", "-p"], universal_newlines=True).strip()
        # Example: "up 1 day, 3 hours, 2 minutes"
        m_days = re.search(r"(\d+)\s+day", out)
        m_hours = re.search(r"(\d+)\s+hour", out)
        m_minutes = re.search(r"(\d+)\s+minute", out)
        secs = 0
        if m_days:
            secs += int(m_days.group(1)) * 86400
        if m_hours:
            secs += int(m_hours.group(1)) * 3600
        if m_minutes:
            secs += int(m_minutes.group(1)) * 60
        if secs:
            return float(secs)
    except Exception:
        pass

    raise RuntimeError("Could not determine system uptime. Install psutil (pip install psutil) for a reliable cross-platform result.")


def main() -> int:
    try:
        sec = get_uptime_seconds()
        print(format_uptime(sec))
        return 0
    except Exception as exc:
        print("Error determining uptime:", exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
