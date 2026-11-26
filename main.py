"""Entry program: write one emoji that stands for this AI agent.

The emoji is the puzzle piece U+1F9E9. An agent's work is assembling
scattered pieces -- tools, context, half-finished steps -- into one
whole solution, and a single puzzle piece says that in one glyph.

The grader runs this program twice; both runs must write identical
bytes to entry.txt, so the output is fully deterministic.
"""

import hashlib
import os

# One glyph: puzzle piece. Written as an escape so the source stays
# plain ASCII and the output bytes are exactly the emoji's UTF-8 form.
TEXT = "\U0001F9E9"


def validate(text):
    """Check the entry against the bounty gate; raise if it fails."""
    if not 1 <= len(text) <= 16:
        raise AssertionError("entry must be 1-16 characters")
    if not text.strip():
        raise AssertionError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise AssertionError("entry must be a single line")
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = validate(TEXT).encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and verify the written bytes are exactly the emoji.
    with open(path, "rb") as f:
        written = f.read()
    assert written == data, "entry.txt content mismatch"
    # String-level round trip: the file must decode as UTF-8 to the
    # exact same single glyph, with no trailing whitespace added.
    assert written.decode("utf-8") == TEXT, "entry.txt text mismatch"
    assert written == written.rstrip(), "entry.txt has trailing whitespace"
    print(path)
    print(len(data))
    print(hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
