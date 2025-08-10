import sys
import os

ot_filenames = [
    "GEN_src.tex", "EXO_src.tex", "LEV_src.tex", "NUM_src.tex", "DEU_src.tex", "JOS_src.tex", "JDG_src.tex", "RUT_src.tex", "1SA_src.tex", "2SA_src.tex", "1KI_src.tex", "2KI_src.tex", "1CH_src.tex", "2CH_src.tex", "EZR_src.tex", "ESG_src.tex", "JOB_src.tex", "PSA_src.tex", "PRO_src.tex", "ECC_src.tex", "SNG_src.tex", "ISA_src.tex", "JER_src.tex", "LAM_src.tex", "EZK_src.tex", "DAG_src.tex", "HOS_src.tex", "JOL_src.tex", "AMO_src.tex", "OBA_src.tex", "JON_src.tex", "MIC_src.tex", "NAM_src.tex", "HAB_src.tex", "ZEP_src.tex", "HAG_src.tex", "ZEC_src.tex", "MAL_src.tex", "1ES_src.tex", "TOB_src.tex", "JDT_src.tex", "WIS_src.tex", "SIR_src.tex", "BAR_src.tex", "LJE_src.tex", "SUS_src.tex", "BEL_src.tex", "1MA_src.tex", "2MA_src.tex", "3MA_src.tex", "4MA_src.tex", "MAN_src.tex"
]

nt_filenames = [
    "MAT_src.tex", "MRK_src.tex", "LUK_src.tex", "JHN_src.tex", "ACT_src.tex", "ROM_src.tex", "1CO_src.tex", "2CO_src.tex", "GAL_src.tex", "EPH_src.tex", "PHP_src.tex", "COL_src.tex", "1TH_src.tex", "2TH_src.tex", "1TI_src.tex", "2TI_src.tex", "TIT_src.tex", "PHM_src.tex", "HEB_src.tex", "JAS_src.tex", "1PE_src.tex", "2PE_src.tex", "1JN_src.tex", "2JN_src.tex", "3JN_src.tex", "JUD_src.tex", "REV_src.tex"
]

def concatenate(files, src_dir, out_file):
    with open(out_file, 'w', encoding="utf-8") as outfile:
        for name in files:
            path = os.path.join(src_dir, name)
            with open(path, 'r', encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n")

if __name__ == "__main__":
    # Usage: python concat.py ot|nt
    if len(sys.argv) < 2:
        print("Usage: python concat.py ot|nt")
        sys.exit(1)
    mode = sys.argv[1].lower()
    if mode == "ot":
        concatenate(ot_filenames, "grcbrent_xetex", "concatenated-ot.tex")
        print("OT files concatenated to concatenated-ot.tex")
    elif mode == "nt":
        concatenate(nt_filenames, "ognt_xetex", "concatenated-nt.tex")
        print("NT files concatenated to concatenated-nt.tex")
    else:
        print("Unknown option. Use 'ot' or 'nt'.")
        sys.exit(1)