# make_genes.py — prepare gene data for the browser
# Run from the project folder:  python3 prep/make_genes.py

import json

# NEW: biotype -> display group (anything not listed becomes "other")
GROUPS = {
    "protein_coding": "protein_coding",
    "lncRNA": "lncRNA",
    "tRNA": "tRNA",
    "rRNA": "rRNA",
    "snRNA": "small_RNA",
    "miRNA": "small_RNA",
    "snoRNA": "small_RNA",
    "misc_RNA": "small_RNA",
    "SRP_RNA": "small_RNA",
    "ncRNA": "small_RNA",
    "RNase_P_RNA": "small_RNA",
    "RNase_MRP_RNA": "small_RNA",
    "antisense_RNA": "small_RNA",
    "pseudogene": "pseudogene",
    "transcribed_pseudogene": "pseudogene",
    "ncRNA_pseudogene": "pseudogene",
}

# ---------- Part B: read the chromosome map ----------
chrom_name = {}   # "NC_133176.1" -> "chr1"
chrom_size = {}   # "chr1" -> 63108402

for line in open("data/chrom_map.tsv"):
    acc, name, length = line.rstrip("\n").split("\t")
    chrom_name[acc] = name
    chrom_size[name] = int(length)

# ---------- Parts C, D, E: read the GTF, keep genes ----------
gene_count = 0
genes = []

for line in open("data/raw/V12_genomic.gtf"):
    if line.startswith("#"):
        continue
    cols = line.rstrip("\n").split("\t")
    if cols[2] == "gene":
        gene_count += 1

        # Part D: column 9 -> dictionary
        attrs = {}
        for part in cols[8].split(";"):
            part = part.strip()
            if " " not in part:
                continue
            key, value = part.split(" ", 1)
            attrs[key] = value.strip('"')

        # Part E: one gene = one dictionary with 8 fields
        gene = {
            "chrom": chrom_name[cols[0]],
            "start": int(cols[3]) - 1,
            "end": int(cols[4]),
            "name": attrs["gene"],
            "id": attrs["gene_id"],
            "biotype": attrs["gene_biotype"],
            "group": GROUPS.get(attrs["gene_biotype"], "other"),   # NEW
            "strand": cols[6],
        }
        genes.append(gene)

print("genes:", gene_count)
print("list length:", len(genes))
print(genes[0])

# ---------- Part F: write the outputs ----------
with open("data/genes.json", "w") as out:
    json.dump(genes, out)

with open("data/genes.tsv", "w") as out:
    out.write("chrom\tstart\tend\tname\tid\tbiotype\tgroup\tstrand\n")   # NEW: group column
    for g in genes:
        out.write(f"{g['chrom']}\t{g['start']}\t{g['end']}\t{g['name']}\t{g['id']}\t{g['biotype']}\t{g['group']}\t{g['strand']}\n")

with open("data/chrom.sizes", "w") as out:
    for name, size in chrom_size.items():
        out.write(f"{name}\t{size}\n")

print("wrote", len(genes), "genes")