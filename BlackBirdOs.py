import os
from pathlib import Path


PROJECT_ROOT = Path(r"Finance-APP")  # change this
OUTPUT_FILE = PROJECT_ROOT / "project_dump.txt"

# Folders to ignore completely (not your code)
IGNORE_DIRS = {
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    ".venv",
    "dist",
    "build",
    ".pytest_cache",
    "__pycache__",
}

# Files to ignore explicitly (add more if needed)
IGNORE_FILES = {
    "package-lock.json",  # usually generated
    "yarn.lock",
    "pnpm-lock.yaml",
}

# Which file extensions to include as "code"
CODE_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".go", ".rs", ".cpp", ".c", ".h", ".hpp",
    ".cs", ".php", ".rb", ".swift", ".kt",
    ".sh", ".ps1", ".bat",
    ".html", ".css", ".scss", ".sass",
    ".ipynb", ".sql", ".yml", ".yaml", ".json", ".toml",
}

README_NAMES = {"README", "README.md", "readme.md", "Readme.md"}


def find_readme(root: Path) -> Path | None:
    print(f"[INFO] Looking for README in {root}...")
    for name in README_NAMES:
        candidate = root / name
        if candidate.exists():
            print(f"[INFO] Found README: {candidate}")
            return candidate
    print("[WARN] No README found.")
    return None


def read_file(path: Path) -> str:
    print(f"[INFO] Reading file: {path}")
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"[ERROR] Failed to read {path}: {e}")
        return f"<<ERROR READING FILE {path}: {e}>>"


def build_tree(root: Path) -> str:
    print(f"[INFO] Building directory tree for {root}...")
    lines = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Remove ignored dirs in-place so os.walk does not descend into them
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in IGNORE_DIRS
        ]

        rel_dir = Path(dirpath).relative_to(root)
        indent_level = len(rel_dir.parts)
        indent = "    " * indent_level

        lines.append(f"{indent}{rel_dir if rel_dir != Path('.') else '.'}/")

        for fname in sorted(filenames):
            if fname.startswith(".") or fname in IGNORE_FILES:
                continue
            lines.append(f"{indent}    {fname}")
    print("[INFO] Finished building directory tree.")
    return "\n".join(lines)


def is_code_file(path: Path) -> bool:
    return path.suffix in CODE_EXTS


def collect_code(root: Path) -> list[tuple[Path, str]]:
    print(f"[INFO] Collecting code files from {root}...")
    result = []
    file_count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip ignored directories (not your code)
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in IGNORE_DIRS
        ]

        for fname in sorted(filenames):
            if fname.startswith(".") or fname in IGNORE_FILES:
                continue

            fpath = Path(dirpath) / fname
            if is_code_file(fpath):
                file_count += 1
                print(f"[INFO] Processing code file #{file_count}: {fpath}")
                content = read_file(fpath)
                result.append((fpath.relative_to(root), content))
            else:
                # Optional: log non‑code files that are being skipped
                # print(f"[DEBUG] Skipping non-code file: {fpath}")
                pass

    print(f"[INFO] Finished collecting code files. Total: {file_count}")
    return result


def main():
    print(f"[INFO] Starting export for project at: {PROJECT_ROOT}")

    if not PROJECT_ROOT.exists():
        print(f"[ERROR] PROJECT_ROOT does not exist: {PROJECT_ROOT}")
        return

    parts = []

    # 1. README info
    print("[STEP] 1/3: Handling README...")
    readme_path = find_readme(PROJECT_ROOT)
    parts.append("===== Readme info =====\n")
    if readme_path:
        parts.append(f"% README file: {readme_path.name}\n\n")
        parts.append(read_file(readme_path))
    else:
        parts.append("% No README file found.\n")
    parts.append("\n\n")

    # 2. Structure of project
    print("[STEP] 2/3: Building project structure...")
    parts.append("===== Structure of project =====\n\n")
    parts.append(build_tree(PROJECT_ROOT))
    parts.append("\n\n")

    # 3. Code files in TeX‑friendly format
    print("[STEP] 3/3: Exporting code files...")
    parts.append("===== Code files =====\n\n")
    for rel_path, content in collect_code(PROJECT_ROOT):
        print(f"[INFO] Writing section for: {rel_path}")
        parts.append(f"\\section*{{File: {rel_path}}}\n")
        parts.append("\\begin{verbatim}\n")
        safe_content = content.replace("\\end{verbatim}", "\\end{verba\\-tim}")
        parts.append(safe_content.rstrip() + "\n")
        parts.append("\\end{verbatim}\n\n")

    print(f"[INFO] Writing output file: {OUTPUT_FILE}")
    OUTPUT_FILE.write_text("".join(parts), encoding="utf-8")
    print(f"[DONE] Wrote: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
