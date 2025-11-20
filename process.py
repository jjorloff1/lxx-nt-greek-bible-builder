import re, sys, argparse

lxx_to_mas_psalms = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": ["9", "10"], "10": "11", "11": "12", "12": "13", 
                     "13": "14", "14": "15", "15": "16", "16": "17", "17": "18", "18": "19", "19": "20", "20": "21", "21": "22", "22": "23", "23": "24", 
                     "24": "25", "25": "26", "26": "27", "27": "28", "28": "29", "29": "30", "30": "31", "31": "32", "32": "33", "33": "34", "34": "35", 
                     "35": "36", "36": "37", "37": "38", "38": "39", "39": "40", "40": "41", "41": "42", "42": "43", "43": "44", "44": "45", "45": "46", 
                     "46": "47", "47": "48", "48": "49", "49": "50", "50": "51", "51": "52", "52": "53", "53": "54", "54": "55", "55": "56", "56": "57", 
                     "57": "58", "58": "59", "59": "60", "60": "61", "61": "62", "62": "63", "63": "64", "64": "65", "65": "66", "66": "67", "67": "68", 
                     "68": "69", "69": "70", "70": "71", "71": "72", "72": "73", "73": "74", "74": "75", "75": "76", "76": "77", "77": "78", "78": "79", 
                     "79": "80", "80": "81", "81": "82", "82": "83", "83": "84", "84": "85", "85": "86", "86": "87", "87": "88", "88": "89", "89": "90", 
                     "90": "91", "91": "92", "92": "93", "93": "94", "94": "95", "95": "96", "96": "97", "97": "98", "98": "99", "99": "100", "100": "101", 
                     "101": "102", "102": "103", "103": "104", "104": "105", "105": "106", "106": "107", "107": "108", "108": "109", "109": "110", 
                     "110": "111", "111": "112", "112": "113", "113": ["114", "115"], "114": "116:1-9", "115": "116:10-19", "116": "117", "117": "118", 
                     "118": "119", "119": "120", "120": "121", "121": "122", "122": "123", "123": "124", "124": "125", "125": "126", "126": "127", 
                     "127": "128", "128": "129", "129": "130", "130": "131", "131": "132", "132": "133", "133": "134", "134": "135", "135": "136", 
                     "136": "137", "137": "138", "138": "139", "139": "140", "140": "141", "141": "142", "142": "143", "143": "144", "144": "145", 
                     "145": "146", "146": "147:1-11", "147": "147:12-20", "148": "148", "149": "149", "150": "150", "151": None}
first_chapter_pattern = r'(\\par \}\s*(?:\\ChapOne\{1\}|\\OneChap)\s*\{\\PP \\VerseOne\{1\}\s*)([Α-Ωα-ω\u0370-\u03FF\u1F00-\u1FFF])([^\s]*)'

preface = r"""\cleardoublepage
\begin{titlepage}
  \begin{center}
    \textcolor{bookheadingcolor}{\Huge Preface}\par
  \end{center}
  \vspace{2em}
  
  This project was undertaken in love and respect for the Bible, with a desire to have an accessible and
  beautiful Greek Bible available in print to anyone who would like one. While there are many great Greek
  New Testaments available in print, the Septuagint has been less accessible, particularly in a format that
  is both compact and minimalist. Most of the Septuagints available in print are quite large. Additionally,
  there are almost no complete Greek Bibles available to purchase for a reasonable price. I have undertaken
  this project for those out there who, like me, want to take a physical Greek Bible along 
  with them where ever they want to go.

  When I started this project, I went hunting for open and public domain editions of the Septuagint and the NT
  that I could use as the texts for this Bible. While there are several great options out there, I settled on
  the Brenton Septuagint and the OpenGNT new testament. The reason for choosing Brenton's Septuagint was simple:
  I found a great open source project that had already digitized the text and prepared it for print: 
  https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/. Starting with this baseline, I was able to
  style the text in a way that I liked. Then I had to find and prepare a NT Text.

  For the NT I chose the Open GNT (https://opengnt.com/) which was prepared by Eliran Wong and released under
  the Creative Commons Attribution 4.0 International License (CC BY 4.0). This project was created "to offer a 
  FREE NA-equivalent text of Greek New Testament, compiled from open-resources" and provided access to the text
  in a format that I could adapt to my needs.

  As for formatting, I was inspired by some of the beautiful minimalist reader Bibles available in English. As
  much as possible, I wanted to keep the text front and center, eliminating distractions and unnecessary elements.
  I have tried to mitigate the distraction from things like section headings, spacing between chapters, and even
  chapter numbers to some degree. I ultimately decided to leave verse numbers in place, because I think navigating
  the Old Testament may have been more difficult without them; however, I tried to minimize their visual impact.
  My goal is to facilitate a novel-like reading experience, free of distractions.

  The source code that I have used to extract, process, and format the texts used for this Bible is available 
  free of charge at https://github.com/jjorloff1/lxx-nt-greek-bible-builder.

  I hope that this Greek Bible will serve you well as you study and meditate on the Scriptures.
  Glory to God!

  \vfill
  \begin{flushright}
    {\large\textit{Jesse Orloff}\par}
    {\large www.jesseorloff.com\par}
    {\large August 2025\par}
  \end{flushright}  
\end{titlepage}

"""

ot_title_page = r"""\cleardoublepage
\thispagestyle{empty}
\vspace*{3cm}
\phantomsection
\addcontentsline{toc}{part}{Η ΠΑΛΑΙΑ ΔΙΑΘΗΚΗ}
\begin{center}
  {\Huge Η ΠΑΛΑΙΑ ΔΙΑΘΗΚΗ}\\[2em]
  {\large Ἡ μετάφρασις τῶν Ἑβδομήκοντα}
\end{center}
\newpage
\thispagestyle{empty}
\null
"""

nt_title_page = r"""\cleardoublepage
\thispagestyle{empty}
\vspace*{3cm}
\phantomsection
\addcontentsline{toc}{part}{Η ΚΑΙΝΗ ΔΙΑΘΗΚΗ}
\begin{center}
  {\Huge Η ΚΑΙΝΗ ΔΙΑΘΗΚΗ}\\[2em]
\end{center}
\newpage
\thispagestyle{empty}
\null
"""

def toc_section(section_title):
    return r"""\cleardoublepage
\pagestyle{empty}
\begingroup
\centering
{\huge \textcolor{bookheadingcolor}{%s} \par}
\endgroup

\begin{multicols}{2}
\makeatletter
\renewcommand{\tableofcontents}{\@starttoc{toc}}
\makeatother
\large\tableofcontents
\end{multicols}
\pagestyle{fancy}

""" % section_title

FOOT = r"""
\end{spacing}
\end{document}"""

# Replacement function to wrap the first Greek letter in lettrine with color
def lettrine_replacer(match):
    prefix = match.group(1)
    first_letter = match.group(2)
    rest_of_word = match.group(3)
    # Use your color and lettrine settings
    return f'{prefix}\\lettrine[lines=2, loversize=0.2, nindent=0em, findent=.25em]{{\\textcolor{{bookheadingcolor}}{{{first_letter}}}}}{{{rest_of_word}}}'

def get_preamble_with_color(use_color=False):
    """Generate preamble line with appropriate color setting"""
    if use_color:
        color_def = r"\definecolor{bookheadingcolor}{HTML}{9B3A3F} % 9B3A3F - Deep red"
    else:
        color_def = r"\definecolor{bookheadingcolor}{HTML}{000000} % 000000 - Pure black for B&W printing"
    
    return f"\\input{{preamble.tex}}\n% Override color setting\n{color_def}\n\n"

def title_page(title, author=None, include_preamble=False, use_color=False):
    s = ""
    if include_preamble:
        s += get_preamble_with_color(use_color)
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

def get_maschal_value(psalm_num):
    masch_val = lxx_to_mas_psalms.get(psalm_num)
    if isinstance(masch_val, list):
        masch_val = '-'.join(masch_val)
    elif masch_val is None:
        masch_val = ''
    return masch_val

def psalmchap_replacer(match):
    psalm_num = match.group(1)
    rest = match.group(2)
    masch_val = get_maschal_value(psalm_num)
    return f'\\psalmheading{{\\ch{{{psalm_num}}}{{{masch_val}}} {rest}}}'

def psalmchap_pp_replacer(match):
    psalm_num = match.group(1)
    masch_val = get_maschal_value(psalm_num)
    return f'\\ch{{{psalm_num}}}{{{masch_val}}}'

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
    latex = re.sub(r'\n\\VS\{23\}Ἔφη· ', r"\n\n\\vs{23}Ἔφη· ", latex) # Spacing of the following poetry block looks better with this starting a new paragraph.

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

    latex = re.sub(r'\\PsalmChap\{(\d+)\}\{\\D \\VerseOne\{1\}(.*)\n', psalmchap_replacer, latex, flags=re.M)
    latex = re.sub(r'\\PsalmChap\{(\d+)\}\{\\PP \\VerseOne\{1\}', psalmchap_pp_replacer, latex, flags=re.M)

    # Note at the end of Psalm 71
    latex = re.sub(r'\{\\D \\VS\{20\}(.*)', r'\n\\textit{\1}', latex, flags=re.M)
    
    latex = re.sub(r'\\Chap\{(\d+)\}', r'\\ch{\1}', latex, flags=re.M)
    latex = re.sub(r'\\VerseOne\{1\}', r'', latex, flags=re.M)
    latex = re.sub(r'VS(\{\d+|\d+[a-z]\})', r'vs\1', latex, flags=re.M)
    latex = re.sub(r'\{\\PP ', r'\n', latex, flags=re.M)

    # Keep psalm headings together with next verse
    latex = re.sub(r'\\psalmheading(\{\\ch\{\d+\}.*?\})(\n|)(.*?\n)', r'\\begin{psalmheading}\1\2\3\\end{psalmheading}\n', latex, flags=re.M)
    
    return latex

def main():
    parser = argparse.ArgumentParser(description="Process OT/NT/Full Bible LaTeX files.")
    parser.add_argument('--ot', help='OT input file')
    parser.add_argument('--nt', help='NT input file')
    parser.add_argument('--output', required=True, help='Output file')
    parser.add_argument('--color', action='store_true', help='Use color headings (default is black and white)')
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
                output.write(title_page(main_title, None, include_preamble=True, use_color=args.color))
                output.write(preface)
                output.write(toc_section("Table of Contents"))
                # OT section
                output.write(ot_title_page)
                output.write(ot_latex)
                # NT section
                output.write(nt_title_page)
                output.write(nt_latex)
                output.write(FOOT)
        elif args.ot:
            # OT only
            with open(args.ot, "r", encoding="utf-8") as otfile:
                ot_latex = process_latex(otfile.read())
                output.write(title_page(ot_title, ot_author, include_preamble=True, use_color=args.color))
                output.write(preface)
                output.write(toc_section("Table of Contents"))
                output.write(ot_latex)
                output.write(FOOT)
        elif args.nt:
            # NT only
            with open(args.nt, "r", encoding="utf-8") as ntfile:
                nt_latex = process_latex(ntfile.read())
                output.write(title_page(nt_title, nt_author, include_preamble=True, use_color=args.color))
                output.write(preface)
                output.write(toc_section("Table of Contents"))
                output.write(nt_latex)
                output.write(FOOT)
        else:
            print("Error: At least one of --ot or --nt must be provided.")
            sys.exit(1)

if __name__ == "__main__":
    main()
