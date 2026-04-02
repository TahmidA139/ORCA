# ORF Analysis Module

## Overview

This Python module provides tools for analyzing Open Reading Frames (ORFs). It focuses on identifying repeated ORFs and computing biologically meaningful statistics for each ORF, such as GC content and protein length.

The module is designed to integrate into the ORCA pipeline and supports downstream reporting and comparative analysis.

---

## Important Update on Similarity Scoring

The original implementation included pairwise similarity comparisons between every ORF. This approach was removed because:

* It scales poorly (O(n²) comparisons for large ORF sets)
* It is not biologically meaningful without proper alignment methods
* It introduces unnecessary computational overhead

Instead, similarity analysis is simplified:

* A similarity score can be computed **between two sequences only**
* This allows meaningful comparison between datasets without excessive computation

---

## Core Functions

### 1. `find_repeated_orfs(orfs)`

Identifies ORF sequences that appear more than once.

**Input:**

* `orfs` (list): A list of ORF dictionaries. Each ORF must include a `"sequence"` field.

**Output:**

* `dict`: Repeated ORF sequences and their counts

**Example:**

```python
orfs = [
    {"sequence": "ATGAAA"},
    {"sequence": "ATGAAA"},
    {"sequence": "ATGCCA"},
    {"sequence": "ATGAAA"}
]

print(find_repeated_orfs(orfs))
```

**Output:**

```
{'ATGAAA': 3}
```

---

### 2. `calculate_orf_stats(orfs, dna_sequence)`

Computes per-ORF statistics.

For each ORF, this function:

* Extracts the nucleotide sequence
* Calculates GC content
* Calculates protein length

**Input:**

* `orfs` (list): List of ORF dictionaries with `start`, `end`, and `strand`
* `dna_sequence` (str): Full DNA sequence

**Output:**

* Updated list of ORFs with:

  * `"sequence"`
  * `"gc_content"`
  * `"protein_length"`

---

### 3. `extract_sequence(dna, start, end, strand)`

Extracts the nucleotide sequence for an ORF.

* Handles both forward (`+`) and reverse (`-`) strands
* Reverse strand returns reverse complement

---

### 4. `gc_content(sequence)`

Calculates the percentage of G and C bases in a sequence.

**Output:**

* Float representing GC percentage

---

### 5. `protein_length(sequence)`

Calculates the number of amino acids produced by an ORF.

**Logic:**

* Length of sequence divided by 3 (codon size)

---

### 6. (Optional) `calculate_similarity(seq1, seq2)`

Computes similarity between **two sequences only**.

**How it works:**

* Compares matching positions
* Uses length of shorter sequence
* Returns value between 0.0 and 1.0

---

## Additional Stats Module (Separate File)

The following functions are implemented in the stats module:

### `write_stats_to_file`

Writes a summary report including:

* Total ORFs
* Average GC content
* Longest ORF
* Per-ORF table
* Codon usage

---

### `write_comparative_report`

Generates a human-readable comparison between two datasets.

---

### `write_comparative_csv`

Outputs a codon usage comparison table in CSV format for visualization.

---

## Features

* Detect repeated ORFs
* Compute GC content and protein length
* Extract sequences from forward and reverse strands
* Generate dataset-level and per-ORF statistics
* Support comparative analysis between two sequences

---

## Requirements

* Python 3.x

---

## Usage

Run as part of the ORCA pipeline:

```bash
python main.py --accession <ACCESSION> --email <YOUR_EMAIL>
```

---

## Notes

* ORFs must include `start`, `end`, and `strand` fields
* Sequence extraction assumes valid DNA input
* No sequence alignment is performed for similarity calculations
* Designed for integration with downstream reporting and visualization modules
