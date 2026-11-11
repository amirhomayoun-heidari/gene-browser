chrom_name = {}   # long name  -> short name   e.g. "NC_133176.1" -> "chr1"
chrom_size = {}   # short name -> length       e.g. "chr1" -> 63108402

for line in open("data/chrom_map.tsv"):
    acc, name, length = line.rstrip("\n").split("\t")
    chrom_name[acc] = name
    chrom_size[name] = int(length)

print(len(chrom_name), len(chrom_size))
print(chrom_name["NC_133176.1"])
print(chrom_size["chr1"])

# ---------- Part C: count gene lines ----------
gene_count = 0

for line in open("data/raw/V12_genomic.gtf"):
    if line.startswith("#"):
        continue
    cols = line.rstrip("\n").split("\t")
    if cols[2] == "gene":
        gene_count += 1

print("genes:", gene_count)