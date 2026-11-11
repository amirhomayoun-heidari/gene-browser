## 2026-11-10 — Day 1: raw data
Annotation:  data/raw/V12_genomic.gtf
  genome-build GRCz12tu, GCF_049306965.2, NCBI RefSeq RS_2026_08
Assembly report:  data/raw/GCF_049306965.2_GRCz12tu_assembly_report.txt
  downloaded with (run inside data/raw):
  curl -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/049/306/965/GCF_049306965.2_GRCz12tu/GCF_049306965.2_GRCz12tu_assembly_report.txt






  # Notes

## 2026-11-10 — Day 1: raw data

### Files
Annotation:  data/raw/V12_genomic.gtf  (1.6 GB, not in Git)
  genome-build GRCz12tu, GCF_049306965.2, NCBI RefSeq RS_2026_08
  3,573,984 non-comment lines, all on 25 sequences (NC_133176.1 ... NC_133200.1)
Assembly report:  data/raw/GCF_049306965.2_GRCz12tu_assembly_report.txt  (3.4 KB)
  downloaded with (run inside data/raw):
  curl -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/049/306/965/GCF_049306965.2_GRCz12tu/GCF_049306965.2_GRCz12tu_assembly_report.txt

### Assembly report: what I found
Q1. Columns (tab-separated): short name = col 1, long name = col 7, length = col 9.
    Trap: col 8 "Primary Assembly" has a space but is ONE column -> always split on tabs.
Q2. GTF column 1 uses RefSeq accessions (NC_...). They match report col 7, not col 5.
Q3. Keep rows where col 2 == "assembled-molecule".
    The GTF has genes on exactly 25 sequences = chr1-chr25. No unplaced scaffolds, no MT.
    A row with no genes should not be in the browser's chromosome list.
Q4. Hidden characters at line ends: YES — every line ends with \r (Windows, shown as ^M by cat -e).
    Only touches the LAST column (col 10). Cols 1, 7, 9 are safe, but strip it anyway: tr -d '\r'

### Commands I learned today
git clone / status / add / commit / push / log --oneline / rm --cached
curl -O URL      download a file, keep its name
cat -e FILE      show hidden characters at line ends











## 2026-11-11 — Day 2: chromosome map

### Output
data/chrom_map.tsv  (25 rows: accession, short name, length; not in Git)

### Made with (run from repo root)
awk -F'\t' -v OFS='\t' '$2 == "assembled-molecule" {print $7, $1, $9}' data/raw/GCF_049306965.2_GRCz12tu_assembly_report.txt > data/chrom_map.tsv

Checks: wc -l = 25; columns = NC_... / chr1 / length; cat -e shows no ^M

### Why this command is enough
No grep -v '^#':  comment lines never have "assembled-molecule" in column 2,
                  so the condition already drops them.
No tr -d '\r':    \r sits only at the end of the LAST column (col 10).
                  I print cols 7, 1, 9, so it never reaches my output.
                  If I ever need the last column, add  tr -d '\r' |  before awk.

### Lesson: never edit raw files
I ran  perl -pi -e 's/\r$//'  on the raw report. -i rewrites the original file in place,
so my copy no longer matched a fresh download, and that step was written nowhere.
Fixed: deleted it and re-downloaded with the curl command from Day 1 (recipe works).
Rule: clean data on the way (in the pipeline), never at the source.
Red flag in data/raw: any tool with -i (perl -i, sed -i).