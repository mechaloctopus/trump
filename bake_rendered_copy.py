import re
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent / "index.html"


def bake_rendered_wording(index_path: Path) -> None:
    s = index_path.read_text(encoding="utf-8")

    # Backup
    bak = index_path.with_suffix(index_path.suffix + ".bak")
    if bak.exists():
        bak2 = index_path.with_suffix(index_path.suffix + ".bak2")
        bak2.write_text(s, encoding="utf-8")
    else:
        bak.write_text(s, encoding="utf-8")

    # Only bake the card HTML (before the first <script>)
    idx = s.lower().find("<script")
    pre = s if idx == -1 else s[:idx]
    post = "" if idx == -1 else s[idx:]

    t = pre

    # Titles: bake what cleanDisplayTitle() does at runtime
    t = re.sub(
        r"(<h2[^>]*>\s*)It doesn[’']t help\s*:\s*",
        r"\1",
        t,
        flags=re.IGNORECASE,
    )

    # Text: bake what professionalizeText()/professionalizeHtml() do at runtime
    t = re.sub(r"\bIt also doesn[’']t help that\s+", "Critics also argue that ", t, flags=re.IGNORECASE)
    t = re.sub(r"\bAnd it doesn[’']t help that\s+", "Critics also argue that ", t, flags=re.IGNORECASE)
    t = re.sub(r"\bIt doesn[’']t help that\s+", "Critics argue that ", t, flags=re.IGNORECASE)
    t = re.sub(r"\bIt doesn[’']t help\b", "Critics argue this is concerning", t, flags=re.IGNORECASE)
    t = re.sub(r"\bdoesn[’']t help\b", "is concerning", t, flags=re.IGNORECASE)

    # Subheads: bake what professionalizeHtml() does at runtime
    t = re.sub(
        r'<h3\s+class="subhead">\s*Why critics say this\s*[“"]?doesn[’\']t help[”"]?\s*</h3>',
        '<h3 class="subhead">Why critics consider this relevant</h3>',
        t,
        flags=re.IGNORECASE,
    )
    t = re.sub(
        r'<h3\s+class="subhead">\s*Why critics say this\s*[“"]?is concerning[”"]?\s*</h3>',
        '<h3 class="subhead">Why critics consider this relevant</h3>',
        t,
        flags=re.IGNORECASE,
    )

    index_path.write_text(t + post, encoding="utf-8")


if __name__ == "__main__":
    bake_rendered_wording(INDEX_PATH)
    print("OK: baked rendered wording into index.html (backup: index.html.bak)")
