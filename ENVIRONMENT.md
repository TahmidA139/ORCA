# Setting up the environment

## About `environment.yml`

The file `environment.yml` was created by running:

```bash
conda activate ORCA
conda env export --from-history > environment.yml
```

The `--from-history` flag tells conda to record only the packages that were explicitly installed (rather than every sub-dependency resolved during installation). This makes the file portable across operating systems: conda will resolve the correct platform-specific dependencies when the environment is recreated on a different machine.

The environment was originally created with:

```bash
conda create -n ORCA python=3.10 matplotlib numpy -y
```

## Creating the environment from `environment.yml`

From the project's root directory, run:

```bash
conda env create -f environment.yml
conda activate ORCA
```

This will install Python 3.10 along with matplotlib and numpy. The standard library modules used by the project (argparse, csv, os, sys) do not require separate installation.

## Running the program

With the environment activated, run the pipeline from the project's root directory.

**Single-sequence mode** (NCBI accession):

```bash
python -m src.main \
    --accession NM_012367.1 \
    --email your@email.com
```

**Single-sequence mode** (local FASTA file):

```bash
python -m src.main \
    --fasta example_input_files/OR2B6_sequence.fasta \
    --email your@email.com
```

**Comparative mode** (two local FASTA files):

```bash
python -m src.main \
    --fasta  example_input_files/OR2B6_sequence.fasta \
    --fasta2 example_input_files/IUPAC_ambiguity_test.fasta \
    --email  your@email.com
```

### Arguments

| Flag | Required | Description |
|------|----------|-------------|
| `--accession` | See note | NCBI accession number for sequence 1. Cannot be used with `--fasta`. |
| `--fasta` | See note | Path to a local FASTA file for sequence 1. Must contain exactly one sequence. Cannot be used with `--accession`. |
| `--accession2` | No | NCBI accession number for sequence 2. Enables comparative mode. |
| `--fasta2` | No | Path to a local FASTA file for sequence 2. Enables comparative mode. Cannot be used with `--accession2`. |
| `--email` | Yes | Email address required by NCBI Entrez. Not used when loading from local files, but must still be supplied to avoid an interactive prompt. |
| `--min-length` | No | Minimum ORF length in nucleotides (default: 30). |
| `--start-codons` | No | One or more start codons to search for (default: `ATG`). Non-canonical alternatives: `GTG`, `TTG`. |
| `--output` | No | Path for the primary ORF output CSV (default: `output/orfs.csv`). |

**Note:** exactly one of `--accession` or `--fasta` must be provided for sequence 1.

## Expected output

All output files are written to the `output/` directory in the project root.

### Single-sequence mode

| File | Description |
|------|-------------|
| `output/orfs.csv` | One row per ORF: strand, frame, start, end, length, start codon, and GC content. |
| `output/cleaned_sequence.fasta` | The input sequence after validation and cleaning. |
| `output/orf_map.png` | ORF map showing all ORFs across all six reading frames. |
| `output/orf_summary.txt` | Human-readable summary of ORF statistics. |

### Comparative mode (additional files)

| File | Description |
|------|-------------|
| `output/orfs_seq2.csv` | ORF table for sequence 2. |
| `output/cleaned_sequences.fasta` | Both cleaned sequences combined in a single FASTA file. |
| `output/orf_map.png` | Side-by-side comparative ORF map for both sequences. |
| `output/codon_usage_comparison.png` | RSCU codon-usage heatmap comparing the two sequences. |
| `output/orf_summary_seq2.txt` | ORF statistics summary for sequence 2. |

When run on `OR2B6_sequence.fasta` with default settings, the terminal output should look like this:

```
[ORCA] Processing sequence 1: (local file) example_input_files/OR2B6_sequence.fasta

--- ORF Summary: NM_012367.1 ---
Total ORFs found: ...
  [INFO] ORF map saved to: output/orf_map.png
```
