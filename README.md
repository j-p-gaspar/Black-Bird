# Project Dump Exporter (BlackBirdOs.py)

A lightweight Python utility that **exports an entire software project into a single text file**, including:

- The project README (if present)
- A full directory tree (excluding junk folders)
- The contents of all source code files (in a TeX/LaTeX-friendly format)

This is useful for:
- University project submissions
- Report appendices (LaTeX-friendly)
- Archiving code snapshots
- Sharing full projects for review

---

## Features

- Automatically detects and includes a README file
- Builds a clean directory tree
- Collects and exports all code files into one output file
- Skips common non-source folders (`node_modules`, `.git`, `.venv`, etc.)
- Skips lockfiles (`package-lock.json`, `yarn.lock`, etc.)
- Supports many programming languages and config formats
- Exports code in LaTeX-friendly format using `verbatim`

---

## Output

The script generates:

```
Finance-APP/project_dump.txt
```

The output contains 3 sections:

1. **README info**
2. **Structure of project**
3. **Code files** (each file printed in its own section)

---

## Supported File Types

The tool exports files with these extensions:

- `.py .js .ts .tsx .jsx`
- `.java .go .rs .cpp .c .h .hpp`
- `.cs .php .rb .swift .kt`
- `.sh .ps1 .bat`
- `.html .css .scss .sass`
- `.ipynb .sql .yml .yaml .json .toml`

---

## Ignored Directories

The script skips these directories by default:

- `node_modules`
- `.git`
- `.idea`
- `.vscode`
- `.venv`
- `dist`
- `build`
- `.pytest_cache`
- `__pycache__`

---

## Ignored Files

The script skips these files:

- `package-lock.json`
- `yarn.lock`
- `pnpm-lock.yaml`

---

## How It Works

The script runs 3 main steps:

### 1) README Extraction
It searches for one of:

- `README`
- `README.md`
- `readme.md`
- `Readme.md`

If found, its content is included in the output.

### 2) Directory Tree Generation
The script walks through the project folder and prints a clean directory tree.

### 3) Code Export
All supported code files are appended in a LaTeX-friendly format:

```tex
\section*{File: path/to/file.py}
\begin{verbatim}
...file contents...
\end{verbatim}
```

To avoid breaking LaTeX, any `\end{verbatim}` found inside code is safely rewritten.

---

## Requirements

- Python 3.10+ recommended
- No external libraries required

---

## Usage

### 1) Set the Project Root

Inside `BlackBirdOs.py`, edit:

```python
PROJECT_ROOT = Path(r"Project_Path")
```

Set it to the folder of the project you want to dump.

### 2) Run

```bash
python BlackBirdOs.py
```

---

## Example Console Output

```
[INFO] Starting export for project at: Finance-APP
[STEP] 1/3: Handling README...
[STEP] 2/3: Building project structure...
[STEP] 3/3: Exporting code files...
[DONE] Wrote: Finance-APP/project_dump.txt
```

---

## Customization

You can customize the tool by editing:

- `IGNORE_DIRS`
- `IGNORE_FILES`
- `CODE_EXTS`

---

## License

Free to use and modify for academic and personal projects.
