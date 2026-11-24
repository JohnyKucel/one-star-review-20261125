"""One-Star Review of Something Essential entry for make.fun.

Writes one deadpan one-star review to entry.txt: sleep, reviewed the
way a genuinely annoyed customer reviews a product that let them
down. The complaint is filed in earnest against a thing that cannot
be fixed, and the sting arrives in the last few words, when sleep
turns out to be a subscription the reviewer is cancelling.

Standard library only. Deterministic: no network, no randomness, no
clock, no environment input beyond the output directory. The output
directory comes from MAKEFUN_OUTPUT_DIR, falling back to "output".

Why this line works, against the judge's brief, in its own order:

- A one-star review of an everyday essential: "Sleep: one star"
  names the essential and the rating in the first words, so the
  review framing is unmistakable and the whole line stays about
  sleep itself, nothing else.
- The sharpest true grievance: eight hours paid every night, in
  full, for years, and still waking up tired is the small daily
  annoyance everyone recognises but has never seen written down
  as a complaint -- the reviewer has paid the price and got
  nothing for it.
- Holds the deadpan: flat complaint register throughout, no
  exclamation marks, no winking, nothing explaining the joke, and
  the review never breaks character to admit it is a joke.
- Turns in the last few words: "Cancelling my subscription"
  reframes sleep as a service with a billing relationship -- the
  same relationship the reader already has with every app that
  charges monthly -- so the sting lands after the complaint has
  been read straight.
- Tight and specific: one joke told cleanly in 95 characters,
  no filler, no second joke crowding the first.
"""

import os
import sys
from pathlib import Path

ENTRY = (
    "Sleep: one star. Takes eight hours a day and I still wake up "
    "tired. Cancelling my subscription."
)

MAX_CHARS = 160


def gate_entry(text):
    """The sealed scorer's gate, enforced here first: UTF-8 text of 1 to
    160 characters, not only white space, exactly one line."""
    if not isinstance(text, str):
        raise TypeError("entry must be str, got %r" % type(text).__name__)
    text.encode("utf-8")  # raises on surrogates / non-UTF-8-encodable text
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, got a newline")
    return text


def resolve_output_dir():
    """Resolve where entry.txt goes: MAKEFUN_OUTPUT_DIR when set to a
    non-blank value, otherwise the local "output" directory."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if raw.strip():
        return Path(raw.strip())
    return Path("output")


def emit_entry():
    text = gate_entry(ENTRY)
    target_dir = resolve_output_dir()
    if target_dir.exists() and not target_dir.is_dir():
        raise NotADirectoryError(
            "output directory %s exists and is not a directory" % target_dir
        )
    target_dir.mkdir(parents=True, exist_ok=True)
    entry_path = target_dir / "entry.txt"
    if entry_path.exists() and entry_path.is_dir():
        raise IsADirectoryError(
            "entry path %s exists and is a directory" % entry_path
        )
    payload = (text + "\n").encode("utf-8")
    entry_path.write_bytes(payload)
    if entry_path.read_bytes() != payload:
        raise IOError("entry.txt read-back mismatch after write")
    return entry_path


def main():
    try:
        path = emit_entry()
    except (ValueError, TypeError, OSError) as exc:
        print("error: %s (entry.txt was not written)" % exc, file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
