# Brenton's Septuagint in Latex

This repository's purpose is to make Brenton's Septuagint available in print-ready format for free. If you do a search for printed Septuagint Bibles online, you will quickly find that they are very large and heavy and quite expensive. We want to change that! This edition is designed to be as compact as possible, and the price can't be beat. :) 

## Download
If you just want the most up to date version of the PDF file, click here to download it. [**Brenton LXX PDF**](https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/releases/latest/download/Brenton.pdf)

## Details
**Brenton.pdf**  
The main files in this repo are `Brenton.tex` and `Brenton.pdf`. If you want to print a book of your own, just download the latest release of [Brenton.pdf](https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/releases/latest/download/Brenton.pdf) and send it to your local print shop or your favorite self-publishing company. I have used [Snowfall Press](https://www.snowfallpress.com/) with good results. (Choose their lightest paper, "White, 40# / 13LB Bond" as that will help keep the size and weight of the book down.)

**Process.py**  
`Process.py` is the main worker. It takes the concatenated xetex files (see below) and transforms them into `Brenton.tex`, which is the source for `Brenton.pdf`. If you want to modify the PDF in any way, you'll need to modify `Brenton.tex` and then run it through LaTex to create a new PDF file. This repo uses LuaLaTex via [MikTex](https://miktex.org/).  

## Source and License
The digital Brenton LXX text is sourced from [ebible.org](https://ebible.org/Scriptures/details.php?id=grcbrent) and is in the public domain. (The exact source for the files in `grcbrent_xetex` is the [ebible XeTeX file](https://ebible.org/Scriptures/grcbrent_xetex.zip). You can use the script `concat.py` to merge each individual book into one file (concatenated.tex) as we did here.) All of the code and `.tex` formatting are licensed [CC0-1.0 (public domain)](https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/blob/main/LICENSE) and may be used and copied freely. May God get all the glory! 

## TODO 
- [x] Add book names to the running header
- [x] Add chapter:verse references to the running header like most Bibles have 
- [x] Keep all Psalm headings with the following paragraphs
- [ ] Add front matter (copyright, editor, year, etc)

## TODO: Jesse
- [x] fork repo
- [x] Single column
- [x] Drop Cap
  - [x] Make second line line up
  - Drop p2 down if a verse number would invate in the space. 2 Kings, ΙΩΗΛ, ΝΑΟΥΜ, ΑΜΒΑΚΟΥΜ, ΜΑΛΑΧΙΑΣ -- \hspace*{3em} seems to do the job
  - [x] Dropcap moved down line from chapter 1 number.  Align or remove ch 1 number
  - [x] Dropcap not on first line:
    - [x] ΘΡΗΝΟΙ ΙΕΡΕΜΙΟΥ - drop cap at 1st labeled verse, but probably want it on first real line
    - [x] ΣΟΦΙΑ ΣΕΙΡΑΧ - Maybe ΠΡΟΛΟΓΟΣ needs a different style
  - [x] No dropcap: 
    - [x] ΜΑΚΚΑΒΑΙΩΝ Γʹ
    - [x] ΕΣΘΗΡ - Has quotes from alternate text I guess
    - [x] ΨΑΛΜΟΙ - Probably don't want drop caps
- [x] Make verse numbers light grey
- [ ] Psalms formatting
  - [ ] chapter margin not right because of centering
  - [ ] line breaks in psalms
- [x] Page size (fit reader size)
- [x] If I ever change page size ΜΑΛΑΧΙΑΣ dropcap will probably Need to be reset in the source tex
- [ ] Fetch and add NT
  - [ ] Make sure things like John 8, Mark 16 etc show as I would expect
  - [x] Dropcaps to fix: 
      - ΚΑΤΑ ΜΑΘΘΑΙΟΝ
      - ΙΩΑΝΝΟΥ Γ
  - [ ] Fix paragraphing
    - [x] verse positioning.
    - [x] Weird breaks: \par }{\PP \postdropcapindent\VS{2}
        - ΚΑΤΑ ΛΟΥΚΑΝ 1:4
        - ΚΑΤΑ ΜΑΡΚΟΝ 1:3
    - [x] ¬ 
      - [x] basic functionality
      - [x] need to indent and stylize: signifies italicized or indented quotes, sometimes vs number before
      - [x] extra white space, in preamble controlling bottom, need to adjust.
      - [x] define poetry block in code
      - [x] remove: ¬ 
    - [x] Not breaking paragraphs in 1st verse of chapter
  - [ ] Random stuff
    - [ ] ΠΡΟΣ ΤΙΜΟΘΕΟΝ Β -  ἀλλὰ συνκακοπάθησον= τῷ εὐαγγελίῳ κατὰ δύναμιν Θεοῦ,
    - [ ] Rev 1: ναί, ἀμήν.
    - [ ] 1 Tim 3:1.  In NA 28, this verse is broken between paragraphs, but the first part of the verse is actually part of the last paragrah, and this is not typical for a new chapter to start mid-paragraph
    - [ ] Heb 2:6, word doesn't split and goes into margin.  Try "διε\-μαρ\-τύ\-ρα\-το" or \setmainlanguage{greek}
- [ ] Word out in margins.