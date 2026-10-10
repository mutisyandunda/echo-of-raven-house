from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"

BANNED_CLICHES = [
    r"a chill ran down (?:her|his|their) spine",
    r"blood ran cold",
    r"heart skipped a beat",
    r"deafening silence",
    r"if these walls could talk",
    r"secrets buried in the walls",
]

def chapter_files():
    return sorted(p for p in MANUSCRIPT.glob("[0-9][0-9]-*.md"))

def main():
    files = chapter_files()
    problems = []
    if len(files) != 35:
        problems.append(f"Expected 35 chapter files; found {len(files)}")

    titles = {}
    for p in files:
        text = p.read_text(encoding="utf-8")
        m = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", text, re.M)
        if m:
            title = m.group(1)
            if title in titles:
                problems.append(f"Duplicate title: {title}")
            titles[title] = p.name
        draft = text.split("## Draft", 1)[-1]
        for pattern in BANNED_CLICHES:
            if re.search(pattern, draft, re.I):
                problems.append(f"{p.name}: cliché match /{pattern}/")

    if problems:
        print("CONTINUITY / STYLE WARNINGS")
        for p in problems:
            print("-", p)
        return 1

    print("Basic repository checks passed.")
    print("Chapters:", len(files))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
