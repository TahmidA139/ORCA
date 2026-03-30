<p align="center">
  <img src="images/orca_banner.png" alt="ORCA Banner" width="350"/>
</p>

# ORCA (ORF Recognition and Comparative Annotator)

## Objective
ORCA is a command-line bioinformatics pipeline that automates ORF detection and analysis in DNA sequences. It helps researchers identify potential protein-coding regions, compare ORF structure across two species or transcripts, and generate detailed statistics for further study — all from a single NCBI accession number (or two, for comparative mode).

## Features
- Downloads DNA sequences in FASTA format directly from NCBI using an accession number
- Validates and cleans sequences before analysis
- Scans all six reading frames (+1, +2, +3, −1, −2, −3) using NumPy vectorization
- Detects canonical (ATG) and non-canonical (GTG, TTG) start codons
- Separates complete vs incomplete ORFs and flags nested ORFs
- Computes per-ORF statistics: GC content, codon usage, and protein length
- **Comparative mode** (`--accession2`): side-by-side ORF structure comparison, codon usage differences, and shared start-site analysis between two sequences
- Writes all results to the `output/` folder as CSV and plain-text reports

## Project Structure

```
ORCA/
├── README.md
├── LICENSE
├── environment.yml
├── src/
│   ├── __init__.py
│   ├── main.py                        # Pipeline driver; handles CLI args and output
│   │
│   ├── input_lib/                     # Tahmid Anwar
│   │   ├── __init__.py
│   │   └── input_validate.py          # Fetches from NCBI, validates, writes cleaned FASTA
│   │
│   ├── orf_finder_lib/                # Erin Nicole Decocker
│   │   ├── __init__.py
│   │   └── orf_finder.py              # Six-frame ORF detection with NumPy vectorization
│   │
│   ├── analysis_lib/                  # Amanda Yaworsky
│   │   ├── __init__.py
│   │   └── orf_analysis.py            # All calculations: per-ORF stats, repeated ORFs,
│   │                                  # comparative analysis between two sequences
│   │
│   └── statistics_lib/
│       ├── __init__.py
│       └── statistics_summary.py      # File writing only: imports results from
│                                      # orf_analysis.py and writes reports/CSVs
│
└── examples/
    ├── example_output.fasta
    └── example_run.txt
```

### File Descriptions

**`main.py`** — Pipeline driver. Parses CLI arguments, calls all modules in order, and coordinates single-sequence and comparative output.

**`input_validate.py`** — Fetches a FASTA file from NCBI using an accession number, removes the header, validates the sequence against the IUPAC nucleotide alphabet, and writes a cleaned FASTA to disk.

**`orf_finder.py`** — Detects ORFs across all six reading frames using NumPy-vectorized codon extraction. Supports canonical and non-canonical start codons, nested ORF detection, and configurable minimum length filtering.

**`orf_analysis.py`** — Owns all computation in the pipeline:
- Extracts ORF nucleotide sequences from the full DNA string
- Calculates GC content and codon usage per ORF (NumPy)
- Estimates protein length in amino acids
- Enriches the flat ORF list with these statistics (`calculate_orf_stats`)
- Finds repeated ORF sequences within a single dataset (`find_repeated_orfs`)
- Compares two ORF datasets for structure, codon usage differences, and shared start sites (`compare_orf_sets`)

**`statistics_summary.py`** — File writing only. Imports all computed results from `orf_analysis.py` and writes them to:
- `output/stats_summary.txt` — human-readable single-sequence report
- `output/orf_stats.csv` — per-ORF statistics table
- `output/comparative_report.txt` — side-by-side comparative report (comparative mode)
- `output/comparative_stats.csv` — codon-usage delta table (comparative mode)

## Output Files

| File | Mode | Description |
|------|------|-------------|
| `output/orfs.csv` | Both | Flat ORF table for sequence 1 |
| `output/orf_stats.csv` | Both | Per-ORF stats for sequence 1 |
| `output/stats_summary.txt` | Both | Human-readable summary for sequence 1 |
| `output/orfs_seq2.csv` | Comparative | Flat ORF table for sequence 2 |
| `output/orf_stats_seq2.csv` | Comparative | Per-ORF stats for sequence 2 |
| `output/stats_summary_seq2.txt` | Comparative | Human-readable summary for sequence 2 |
| `output/comparative_report.txt` | Comparative | Side-by-side comparison of both sequences |
| `output/comparative_stats.csv` | Comparative | Codon usage delta table (seq1 − seq2) |

## Installation

### Dependency Requirements
- Python 3.10
- numpy
- Biopython

### Setup

1. Clone the repository:
```bash
git clone https://github.com/TahmidA139/ORCA.git
```

2. Go into the project folder:
```bash
cd ORCA
```

3. Create the environment:
```bash
conda env create -f environment.yml
```

4. Activate the environment:
```bash
conda activate ORCA
```

## Usage

### Command-Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--accession` | Yes | — | NCBI accession number for sequence 1 |
| `--accession2` | No | — | NCBI accession number for sequence 2 (enables comparative mode) |
| `--email` | Yes | — | Your email address (required by NCBI Entrez) |
| `--start-codons` | No | `ATG` | One or more start codons: `ATG`, `GTG`, `TTG` |
| `--min-length` | No | `30` | Minimum ORF length in nucleotides |
| `--ignore-nested` | No | `False` | Exclude ORFs nested inside another ORF in the same frame |
| `--output` | No | `output/orfs.csv` | Path for the primary ORF output CSV |

### Usage Examples

Single sequence — all defaults (ATG only, min 30 nt, nested ORFs included):
```bash
python main.py --accession NM_001301717 --email you@example.com
```

Single sequence — all three start codons, minimum 60 nt, no nested ORFs:
```bash
python main.py --accession NM_001301717 --email you@example.com \
    --start-codons ATG GTG TTG --min-length 60 --ignore-nested
```

Comparative mode — two accessions side by side:
```bash
python main.py --accession NM_001301717 --accession2 NM_001256799 \
    --email you@example.com
```

## Algorithm Description

### Input Validation (`input_validate.py`)
The accession number is passed to NCBI's Entrez API via `Biopython`. The returned FASTA file is parsed with `SeqIO`, the header is stripped, and the raw sequence is validated against the IUPAC nucleotide alphabet. Invalid characters are removed and the cleaned sequence is written to `output/cleaned_sequence.fasta` before being passed to the ORF finder.

### ORF Detection (`orf_finder.py`)
The sequence is scanned in all six reading frames using NumPy-vectorized codon arrays. For each frame, every start codon position is identified with a boolean mask and paired with the next downstream stop codon. ORFs below the minimum length threshold are discarded. The reverse complement strand is generated with a vectorized complement lookup and scanned with the same logic. Coordinates on the reverse strand are converted back to forward-strand positions. Each ORF is then checked for nesting (whether its start falls inside another ORF on the same strand and frame).

### ORF Analysis (`orf_analysis.py`)
For each detected ORF, the nucleotide sequence is extracted from the full DNA string (with reverse complement handling for minus-strand ORFs). GC content is computed with NumPy boolean masking, codon usage is counted with `np.unique`, and protein length is estimated from the nucleotide length. In comparative mode, two enriched ORF datasets are compared for counts by category, reading-frame distribution, length statistics, mean GC per ORF, top codons, codon usage differences (delta = seq1 − seq2), and shared vs unique ORF start positions.

### Statistics Output (`statistics_summary.py`)
Receives all computed results from `orf_analysis.py` and writes them to disk. No calculations are performed here.

## References

- NCBI Entrez API: https://www.ncbi.nlm.nih.gov/books/NBK25499/
- Biopython: https://biopython.org/
- NumPy: https://numpy.org/

## License
This project is licensed under the GNU GPL v2.1. Chosen for open collaboration, ease of edits, and public use.

## Authors

**Amanda Yaworsky**
- Student ID: 801489950
- Email: ayaworsk@charlotte.edu

**Erin Nicole Decocker**
- Student ID: 801442694
- Email: edecocke@charlotte.edu

**Tahmid Anwar**
- Student ID: 801501080
- Email: tanwar@charlotte.edu
