# `orf_finder_lib` — Module Reference

Detects Open Reading Frames (ORFs) across all six reading frames of a DNA sequence. Supports non-canonical start codons, nested ORF detection, and reverse-complement scanning.

```
src/orf_finder_lib/
├── frame_scanner.py   # Low-level sequence utilities and per-frame scanning
├── orf_finder.py      # orchestrates all six frames and builds output
└── output_writer.py   # Summary printing and CSV export
```

---

## `orf_finder.py` 

`find_orfs` returns a 2-tuple: a nested dict organised by canonical/non-canonical start codon, and a flat list of all ORF records. Each record contains `orf_id`, `strand`, `start_codon`, `frame`, `start`, `end`, `length_nt`, and `is_nested`.

`find_nested(flat_list)` returns the subset of ORFs fully contained within another ORF on the same strand and frame.

---


### Terminal summary (`print_summary`)

```
----------  ORF Summary — Sequence 1 ----------
  Total ORFs found            : 9
  Forward strand (+)          : 3
  Reverse strand (-)          : 6
  Canonical   (ATG)           : 9
  Nested ORFs detected        : 0
----------------------------------------------
```

### CSV output (`write_combined_csv`)

Each sequence block starts with the accession on its own row, followed by column headers and one row per ORF. In comparative mode the two blocks are separated by two blank rows. The `sequence (5'->3')` column always reads in the 5′→3′ direction regardless of strand.

```
NM_001301717
orf_id  strand  start_codon  frame  start  end   length_nt  sequence (5'->3')
ORF1    +       ATG          0      99     1218  1119       ATGAAAAGCGTGCTGGTGGTG...
ORF2    +       ATG          0      1287   1476  189        ATGACTCAGGACATCCCCCCG...
ORF3    -       ATG          1      1842   1935  93         ATGTCATCCCCACTCTGGAGC...
ORF4    +       ATG          2      1583   2183  600        ATGAACCTTCTGGCCTCCCAC...
ORF5    -       ATG          2      1013   1178  165        ATGGAGGAGCGCCGGATGTGC...
ORF6    -       ATG          2      914    998   84         ATGTTGAGTTGCTTACTGAGC...
ORF7    -       ATG          2      806    899   93         ATGAAGACCACGACCACAGCG...
ORF8    -       ATG          2      572    797   225        ATGGCCAGCAGGGGGACCAGA...
ORF9    -       ATG          2      200    284   84         ATGATGGAGTACATGATAGGG...
```
