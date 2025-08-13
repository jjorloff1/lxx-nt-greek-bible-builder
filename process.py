import re, sys, argparse

first_chapter_pattern = r'(\\par \}\s*(?:\\ChapOne\{1\}|\\OneChap)\s*\{\\PP \\VerseOne\{1\}\s*)([Α-Ωα-ω\u0370-\u03FF\u1F00-\u1FFF])([^\s]*)'

# Replacement function to wrap the first Greek letter in lettrine with color
def lettrine_replacer(match):
    prefix = match.group(1)
    first_letter = match.group(2)
    rest_of_word = match.group(3)
    # Use your color and lettrine settings
    return f'{prefix}\\lettrine[lines=2, loversize=0.2, nindent=0em, findent=.25em]{{\\textcolor{{bookheadingcolor}}{{{first_letter}}}}}{{{rest_of_word}}}'

def title_page(title, author=None, include_preamble=False):
    s = ""
    if include_preamble:
        s += f"\\input{{preamble.tex}}\n\n"
    else:
        s += f"\\end{{spacing}}\n"
        
    s += f"\\title{{{title}}}\n"
    if author:
        s += f"\\author{{{author}}}\n"
    else:
        s += f"\\author{{}}\n"
    s += f"\\date{{}}\n\n"
    if include_preamble:
        s += f"\\begin{{document}}\n"
    s += f"\\begin{{spacing}}{{1.1}}\n\\maketitle\n\n"
    return s

ot_part_subtitle = r"""\begin{center}
  {\large Ἡ μετάφρασις τῶν Ἑβδομήκοντα}
\end{center}
"""

def toc_section(section_title):
    return r"""\pagestyle{empty}
\begingroup
\centering
{\huge %s \par}
\vspace{1em}
\endgroup

\begin{multicols}{2}
\makeatletter
\renewcommand{\tableofcontents}{\@starttoc{toc}}
\makeatother
\tableofcontents
\end{multicols}
\pagestyle{fancy}
""" % section_title

FOOT = r"""\vfill
\setlength{\parindent}{0cm}
\fontsize{8}{10}\selectfont{This greek texts used by this work are in the public domain.}

\end{spacing}
\end{document}"""

def process_latex(latex):
    # Apply transformations to the text
    latex = re.sub(r'[“|”]',"", latex) # eliminate custom quotes, must be before first chapter
    latex = re.sub(first_chapter_pattern, lettrine_replacer, latex) # set up dropcaps

    # Fix typos/issues in the source text
    latex = re.sub(r',,', r',', latex, flags=re.M)              # Exodus 33:13
    latex = re.sub(r'ʼΑλλʼ', r'Ἀλλ’', latex, flags=re.M)        # Psalm 1:2
    latex = re.sub(r'(\\par \}\{\\PP )(Ὁ Θεὸς ἔστη ἐν συναγωγῇ θεῶν,)', r'\1\\VS{2}\2', latex, flags=re.M) # Fix missing verse number from Psalm 81:2
    latex = re.sub(r'(\\par \}\{\\PP )(Κλίνον Κύριε τὸ οὖς σου,)', r'\1\\VS{2}\2', latex, flags=re.M) # Fix missing verse number from Psalm 85:2
    latex = re.sub(r'\n\\VS\{2\}(ὁπότε ἐνεπύρισε .*?\.)', r' \1', latex) # Remove verse number from Psalm 59 header
    latex = re.sub(r'ΠΡΟΣΕΥΧ (ἈΜΒΑΚΟΥΜ)', r'ΠΡΟΣΕΥΧΗ \1', latex) # Fix missing eta from Habakkuk 3:1

    # Set up chapter names
    latex = re.sub(r'\{\\MT (.*)', r'\\def\\book{\1}\n\\biblebook{\1}', latex, flags=re.M)

    latex = re.sub(r'\\ChapOne\{1\}', r'', latex, flags=re.M)
    latex = re.sub(r'\\OneChap', r'', latex, flags=re.M)
    latex = re.sub(r'\\VerseOne\{2a\}', r'', latex, flags=re.M)

    # Clean up xetex formatting
    latex = re.sub(r'\\NormalFont\\ShortTitle\{.*?\}', r'', latex, flags=re.M)
    latex = re.sub(r'﻿', r'', latex, flags=re.M)
    latex = re.sub(r'\. [Α-Ωϛ]+ʹ', r'', latex, flags=re.M)
    latex = re.sub(r'^\\par }', r'', latex, flags=re.M)
    latex = re.sub(r'\{\\MM ', r'', latex, flags=re.M)
    latex = re.sub(r'\{\\IP ', r'', latex, flags=re.M)
    latex = re.sub(r'\{\\IS ', r'', latex, flags=re.M)
    latex = re.sub(r'\{\\SH ', r'', latex, flags=re.M)

    # Psalm headings
    latex = re.sub(r'\\PsalmChap\{(\d+)\}\{\\D \\VerseOne\{1\}(.*)\n', r'\\psalmheading{\\ch{\1} \2}', latex, flags=re.M)
    latex = re.sub(r'\\PsalmChap\{(\d+)\}\{\\PP \\VerseOne\{1\}', r'\\ch{\1} ', latex, flags=re.M)
    
    # Note at the end of Psalm 71
    latex = re.sub(r'\{\\D \\VS\{20\}(.*)', r'\n\\textit{\1}', latex, flags=re.M)
    
    latex = re.sub(r'\\Chap\{(\d+)\}', r'\\ch{\1}', latex, flags=re.M)
    latex = re.sub(r'\\VerseOne\{1\}', r'', latex, flags=re.M)
    latex = re.sub(r'VS(\{\d+|\d+[a-z]\})', r'vs\1', latex, flags=re.M)
    latex = re.sub(r'\{\\PP ', r'\n', latex, flags=re.M)

    # Keep psalm headings together with next verse
    latex = re.sub(r'\\psalmheading(\{\\ch\{\d+\}.*?\})(\n|)(.*?\n)', r'\\begin{psalmhead}\1\2\3\\end{psalmhead}\n', latex, flags=re.M)
    
    return latex

def main():
    parser = argparse.ArgumentParser(description="Process OT/NT/Full Bible LaTeX files.")
    parser.add_argument('--ot', help='OT input file')
    parser.add_argument('--nt', help='NT input file')
    parser.add_argument('--output', required=True, help='Output file')
    args = parser.parse_args()

    ot_title = "Η ΠΑΛΑΙΑ ΔΙΑΘΗΚΗ"
    ot_author = "Ἡ μετάφρασις τῶν Ἑβδομήκοντα"
    nt_title = "Η ΚΑΙΝΗ ΔΙΑΘΗΚΗ"
    nt_author = None
    main_title = "Η ΑΓΙΑ ΓΡΑΦΗ"

    with open(args.output, "w", encoding="utf-8") as output:
        if args.ot and args.nt:
            # Full Bible
            with open(args.ot, "r", encoding="utf-8") as otfile, open(args.nt, "r", encoding="utf-8") as ntfile:
                ot_latex = process_latex(otfile.read())
                nt_latex = process_latex(ntfile.read())
                # Main title page (with preamble)
                output.write(title_page(main_title, None, include_preamble=True))
                output.write(toc_section("Table of Contents"))
                # OT section
                output.write("\\cleardoublepage\n")
                output.write(f"\\part{{{ot_title}}}\n")
                output.write(ot_part_subtitle)
                output.write(ot_latex)
                # NT section
                output.write("\\cleardoublepage\n")
                output.write(f"\\part{{{nt_title}}}\n")
                output.write(nt_latex)
                output.write(FOOT)
        elif args.ot:
            # OT only
            with open(args.ot, "r", encoding="utf-8") as otfile:
                ot_latex = process_latex(otfile.read())
                output.write(title_page(ot_title, ot_author, include_preamble=True))
                output.write(toc_section("Table of Contents"))
                output.write(ot_latex)
                output.write(FOOT)
        elif args.nt:
            # NT only
            with open(args.nt, "r", encoding="utf-8") as ntfile:
                nt_latex = process_latex(ntfile.read())
                output.write(title_page(nt_title, nt_author, include_preamble=True))
                output.write(toc_section("Table of Contents"))
                output.write(nt_latex)
                output.write(FOOT)
        else:
            print("Error: At least one of --ot or --nt must be provided.")
            sys.exit(1)

if __name__ == "__main__":
    main()