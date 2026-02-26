#!/usr/bin/env python3

"""
Tahmid's portion:

"""
input_validate.py
-----------------
Fetches a DNA sequence from NCBI in FASTA format, validates it (removing
any invalid characters), and writes a cleaned FASTA file for downstream
modules (ORF_finder.py, ORF_analysis.py, statistics_summary.py).

Dependency:
    pip install biopython
"""

from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import re
import os

# NCBI requires a valid email address for all Entrez queries
Entrez.email = "your_email@example.com"   # <-- replace before running


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 1 — Fetch FASTA from NCBI
# ─────────────────────────────────────────────────────────────────────────────

def fetch_fasta_from_ncbi(accession: str, db: str = "nucleotide") -> str | None:
    """
    Objective:
        Download a DNA sequence in FASTA format from NCBI.

    Input:
        accession (str): NCBI nucleotide accession number
                         e.g. 'NM_001301717' or 'NC_000913.3'
        db (str):        Entrez database to query (default: 'nucleotide')

    Output:
        sequence (str):  Raw DNA sequence string retrieved from NCBI,
                         or None if the fetch fails.

    High-Level Steps:
        1. Query NCBI using the accession number via Entrez.efetch
        2. Retrieve and parse the FASTA record with SeqIO
        3. Extract and return the DNA sequence as a plain string
    """
    try:
        print(f"[INFO] Querying NCBI for accession: '{accession}' ...")
        # Step 1 & 2 — query NCBI and parse the FASTA response
        handle = Entrez.efetch(db=db, id=accession, rettype="fasta", retmode="text")
        record = SeqIO.read(handle, "fasta")
        handle.close()

        # Step 3 — extract the raw sequence string
        sequence = str(record.seq)
        print(f"[INFO] Fetched '{record.id}' — {len(sequence)} bp")
        return sequence

    except Exception as e:
        print(f"[ERROR] Could not fetch sequence from NCBI: {e}")
        return None

# ─────────────────────────────────────────────────────────────────────────────
# FUNCTION 2 — Validate (and clean) the DNA sequence
# ─────────────────────────────────────────────────────────────────────────────

