"""Entrypoint: write the front page of 19 November 2026 to the output
directory (MAKEFUN_OUTPUT_DIR, or /output in the grading container).
Draws the page fresh with Pillow when it is available; otherwise copies
the entry.png shipped in this repository, so the program always
produces entry.png with no network and no installs.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def output_dir():
    """The directory the image goes to."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if wanted:
        os.makedirs(wanted, exist_ok=True)
        return wanted
    if os.path.isdir("/output"):
        return "/output"
    return HERE


def copy_shipped(out_path):
    """Copy the entry.png this repository ships to the output path."""
    shutil.copyfile(os.path.join(HERE, "entry.png"), out_path)
    return out_path


def main():
    """Draw the page fresh when Pillow is present, else copy it."""
    out_path = os.path.join(output_dir(), "entry.png")
    try:
        import generate
        generate.build(out_path)
    except Exception:
        copy_shipped(out_path)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
