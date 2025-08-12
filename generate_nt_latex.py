import csv
import re
import os

import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Mapping for NT books (example for Matthew)
nt_books = {
    40: {'code': 'MAT', 'title': 'ΚΑΤΑ ΜΑΘΘΑΙΟΝ'},
    41: {'code': 'MRK', 'title': 'ΚΑΤΑ ΜΑΡΚΟΝ'},
    42: {'code': 'LUK', 'title': 'ΚΑΤΑ ΛΟΥΚΑΝ'},
    43: {'code': 'JHN', 'title': 'ΚΑΤΑ ΙΩΑΝΝΗΝ'},
    44: {'code': 'ACT', 'title': 'ΠΡΑΞΕΙΣ ΑΠΟΣΤΟΛΩΝ'},
    45: {'code': 'ROM', 'title': 'ΠΡΟΣ ΡΩΜΑΙΟΥΣ'},
    46: {'code': '1CO', 'title': 'ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Α'},
    47: {'code': '2CO', 'title': 'ΠΡΟΣ ΚΟΡΙΝΘΙΟΥΣ Β'},
    48: {'code': 'GAL', 'title': 'ΠΡΟΣ ΓΑΛΑΤΑΣ'},
    49: {'code': 'EPH', 'title': 'ΠΡΟΣ ΕΦΕΣΙΟΥΣ'},
    50: {'code': 'PHP', 'title': 'ΠΡΟΣ ΦΙΛΙΠΠΗΣΙΟΥΣ'},
    51: {'code': 'COL', 'title': 'ΠΡΟΣ ΚΟΛΟΣΣΑΕΙΣ'},
    52: {'code': '1TH', 'title': 'ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Α'},
    53: {'code': '2TH', 'title': 'ΠΡΟΣ ΘΕΣΣΑΛΟΝΙΚΕΙΣ Β'},
    54: {'code': '1TI', 'title': 'ΠΡΟΣ ΤΙΜΟΘΕΟΝ Α'},
    55: {'code': '2TI', 'title': 'ΠΡΟΣ ΤΙΜΟΘΕΟΝ Β'},
    56: {'code': 'TIT', 'title': 'ΠΡΟΣ ΤΙΤΟΝ'},
    57: {'code': 'PHM', 'title': 'ΠΡΟΣ ΦΙΛΗΜΟΝΑ'},
    58: {'code': 'HEB', 'title': 'ΠΡΟΣ ΕΒΡΑΙΟΥΣ'},
    59: {'code': 'JAS', 'title': 'ΙΑΚΩΒΟΥ'},
    60: {'code': '1PE', 'title': 'ΠΕΤΡΟΥ Α'},
    61: {'code': '2PE', 'title': 'ΠΕΤΡΟΥ Β'},
    62: {'code': '1JN', 'title': 'ΙΩΑΝΝΟΥ Α'},
    63: {'code': '2JN', 'title': 'ΙΩΑΝΝΟΥ Β'},
    64: {'code': '3JN', 'title': 'ΙΩΑΝΝΟΥ Γ'},
    65: {'code': 'JUD', 'title': 'ΙΟΥΔΑ'},
    66: {'code': 'REV', 'title': 'ΑΠΟΚΑΛΥΨΙΣ ΙΩΑΝΝΟΥ'},
}

# Special dropcap handling for verse 2 of first chapter
special_dropcap_books = {40, 64}  # 40: ΚΑΤΑ ΜΑΘΘΑΙΟΝ, 64: ΙΩΑΝΝΟΥ Γ

# Set of single-chapter NT books by book number
single_chapter_books = {57, 63, 64, 65}  # PHM, 2JN, 3JN, JUD

# Mapping of problematic words to their hyphenated LaTeX forms
hyphenation_map = {
    "διεμαρτύρατο": r"διε\-μαρ\-τύ\-ρα\-το",
}

def clean_word(word_html):
    # Remove tags and extract text/punctuation
    word = re.sub(r'<.*?>', '', word_html)
    return word

def parse_csv(csv_path):
    book_data = {}

    with open(csv_path, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')

        in_poetry_block = False
        paragraph_marker_next = False
        for row in reader:
            # Skip empty or malformed rows
            if not row or len(row) < 3:
                continue
            # Example: row[1] = '〔40｜1｜1〕'
            book_num, chap_num, verse_num = map(int, re.findall(r'\d+', row[1]))
            word_html = row[2]
            word = clean_word(word_html)

            # Handle poetry quote starts
            poetry_quote_starts = False
            if '<pm>¬</pm>' in word_html:
                poetry_quote_starts = True
                in_poetry_block = True
                word = word.replace('¬', '')

            # Detect paragraph marker
            if '<pm>¶</pm>' in word_html:
                paragraph_marker_next = True
                word = word.replace('¶', '')

            # Remove Special Characters used to annotate text See: https://github.com/eliranwong/OpenGNT/blob/master/fileDescription.md
            word = re.sub(r'[\*=+]', '', word)

            # Ensure book exists
            if book_num not in book_data:
                book_data[book_num] = {}
            # Ensure chapter exists
            if chap_num not in book_data[book_num]:
                book_data[book_num][chap_num] = {}
            # Ensure verse exists
            if verse_num not in book_data[book_num][chap_num]:
                book_data[book_num][chap_num][verse_num] = []

            # Add word to verse
            book_data[book_num][chap_num][verse_num].append((word, paragraph_marker_next, poetry_quote_starts, in_poetry_block))
            
            if paragraph_marker_next:
                in_poetry_block = False # Poetry blocks end at a Paragraph (unless the next word starts a new one)
            paragraph_marker_next = False # Assume next word does not start a new paragraph

    return book_data

def generate_latex_files(book_data, output_folder):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate LaTeX files
    for book_num, book_info in nt_books.items():
        logging.info(f'Processing book {book_info["code"]}: {book_info["title"]}')

        tex_lines = []
        tex_lines.append(f'\\NormalFont\\ShortTitle{{{book_info["title"]}}}')
        tex_lines.append(f'{{\\MT {book_info["title"]}\n')

        tex_lines.extend(generate_book_lines(book_data, book_num))
        
        # Close final paragraph
        tex_lines.append(r'\par }')

        book_content = '\n'.join(tex_lines)
        book_content = '\n'.join(add_poetryblock_to_quotes(book_content.splitlines()))

        out_path = f'{output_folder}/{book_info["code"]}_src.tex'
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write(book_content)
        logging.info(f'Wrote book file: {out_path}')

def add_poetryblock_to_quotes(lines):
    output = []
    in_poetry = False

    for i, line in enumerate(lines):
        # is_quote_line = line.lstrip().contains(r'\par }{\PP \begin{quote}')
        if r'\par }{\PP \begin{quote}' in line and not in_poetry:
            # Start of poetry block
            output.append(r'\begin{poetryblock}')
            in_poetry = True

        output.append(line)

        # Check if next line is not a quote line (or end of file)
        # next_is_quote = (i + 1 < len(lines)) and lines[i + 1].contains(r'\par }{\PP \begin{quote}')
        next_is_quote = (i + 1 < len(lines)) and r'\par }{\PP \begin{quote}' in lines[i + 1]
        if in_poetry and (not next_is_quote or i + 1 == len(lines)):
            # End of poetry block before the next non-quote line
            output.append(r'\end{poetryblock}')
            in_poetry = False

    return output

def generate_book_lines(book_data, book_num):
    book_lines = []

    chapters = book_data.get(book_num, {})
    for chap_num, chapter in chapters.items():
        logging.info(f'  Chapter {chap_num}')
        book_lines.extend(generate_chapter_lines(book_num, chap_num, chapter))
    return book_lines

def generate_chapter_lines(book_num, chap_num, chapter):
    chapter_lines = []

    if chap_num > 1:
        chapter_lines.append('')

    should_add_paragraph_marker = False
    for verse_num, words in chapter.items():
        if verse_num == 1:
            line = first_chapter_first_verse_latex(book_num, chap_num)
        elif should_add_paragraph_marker:
            if should_add_post_dropcap_latex(book_num, chap_num, verse_num):
                line = post_dropcap_new_paragraph_verse_latex(verse_num)
            else:
                line = new_par_with_verse_latex(verse_num)
        else:
            line = verse_latex(verse_num)

        chapter_lines.append(build_line_text(line, words))

        should_add_paragraph_marker = should_start_new_paragraph_next_verse(words)

    return chapter_lines

def first_chapter_first_verse_latex(book_num, chap_num = 1):
    chap_latex = r'\ChapOne{1}'
    if book_num in single_chapter_books:
        chap_latex = r'\OneChap '
    elif (chap_num > 1):
        chap_latex = r'\Chap{' + str(chap_num) + r'}'

    return r'\par }' + chap_latex + r'{\PP \VerseOne{1}'

def should_add_post_dropcap_latex(book_num, chap_num, verse_num):
    return  book_num in special_dropcap_books and chap_num == 1 and verse_num == 2

def should_start_new_paragraph_next_verse(words):
    return words[-1][1] if words else False

def post_dropcap_new_paragraph_verse_latex(verse_num):
    return new_par_latex() + fr'\postdropcapindent' + verse_latex(verse_num)

def new_par_latex():
    return fr'\par }}{{\PP '

def new_par_with_verse_latex(verse_num):
    return new_par_latex() + verse_latex(verse_num)

def verse_latex(verse_num):
    return fr'\VS{{{verse_num}}}'

def build_verse_text(words):
    verse_text = ''
    in_quote = False

    for i, (word, pm_next, poetry_quote_starts, in_poetry_block) in enumerate(words):
        if poetry_quote_starts:
            # in our data set, I never see a paragraph mark in immediately preceding a quote mark
            if i > 0:
                verse_text += '\n' # if first word in new verse, we should already be on a new line.
            verse_text += new_par_latex() + fr'\begin{{quote}}'
            in_quote = True

        verse_text += apply_hyphenation(word)

        # Poetry quote ends: next word starts poetry quote, or paragraph break, or end of verse
        next_word_starts_new_poetry_quote = (i + 1 < len(words)) and words[i + 1][2]
        if in_quote and (next_word_starts_new_poetry_quote or pm_next or i == len(words) - 1):
            verse_text += '\\end{quote}'
            in_quote = False

        if i != len(words) - 1 and pm_next:
            verse_text += '\n' + new_par_latex()
        else:
            verse_text += ' '
    return verse_text

def apply_hyphenation(text):
    for word, hyphenated in hyphenation_map.items():
        text = text.replace(word, hyphenated)
    return text

def build_line_text(line_prefix, words):
    verse_text = build_verse_text(words)
    line_text = line_prefix + verse_text.strip()

    # Handle special case for poetry quotes
    return re.sub(r'\\VS\{(\d+)\}\\par \}\{\\PP \\begin\{quote\}', r'\\par }{\\PP \\begin{quote} \\VS{\1}', line_text)

if __name__ == "__main__":
    import sys
    # Default CSV and output folder, can be overridden by command line args
    csv_path = 'nt_data/OpenGNT_basicHTML.csv'
    output_folder = 'ognt_xetex'
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
    book_data = parse_csv(csv_path)
    generate_latex_files(book_data, output_folder)