# Brenton's Septuagint in Latex

This repository's purpose is to make Brenton's Septuagint available in print-ready format for free. If you do a search for printed Septuagint Bibles online, you will quickly find that they are very large and heavy and quite expensive. We want to change that! This edition is designed to be as compact as possible, and the price can't be beat. :) 

## Download
If you just want the most up to date version of the PDF file, click here to download it. [**Brenton LXX PDF**](https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/releases/latest/download/Brenton.pdf)

## Build Process
To build a complete bible from the start, there is a series of steps that you will want to go through.  Note that the outputs of most of these steps have been committed, so you can likely start from the last step, unless you make changes to a source document or a script.

1. Build the NT latex from the nt_data.  This step will transfor the text and markup from the xml-like format used in the source data into a base latex file for each book.
```
python generate_nt_latex.py
```

2. Concatenate both the NT and the OT.
```
python concat.py nt
python concat.py ot
```

3. Process and compile the OT and NT into a single finalized Latex file.  Note, if you would like to build just an OT or just a NT, you can leave out the arguments for the one you don't want, and the script will handle it. The `--color` switch is optional, if used will style the headers and chapter numbers with a nice deep red.
```
python process.py --ot concatenated-ot.tex --nt concatenated-nt.tex --output Bible.tex [--color]
```

4. Run Xelatex twice to build a pdf. The first time you run this command it will build the PDF with all of the text and pages in the right place, but it will not build the TOC.  You will need to run the same command again to build the TOC.
```
xelatex Bible.tex
xelatex Bible.tex
```

## Details
**Brenton.pdf**  
The main files in this repo are `Brenton.tex` and `Brenton.pdf`. If you want to print a book of your own, just download the latest release of [Brenton.pdf](https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/releases/latest/download/Brenton.pdf) and send it to your local print shop or your favorite self-publishing company. I have used [Snowfall Press](https://www.snowfallpress.com/) with good results. (Choose their lightest paper, "White, 40# / 13LB Bond" as that will help keep the size and weight of the book down.)

**Process.py**  
`Process.py` is the main worker. It takes the concatenated xetex files (see below) and transforms them into `Brenton.tex`, which is the source for `Brenton.pdf`. If you want to modify the PDF in any way, you'll need to modify `Brenton.tex` and then run it through LaTex to create a new PDF file. This repo uses LuaLaTex via [MikTex](https://miktex.org/).  

## Source and License
The digital Brenton LXX text is sourced from [ebible.org](https://ebible.org/Scriptures/details.php?id=grcbrent) and is in the public domain. (The exact source for the files in `grcbrent_xetex` is the [ebible XeTeX file](https://ebible.org/Scriptures/grcbrent_xetex.zip). You can use the script `concat.py` to merge each individual book into one file (concatenated.tex) as we did here.) All of the code and `.tex` formatting are licensed [CC0-1.0 (public domain)](https://github.com/mrgreekgeek/Brenton-LXX-Latex-print-project/blob/main/LICENSE) and may be used and copied freely. May God get all the glory! 

The New Testament is the [OpenGNT](https://opengnt.com/).  I obtained the source from EliranWong's GitHub repo for the project [here](https://github.com/eliranwong/OpenGNT). This
project aims to be an open source NA Equivelent NT edition. Open Greek New Testament Project by [Eliran Wong](https://marvel.bible/) is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
 
## Second Printing TODO: Jesse
- [ ] Prepare to print with Ingram Spark (allows 1200 pages with 50# paper in color and hardcover)
- [ ] Prepare to Printing B&W with Snowfall on 40# paper
  - [ ] Change all Red's to solid black
- [ ] Consider slightly wider page width 6" -> 6.5"?
- [ ] Fix some typos:
  - [ ] Gen 11:13: ἔξησε -> ἔζησε (in source)
  - [ ] Gen 11:17: ἔξησεν -> ἔζησεν (in source)
  - [ ] Gen 14:22: Κύπιον -> Κύριον (in source)

## First Printing TODO: Jesse
- [x] Add book names to the running header
- [x] Add chapter:verse references to the running header like most Bibles have 
- [x] Keep all Psalm headings with the following paragraphs
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
- [x] Page size (fit reader size)
- [x] If I ever change page size ΜΑΛΑΧΙΑΣ dropcap will probably Need to be reset in the source tex
- [x] Fetch and add NT
  - [x] Make sure things like John 8, Mark 16 etc show as I would expect
  - [x] Dropcaps to fix: 
      - ΚΑΤΑ ΜΑΘΘΑΙΟΝ
      - ΙΩΑΝΝΟΥ Γ
  - [x] Fix paragraphing
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
    - [x] Chapters starting in the middle of a paragraph:
        - USE this regex in intellij: `〔\d+｜(\d+)｜\d+〕(?!.*¶).*?\n.*?〔\d+｜(?!\1)`
        - [x] John 7:53-8:1 〔43｜8｜1〕
        - [x] 1 Corinthians 11:1 〔46｜11｜1〕
        - [x] 2 Cor 2:1 〔47｜2｜1〕
        - These two don't seem to want to work, because their placement would be in the larger left margin
        - [x] Col 4:1 〔51｜4｜1〕
        - [x] 1 Tim 3:1.  〔54｜3｜1〕 In NA 28, this verse is broken between paragraphs, but the first part of the verse is actually part of the last paragrah, and this is not typical for a new chapter to start mid-paragraph
    - [-] Kata markon 15:1, header verse reference is one verse behind. Low priority, this could change if anything shifts on the page.
  - [ ] Random stuff
    - [x] Special Characters: ΠΡΟΣ ΤΙΜΟΘΕΟΝ Β -  ἀλλὰ συνκακοπάθησον= τῷ εὐαγγελίῳ κατὰ δύναμιν Θεοῦ,
      - [x] '＋' means Greek word, which are not in original Berean Greek data, 3 words adapted from Byzantine text, 2 words adapted from BHP;
      - [x] '＊' means the main word is different from NA28;
      - [x] '＝' means the main word is identical to the corresponding word in NA28, with minor orthographical difference)
      - [-] any other special characters (do a regex find)
    - [x] Rev 1: ναί, ἀμήν.
- [x] Word out in margins.
  - [x] Heb 2:6, word doesn't split and goes into margin.  Try "διε\-μαρ\-τύ\-ρα\-το" or \setmainlanguage{greek}
  - [x] 1 Timothy ἀγαθοεργεῖν, πρεσβυτέρας
- [x] NT Page title
- [x] put together NT and OT with 1 TOC
- [-] compress TOC to one page?
- [x] Update chapter counters at the beginning of books.
- [x] Psalms formatting
  - [x] chapter margin not right because of centering
  - [-] line breaks in psalms (adds 100 pages, not worth it unless I can guarantee thin paper)
  - [x] add masoretic text ps numbers
  - [x] make sure counters are being updated correctly
  - [x] style psalm headings
- [x] Remove notation at the end of the doc
- [x] Add a Preface
- [-] Add front matter (copyright, editor, year, etc)
- [x] The spacing is slightly different between normal margin chapters and those that start in the middle of a paragraph (see colossians and 1 Tim 3/4)
- [x] Adjust to pt 9 font
  - [x] ΜΑΛΑΧΙΑΣ now needs post drop cap fix
  - [x] move title up page by like 1/4
- [x] (ΚΑΤΑ ΜΑΣΟΡΙΤΙΚΟΝ ) needs to be removed from psalm 151
- [x] extra 2 in Luke 18:4
- [x] make toc slightly larger in 8p font mode
- [x] verify 8 font
  - [x] Dropcaps
  - [x] Mid paragraph chapter starts
      * 1075-1071
  - [x] single page chapters
  - [x] chapter endings
  - [-] rev ch 2,3 first and second line spacing
- [x] Make John's  \vs{23}Ἔφη· start a new paragraph in source material
- [x] Empty Pages:
  - [x] end of isaiah
  - [x] end of acts
  - [x] end of hebrews
