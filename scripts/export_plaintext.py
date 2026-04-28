#!/usr/bin/env python3
"""
Strip a thesis-chapter .tex file down to plain prose suitable for pasting
into AI-detection tools (GPTZero etc.).

Each paragraph becomes a single unwrapped line; blank lines separate
paragraphs. Figures, tables, equations, citations, and cross-references
are removed entirely. Section titles are kept as bare text on their own
line so the structure is still readable.

Usage:
    python3 scripts/export_plaintext.py <input.tex> <output.txt>
"""

from __future__ import annotations
import re
import sys
from pathlib import Path


def strip_comments(text: str) -> str:
    """Remove % comments (but not \\%)."""
    out_lines = []
    for line in text.splitlines():
        # find unescaped %
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                line = line[:i]
                break
            i += 1
        out_lines.append(line)
    return "\n".join(out_lines)


def strip_environments(text: str, names: list[str]) -> str:
    """Remove \\begin{name}...\\end{name} blocks (greedy, multiline)."""
    for name in names:
        pattern = re.compile(
            r"\\begin\{" + re.escape(name) + r"\*?\}.*?\\end\{" + re.escape(name) + r"\*?\}",
            re.DOTALL,
        )
        text = pattern.sub("", text)
    return text


def expand_lists(text: str) -> str:
    """Convert enumerate/itemize/description into paragraph-separated items.
    Each \\item starts a new paragraph; the surrounding \\begin/\\end are dropped."""
    for env in ("enumerate", "itemize", "description"):
        # \begin{env}...\end{env} → blank-line-separated items
        pattern = re.compile(
            r"\\begin\{" + env + r"\}(.*?)\\end\{" + env + r"\}",
            re.DOTALL,
        )

        def list_repl(match: re.Match) -> str:
            body = match.group(1)
            # split on \item (drop optional [opt-arg]); each becomes its own paragraph
            items = re.split(r"\\item(?:\[[^\]]*\])?", body)
            items = [it.strip() for it in items if it.strip()]
            return "\n\n" + "\n\n".join(items) + "\n\n"

        text = pattern.sub(list_repl, text)
    return text


def cleanup_residue(text: str) -> str:
    """Tidy artefacts left by stripped commands: empty parens, doubled spaces
    before punctuation, dangling brackets, orphan prepositions where a \\cref
    or \\cite used to live."""
    # Empty parens / brackets with optional whitespace inside
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\[\s*\]", "", text)

    # Whitespace before paren close, after paren open
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)

    # Orphan prepositions / connectors immediately before sentence punctuation
    # (these come from stripped \cref{...} or \cite{...} that finished a clause).
    # Pattern: " <preposition> ." → "." ; covers ., ;, : , and ).
    orphans = (
        r"in|of|to|by|from|as|on|with|via|under|within|see|cf"
        r"|using|for|after|before|alongside"
    )
    text = re.sub(
        r"\s+(?:" + orphans + r")\s*([,.;:)])",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    # Stripped citation/cref at the start of a parenthetical: "(, and..." → "(and..."
    # (This catches the artefact without touching legitimate "(and therefore..." prose.)
    text = re.sub(r"\((?:\s*[,;]\s*)+", "(", text)

    # Space before punctuation: "word ." → "word."
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)

    # Doubled punctuation: "word. ." → "word."
    text = re.sub(r"([,.;:])\s*\1+", r"\1", text)

    return text


def strip_conditional_blocks(text: str) -> str:
    """Remove \\ifdefined\\thesismode ... \\else ... \\fi guards but keep the
    \\else branch unaffected; for the closing \\ifdefined\\thesismode \\endinput \\fi
    block, drop it entirely."""
    # Closing block: \ifdefined\thesismode \endinput \fi
    text = re.sub(
        r"\\ifdefined\\thesismode\s*\\endinput\s*\\fi",
        "",
        text,
    )
    # Opening block: \ifdefined\thesismode\else ... \fi  → drop everything
    # between \ifdefined and \fi (the standalone-only preamble)
    text = re.sub(
        r"\\ifdefined\\thesismode\\else.*?\\fi",
        "",
        text,
        flags=re.DOTALL,
    )
    return text


def replace_headings(text: str) -> str:
    """Convert chapter/section/subsection/paragraph commands to bare titles."""
    # \chapter{Title} / \chapter*{Title}
    text = re.sub(r"\\chapter\*?\{([^{}]*)\}", r"\n\n\1\n", text)
    text = re.sub(r"\\section\*?\{([^{}]*)\}", r"\n\n\1\n", text)
    text = re.sub(r"\\subsection\*?\{([^{}]*)\}", r"\n\n\1\n", text)
    text = re.sub(r"\\subsubsection\*?\{([^{}]*)\}", r"\n\n\1\n", text)
    text = re.sub(r"\\paragraph\{([^{}]*)\}", r"\n\n\1\n", text)
    return text


def strip_label_like(text: str) -> str:
    """Remove labels, refs, citations, indexing commands."""
    patterns = [
        r"\\label\{[^{}]*\}",
        r"\\cite\*?\{[^{}]*\}",
        r"\\citep\{[^{}]*\}",
        r"\\citet\{[^{}]*\}",
        r"\\cref\{[^{}]*\}",
        r"\\Cref\{[^{}]*\}",
        r"\\ref\{[^{}]*\}",
        r"\\autoref\{[^{}]*\}",
        r"\\addbibresource\{[^{}]*\}",
        r"\\printbibliography\[[^\]]*\]",
        r"\\printbibliography",
        r"\\bibliography\{[^{}]*\}",
        r"\\bibliographystyle\{[^{}]*\}",
        r"\\index\{[^{}]*\}",
        r"\\nocite\{[^{}]*\}",
    ]
    for p in patterns:
        text = re.sub(p, "", text)
    return text


def replace_units(text: str) -> str:
    """\\SI{value}{unit} → 'value unit', simplifying common SI macros."""
    unit_map = {
        r"\\pico\\joule": "pJ",
        r"\\nano\\joule": "nJ",
        r"\\milli\\joule": "mJ",
        r"\\joule": "J",
        r"\\watt": "W",
        r"\\milli\\watt": "mW",
        r"\\nano\\metre": "nm",
        r"\\milli\\metre": "mm",
        r"\\micro\\metre": "µm",
        r"\\centi\\metre": "cm",
        r"\\metre": "m",
        r"\\milli\\second": "ms",
        r"\\micro\\second": "µs",
        r"\\nano\\second": "ns",
        r"\\second": "s",
    }

    def si_repl(match: re.Match) -> str:
        value = match.group(1).strip()
        unit_arg = match.group(2)
        unit_text = unit_arg
        for macro, repl in unit_map.items():
            unit_text = re.sub(macro, repl, unit_text)
        unit_text = re.sub(r"\\\w+", "", unit_text).strip()
        return f"{value} {unit_text}".strip()

    # \SI{value}{unit}
    text = re.sub(r"\\SI\{([^{}]*)\}\{([^{}]*)\}", si_repl, text)
    # \si{unit}
    def si_unit_only(match: re.Match) -> str:
        unit_arg = match.group(1)
        for macro, repl in unit_map.items():
            unit_arg = re.sub(macro, repl, unit_arg)
        unit_arg = re.sub(r"\\\w+", "", unit_arg).strip()
        return unit_arg

    text = re.sub(r"\\si\{([^{}]*)\}", si_unit_only, text)
    return text


def replace_chemistry(text: str) -> str:
    """\\ce{...} → its argument with subscripts/superscripts flattened."""

    def ce_repl(match: re.Match) -> str:
        s = match.group(1)
        # _{x} or _x → x; ^{x} or ^x → x. Plain text is fine here.
        s = re.sub(r"\^\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"_\{([^{}]*)\}", r"\1", s)
        s = re.sub(r"\^(\w)", r"\1", s)
        s = re.sub(r"_(\w)", r"\1", s)
        return s

    text = re.sub(r"\\ce\{([^{}]+)\}", ce_repl, text)
    return text


def replace_math(text: str) -> str:
    """Replace inline math with stripped contents; display math is dropped."""
    # \[...\] and \begin{equation}...\end{equation} → [equation removed]
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.DOTALL)

    def inline_math(match: re.Match) -> str:
        s = match.group(1)
        # Strip common math markup; keep digits, letters, operators
        s = re.sub(r"\\(text|mathrm|mathbf|mathit|mathcal)\{([^{}]*)\}", r"\2", s)
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
        s = re.sub(r"\\(times|cdot)", "x", s)
        s = re.sub(r"\\sim", "~", s)
        s = re.sub(r"\\to", "→", s)
        s = re.sub(r"\\,", " ", s)
        s = re.sub(r"\\\\", " ", s)
        s = re.sub(r"\\[a-zA-Z]+", "", s)  # drop remaining \cmd
        s = s.replace("{", "").replace("}", "")
        return s

    # \(...\)
    text = re.sub(r"\\\((.+?)\\\)", lambda m: inline_math(m), text, flags=re.DOTALL)
    # $...$
    text = re.sub(r"\$([^$]+)\$", lambda m: inline_math(m), text)
    return text


def replace_emphasis(text: str) -> str:
    """\\textit{X}, \\textbf{X}, \\emph{X}, \\textsc{X} → X."""
    for cmd in ("textit", "textbf", "emph", "textsc", "texttt", "textsf", "uline"):
        text = re.sub(r"\\" + cmd + r"\{([^{}]*)\}", r"\1", text)
    # \texorpdfstring{a}{b} → a
    text = re.sub(r"\\texorpdfstring\{([^{}]*)\}\{[^{}]*\}", r"\1", text)
    return text


def replace_misc_commands(text: str) -> str:
    """Drop residual \\command and clean up dashes / quotes."""
    # Remove common spacing commands
    text = re.sub(r"\\(noindent|clearpage|newpage|cleardoublepage|hfill|vfill|hspace|vspace)\{[^{}]*\}", "", text)
    text = re.sub(r"\\(noindent|clearpage|newpage|cleardoublepage|hfill|vfill)\b", "", text)
    text = re.sub(r"\\(small|footnotesize|tiny|large|Large|huge|normalsize)\b", "", text)
    text = re.sub(r"\\setlength\{[^{}]*\}\{[^{}]*\}", "", text)

    # En-dash, em-dash, ldots
    text = text.replace("---", "—").replace("--", "–")
    text = re.sub(r"\\ldots\b|\\dots\b", "…", text)

    # LaTeX escaped characters
    text = text.replace("~", " ").replace("\\&", "&").replace("\\%", "%")
    text = text.replace("\\#", "#").replace("\\_", "_").replace("\\$", "$")

    # Smart quotes used in LaTeX
    text = text.replace("``", "“").replace("''", "”").replace("`", "‘")

    # Drop remaining backslash-commands of form \cmd or \cmd[...]{...}
    text = re.sub(r"\\[a-zA-Z]+\*?\[[^\]]*\]\{[^{}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+\*?\{[^{}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)

    # Strip braces left over
    text = text.replace("{", "").replace("}", "")
    return text


def collapse_paragraphs(text: str) -> str:
    """Treat blank lines as paragraph separators; join non-blank lines into
    one line per paragraph; collapse runs of whitespace."""
    paragraphs = re.split(r"\n\s*\n+", text)
    cleaned = []
    for p in paragraphs:
        joined = " ".join(line.strip() for line in p.splitlines())
        joined = re.sub(r"\s+", " ", joined).strip()
        if joined:
            cleaned.append(joined)
    return "\n\n".join(cleaned) + "\n"


def convert(tex: str) -> str:
    tex = strip_comments(tex)
    tex = strip_conditional_blocks(tex)
    tex = strip_environments(
        tex,
        names=[
            "figure",
            "table",
            "sidewaystable",
            "equation",
            "align",
            "tabular",
            "tabularx",
        ],
    )
    tex = expand_lists(tex)
    tex = replace_headings(tex)
    tex = strip_label_like(tex)
    tex = replace_units(tex)
    tex = replace_chemistry(tex)
    tex = replace_math(tex)
    tex = replace_emphasis(tex)
    tex = replace_misc_commands(tex)
    tex = cleanup_residue(tex)
    return collapse_paragraphs(tex)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: export_plaintext.py <input.tex> <output.txt>", file=sys.stderr)
        return 2
    src = Path(argv[1])
    dst = Path(argv[2])
    text = src.read_text(encoding="utf-8")
    out = convert(text)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    print(f"wrote {dst} ({len(out)} chars, {out.count(chr(10) + chr(10)) + 1} paragraphs)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
