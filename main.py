"""Write the one-line AI agent confession to the entry file.

Standard library only. Deterministic: the same bytes on every run.
The entry is a single line, 123 characters, written to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
"""

import os

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


def main() -> None:
    text = validate(CONFESSION)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    # Read back and verify the written bytes are exactly what we meant.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != (text + "\n").encode("utf-8"):
        raise ValueError("entry.txt does not match the confession")


if __name__ == "__main__":
    main()
