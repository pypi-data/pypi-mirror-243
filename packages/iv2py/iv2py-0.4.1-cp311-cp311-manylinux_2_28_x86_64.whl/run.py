import iv2py as iv
import os

# load index or create an index
if os.path.exists("file.fmindex"):
    # load fm index from disk
    index = iv.fmindex(path="file.fmindex")
else:
    # load fasta file - normalize sequences (e.g.: make everything capital letters, check for invalid characters)
    reference = [iv.normalize(rec.seq) for rec in iv.fasta.reader("file.fasta")]

    # build fmindex
    index = iv.fmindex(reference=reference, samplingRate=16)

    index.save("file.fmindex")

# search through fmindex
res = index.search("CG")
print(res)
