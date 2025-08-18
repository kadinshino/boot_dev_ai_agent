# functions/get_files_info.py

import os
import stat
import time
from pathlib import Path
from typing import Dict, Any, List

def get_files_info(working_directory: str, directory: str = ".") -> Dict[str, Any]:
    try:
        wd = Path(working_directory).resolve()
        target = (wd / directory).resolve()

        if os.path.commonpath([str(target), str(wd)]) != str(wd):
            return {
                "ok": False,
                "error": f'Cannot list "{directory}": resolved path escapes working directory.',
                "cwd": str(wd),
                "directory": str(Path(directory)),
            }

        if not target.exists():
            return {
                "ok": False,
                "error": f'Path "{directory}" does not exist.',
                "cwd": str(wd),
                "directory": str(Path(directory)),
            }

        if not target.is_dir():
            return {
                "ok": False,
                "error": f'Path "{directory}" is not a directory.',
                "cwd": str(wd),
                "directory": str(Path(directory)),
            }

        entries: List[Dict[str, Any]] = []

        with os.scandir(target) as it:
            for entry in it:
                try:
                    st = entry.stat(follow_symlinks=False)
                    relpath = str(Path(entry.path).resolve().relative_to(wd))
                    entries.append({
                        "name": entry.name,
                        "relpath": relpath,
                        "is_dir": stat.S_ISDIR(st.st_mode),
                        "is_file": stat.S_ISREG(st.st_mode),
                        "is_symlink": entry.is_symlink(),
                        "size": st.st_size,
                        "mode": oct(st.st_mode),
                        "modified_ts": round(st.st_mtime, 2),
                        "modified_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(st.st_mtime)),
                    })
                except Exception as e:
                    entries.append({
                        "name": entry.name,
                        "relpath": str(Path(entry.path)),
                        "error": f"{type(e).__name__}: {e}",
                    })

        entries.sort(key=lambda x: (not x.get("is_dir", False), x.get("name", "").lower()))

        return {
            "ok": True,
            "error": None,
            "cwd": str(wd),
            "directory": str(Path(directory)),
            "entries": entries,
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"Unhandled error: {type(e).__name__}: {e}",
            "cwd": str(Path(working_directory)),
            "directory": str(Path(directory)),
        }
