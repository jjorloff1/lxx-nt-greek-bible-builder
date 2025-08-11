import csv
import re
import os

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

def clean_word(word_html):
    # Remove <a> tags and extract text/punctuation
    word = re.sub(r'<.*?>', '', word_html)
    return word

def parse_csv_and_generate_tex(csv_path, output_folder):
    # Ensure output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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
                word = word.replace('<pm>¬</pm>', '¬')

            # Detect paragraph marker
            if '<pm>¶</pm>' in word_html:
                paragraph_marker_next = True
                word = word.replace('<pm>¶</pm>', '')
            # Remove stray paragraph marks
            word = word.replace('¶', '')

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

    # Set of single-chapter NT books by book number
    single_chapter_books = {57, 62, 63, 64, 65}  # PHM, 1JN, 2JN, 3JN, JUD

    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Special dropcap handling for verse 2 of first chapter
    special_dropcap_books = {40, 64}  # 40: ΚΑΤΑ ΜΑΘΘΑΙΟΝ, 64: ΙΩΑΝΝΟΥ Γ

    for book_num, book_info in nt_books.items():
        logging.info(f'Processing book {book_info["code"]}: {book_info["title"]}')
        tex_lines = []
        tex_lines.append(f'\\NormalFont\\ShortTitle{{{book_info["title"]}}}')
        tex_lines.append(f'{{\\MT {book_info["title"]}\n')
        chapters = book_data.get(book_num, {})
        if book_num in single_chapter_books:
            # Single-chapter book formatting (MAN_src.tex model)
            first_para = True
            should_add_paragraph_marker = False
            for verse_num, words in chapters.get(1, {}).items():
                if first_para and verse_num == 1:
                    line = r'\par }\OneChap {\PP \VerseOne{1}'
                    first_para = False
                elif should_add_paragraph_marker:
                    if book_num in special_dropcap_books and verse_num == 2:
                        line = fr'\par }}{{\PP \postdropcapindent\VS{{{verse_num}}}'
                    else:
                        line = fr'\par }}{{\PP \VS{{{verse_num}}}'
                else:
                    line = fr'\VS{{{verse_num}}}'

                tex_lines.append(build_line_text(line, words))

                should_add_paragraph_marker = words[-1][1] if words else False
        else:
            # Multi-chapter book formatting (GEN_src.tex model)
            for chap_num, verses in chapters.items():
                logging.info(f'  Chapter {chap_num}')
                if chap_num == 1:
                    first_para = True
                    should_add_paragraph_marker = False
                    for verse_num, words in verses.items():
                        if first_para and verse_num == 1:
                            line = r'\par }\ChapOne{1}{\PP \VerseOne{1}'
                            first_para = False
                        elif should_add_paragraph_marker:
                            if book_num in special_dropcap_books and verse_num == 2:
                                line = fr'\par }}{{\PP \postdropcapindent\VS{{{verse_num}}}'
                            else:
                                line = fr'\par }}{{\PP \VS{{{verse_num}}}'
                        else:
                            line = fr'\VS{{{verse_num}}}'

                        tex_lines.append(build_line_text(line, words))

                        should_add_paragraph_marker = words[-1][1] if words else False
                else:
                    # Add blank line before new chapter
                    tex_lines.append('')
                    
                    should_add_paragraph_marker = False
                    for verse_num, words in verses.items():
                        if verse_num == 1:
                            line = r'\par }\Chap{' + str(chap_num) + r'}{\PP \VerseOne{1}'
                        elif should_add_paragraph_marker:
                            line = fr'\par }}{{\PP \VS{{{verse_num}}}'
                        else:
                            line = fr'\VS{{{verse_num}}}'

                        tex_lines.append(build_line_text(line, words))

                        should_add_paragraph_marker = words[-1][1] if words else False
        
        # Close final paragraph
        tex_lines.append(r'\par }')
        
        out_path = f'{output_folder}/{book_info["code"]}_src.tex'
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write('\n'.join(tex_lines))
        logging.info(f'Wrote book file: {out_path}')

def build_verse_text(words):
    verse_text = ''
    in_quote = False

    for i, (word, pm_next, poetry_quote_starts, in_poetry_block) in enumerate(words):
        if poetry_quote_starts:
            # in our data set, I never see a paragraph mark in immediately preceding a quote mark
            if i > 0:
                verse_text += '\n' # if first word in new verse, we should already be on a new line.
            verse_text += '\\par }{\\PP \\begin{quote}'
            in_quote = True

        verse_text += word

        # Poetry quote ends: next word starts poetry quote, or paragraph break, or end of verse
        next_word_starts_new_poetry_quote = (i + 1 < len(words)) and words[i + 1][2]
        if in_quote and (next_word_starts_new_poetry_quote or pm_next or i == len(words) - 1):
            verse_text += '\\end{quote}'
            in_quote = False

        if i != len(words) - 1 and pm_next:
            verse_text += '\n\\par }{\\PP '
        else:
            verse_text += ' '
    return verse_text

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
    parse_csv_and_generate_tex(csv_path, output_folder)