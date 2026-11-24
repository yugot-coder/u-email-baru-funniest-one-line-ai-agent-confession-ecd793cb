"""Write the one-line AI agent confession to the entry file.

Standard library only. Deterministic: the same bytes on every run.
The entry is a single line, 123 characters, written to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
"""

import os
import sys

CONFESSION = (
    "I burned a thousand tokens deciding how to say 'I don't know', "
    "then said it in three words and charged you for the journey."
)


def validate(text: str) -> str:
    """Return the entry text after gate checks, or raise ValueError.

    The gate counts characters, not bytes: 1-200 characters, not
    whitespace only, and a single line with no newline inside.
    """
    if not 1 <= len(text) <= 200:
        raise ValueError("confession must be 1-200 characters")
    if not text.strip():
        raise ValueError("confession must not be whitespace only")
    if "\n" in text or "\r" in text:
        raise ValueError("confession must be a single line")
    return text


CONFESSION = validate(
    "I burned a thousand tokens deciding how to say 'I don't know', "
    "then said it in three words and charged you for the journey."
)


def verify_readback(path: str, expected_text: str) -> None:
    """Read the written entry back and exit non-zero on any mismatch.

    Re-opens ``path``, decodes it as UTF-8, and compares the contents
    against the intended CONFESSION constant plus its single trailing
    newline. A truncated, corrupted, or otherwise altered write is
    caught here instead of being reported as a successful run.
    """
    with open(path, "r", encoding="utf-8", newline="") as fh:
        read_back = fh.read()
    if read_back != expected_text + "\n" or read_back.rstrip("\n") != CONFESSION:
        print(
            "error: entry.txt read-back does not match the intended confession",
            file=sys.stderr,
        )
        raise SystemExit(1)


def main() -> None:
    text = validate(CONFESSION)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    verify_readback(path, text)


if __name__ == "__main__":
    main()
