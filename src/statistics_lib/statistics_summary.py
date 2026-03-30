#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statistics_summary.py

Purpose:
    Generate summary statistics from ORF datasets for reporting.
    Includes GC content per ORF, codon usage, protein length,
    and overall dataset statistics.

Input:
    flat_list   : list of ORF dicts from ORF_finder.find_orfs()
    dna_sequence: original forward-strand DNA sequence string

Output:
    output/stats_summary.txt  : human-readable summary report
    output/orf_stats.csv      : per-ORF statistics table
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import numpy as np

ORF_STATS_FIELDNAMES: List[str] = [
    "orf_id",
    "strand",
    "frame",
    "start",
    "end",
    "length_nt",
    "protein_length_aa",
    "gc_content_pct",
    "status",
    "start_codon",
]

def _extract_sequence(orf: Dict[str, Any], dna_sequence: str) -> str:
    """
    Extract the nucleotide sequence of an ORF from the full DNA sequence.

    For '+' strand ORFs the slice is straightforward.
    For '-' strand ORFs the stored coordinates are in forward-strand space
    so we slice and reverse complement.

    Parameters
    ----------
    orf : dict
        A single ORF record from flat_list.
    dna_sequence : str
        The original full forward-strand DNA sequence (upper-case).

    Returns
    -------
    str
        Nucleotide sequence of the ORF.
    """
    start = orf["start"]
    end   = orf["end"] if orf["end"] is not None else len(dna_sequence)

    if orf["strand"] == "+":
        return dna_sequence[start:end]
    else:
        fwd_slice  = dna_sequence[start:end]
        char_arr   = np.array(list(fwd_slice), dtype="<U1")
        _comp      = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
        complement = np.vectorize(_comp.get)(char_arr, char_arr)
        return "".join(complement[::-1])


def _gc_content(sequence: str) -> float:
    """
    Calculate GC content of a sequence using NumPy boolean masking.

    Parameters
    ----------
    sequence : str
        Nucleotide sequence string.

    Returns
    -------
    float
        GC content as a percentage (0.0 - 100.0).
    """
    if not sequence:
        return 0.0
    arr = np.array(list(sequence), dtype="<U1")
    gc  = np.isin(arr, ["G", "C"]).sum()
    return round(float(gc / len(sequence) * 100), 2)


def _codon_usage(sequence: str) -> Dict[str, int]:
    """
    Count the occurrence of every codon in a nucleotide sequence using NumPy.

    Codons are extracted in-frame from position 0.
    The stop codon at the end of complete ORFs is included in the count.

    Parameters
    ----------
    sequence : str
        Nucleotide sequence string (should be a multiple of 3).

    Returns
    -------
    dict
        Mapping of codon string to count, sorted alphabetically.
    """
    n_codons = len(sequence) // 3
    if n_codons == 0:
        return {}

    char_arr    = np.array(list(sequence[: n_codons * 3]), dtype="<U1")
    codon_chars = char_arr.reshape(n_codons, 3)
    codons      = np.char.add(
        np.char.add(codon_chars[:, 0], codon_chars[:, 1]),
        codon_chars[:, 2],
    )

    unique, counts = np.unique(codons, return_counts=True)
    return dict(sorted(zip(unique.tolist(), counts.tolist())))


def _protein_length(length_nt: int, status: str) -> int:
    """
    Calculate protein length in amino acids from ORF nucleotide length.

    For complete ORFs the stop codon is subtracted (it is not translated).
    For incomplete ORFs the full length is used as an estimate.

    Parameters
    ----------
    length_nt : int
    status : str
        ORF status string (may contain '|nested').

    Returns
    -------
    int
        Estimated protein length in amino acids.
    """
    base_status = status.split("|")[0]
    if base_status == "complete":
        return max(0, (length_nt - 3) // 3)
    else:
        return length_nt // 3

def calculate_orf_stats(
    flat_list:    List[Dict[str, Any]],
    dna_sequence: str,
) -> List[Dict[str, Any]]:
    """
    Compute per-ORF statistics including GC content, codon usage,
    and protein length.

    Parameters
    ----------
    flat_list : list of dict
        ORF records from ORF_finder.find_orfs().
    dna_sequence : str
        Original forward-strand DNA sequence.

    Returns
    -------
    list of dict
        One record per ORF with added statistics fields.
    """
    results: List[Dict[str, Any]] = []

    for orf in flat_list:
        seq        = _extract_sequence(orf, dna_sequence)
        gc         = _gc_content(seq)
        codons     = _codon_usage(seq)
        prot_len   = _protein_length(orf["length_nt"], orf["status"])

        record = dict(orf)
        record["gc_content_pct"]     = gc
        record["protein_length_aa"]  = prot_len
        record["codon_usage"]        = codons
        results.append(record)

    return results


def write_stats_to_file(
    flat_list:    List[Dict[str, Any]],
    dna_sequence: str,
    accession:    str,
    outfile:      str = "output/stats_summary.txt",
) -> None:
    """
    Write a human-readable summary report to a text file.

    Includes:
        - Dataset-level counts (total, complete, incomplete, nested)
        - Genomic GC content
        - Longest ORF details
        - Per-ORF table with GC content, protein length, and codon usage

    Parameters
    ----------
    flat_list : list of dict
        ORF records from ORF_finder.find_orfs().
    dna_sequence : str
        Original forward-strand DNA sequence.
    accession : str
        NCBI accession number (for report header).
    outfile : str
        Path to write the summary report.
    """
    import os
    os.makedirs(os.path.dirname(outfile), exist_ok=True) if os.path.dirname(outfile) else None

    per_orf_stats = calculate_orf_stats(flat_list, dna_sequence)

    # Dataset-level stats
    total      = len(flat_list)
    complete   = sum(1 for o in flat_list if o["status"].split("|")[0] == "complete")
    incomplete = total - complete
    nested     = sum(1 for o in flat_list if "nested" in o["status"])
    plus       = sum(1 for o in flat_list if o["strand"] == "+")
    minus      = sum(1 for o in flat_list if o["strand"] == "-")

    # Longest ORF
    longest = max(flat_list, key=lambda o: o["length_nt"]) if flat_list else None

    # Genomic GC content
    genomic_gc = _gc_content(dna_sequence)

    with open(outfile, "w") as fh:
        fh.write("=" * 60 + "\n")
        fh.write(f"  ORF Statistics Summary\n")
        fh.write(f"  Accession : {accession}\n")
        fh.write(f"  Sequence length : {len(dna_sequence):,} nt\n")
        fh.write(f"  Genomic GC content : {genomic_gc}%\n")
        fh.write("=" * 60 + "\n\n")

        fh.write("--- Dataset Overview ---\n")
        fh.write(f"  Total ORFs found    : {total}\n")
        fh.write(f"  Complete ORFs       : {complete}\n")
        fh.write(f"  Incomplete ORFs     : {incomplete}\n")
        fh.write(f"  Nested ORFs         : {nested}\n")
        fh.write(f"  Forward strand (+)  : {plus}\n")
        fh.write(f"  Reverse strand (-)  : {minus}\n\n")

        if longest:
            prot_len = _protein_length(longest["length_nt"], longest["status"])
            fh.write("--- Longest ORF ---\n")
            fh.write(f"  ID          : {longest['orf_id']}\n")
            fh.write(f"  Strand      : {longest['strand']}\n")
            fh.write(f"  Frame       : {longest['frame']}\n")
            fh.write(f"  Location    : {longest['start']}..{longest['end']}\n")
            fh.write(f"  Span        : {longest['length_nt']} nt\n")
            fh.write(f"  Protein length : {prot_len} aa\n")
            fh.write(f"  Start codon : {longest['start_codon']}\n")
            fh.write(f"  Status      : {longest['status']}\n\n")

        fh.write("--- Per-ORF Statistics ---\n")
        fh.write(
            f"{'ORF ID':<20} {'Strand':>6} {'Frame':>5} "
            f"{'Start':>7} {'End':>7} {'Length(nt)':>10} "
            f"{'Protein(aa)':>11} {'GC%':>6}\n"
        )
        fh.write("-" * 80 + "\n")

        for rec in per_orf_stats:
            end_str = str(rec["end"]) if rec["end"] is not None else "N/A"
            fh.write(
                f"{rec['orf_id']:<20} {rec['strand']:>6} {rec['frame']:>5} "
                f"{rec['start']:>7} {end_str:>7} {rec['length_nt']:>10} "
                f"{rec['protein_length_aa']:>11} {rec['gc_content_pct']:>6}\n"
            )

        fh.write("\n--- Codon Usage Per ORF ---\n")
        for rec in per_orf_stats:
            fh.write(f"\n  {rec['orf_id']} ({rec['strand']} strand, frame {rec['frame']}):\n")
            codon_usage = rec["codon_usage"]
            # Print codons in rows of 8 for readability
            items = list(codon_usage.items())
            for idx in range(0, len(items), 8):
                row = items[idx: idx + 8]
                fh.write("    " + "  ".join(f"{c}:{n}" for c, n in row) + "\n")

    print(f"[INFO] Statistics report written to: {outfile}")

