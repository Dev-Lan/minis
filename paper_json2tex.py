"""
Converts a json file into template .tex file.

Input:
 json file with list of paper references. Each reference is a dictionary with
    - 'id': the citation key
    - 'title': title of the paper
    - 'abstract': abstract of the paper (optional)
    -  among others.


Output:
   - .tex file, either in draft or present format.
   - draft will have:

   % <title>
   % ABSTRACT: <abstract>
   \\cite{<id>}

   - present will have:

    \\paragraph{<title>}
    \\cite{<id>}
    \\begin{itemize}
        \\item ABSTRACT: <abstract>
    \\end{itemize}

the output should be saved in the same direct and name as the input file, but with a .tex extension.
"""

import json
import os
import sys


def load_json(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_tex(output_path, content):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


def format_entry(entry, mode="draft"):
    title = entry.get("title", "No Title")
    abstract = entry.get("abstract", "No Abstract")
    note = entry.get("note", "")
    # split note by newlines
    note_lines = note.split("\n")
    # remove empty lines
    note_lines = [line for line in note_lines if line.strip()]
    # only keep ones that start with 'tldr:'
    note_lines = [line for line in note_lines if line.lower().startswith("tldr:")]
    # remove 'tldr:' from the start of the line
    note_lines = [line[6:].strip() for line in note_lines]
    cid = entry.get("id", "noid")
    if mode == "draft":
        note_text = "\n% ".join(note_lines)
        if len(note_text) > 0:
            note_text = f"\n% {note_text}"
        return f"% {title}\n% ABSTRACT: {abstract[:50]} ... {abstract[-50:]}{note_text}\n% \n\\cite{{{cid}}}\n\n"
    elif mode == "present":
        note_text = "\n    \\item ".join(note_lines)
        if len(note_text) > 0:
            note_text = f"    \\item {note_text}\n"
        return (
            f"\\paragraph{{{title}}}\n"
            f"\\cite{{{cid}}}\n"
            "\\begin{itemize}\n"
            f"    \\item ABSTRACT: {abstract}\n"
            f"{note_text}"
            f"    \\item \n"
            "\\end{itemize}\n\n"
        )
    else:
        raise ValueError("Unknown mode: choose 'draft' or 'present'.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python paper_json2tex.py <input.json>")
        sys.exit(1)
    input_path = sys.argv[1]
    data = load_json(input_path)
    if not isinstance(data, list):
        print("Input JSON must be a list of references.")
        sys.exit(1)
    for mode in ["draft", "present"]:
        tex_content = "".join(format_entry(entry, mode) for entry in data)
        base_filename = os.path.splitext(input_path)[0]
        base_filename += f"_{mode}"
        output_path = base_filename + ".tex"
        write_tex(output_path, tex_content)
        print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
