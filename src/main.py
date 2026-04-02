#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

from src.input_lib.input_validate import run as validate_run, validate_start_codons
from src.orf_finder_lib.orf_finder import find_orfs
from src.orf_finder_lib.output_writer import write_combined_csv, print_summary
from src.graphics_lib.graphics import plot_orf_map, plot_comparative_orf_map

# ✅ YOUR IMPORTS (TOP LEVEL)
from ORF_analysis import calculate_orf_stats, find_repeated_orfs
from orf_stats import write_stats_to_file, write_comparative_report, write_comparative_csv


# =========================================================
# 🔬 PROCESS ONE SEQUENCE 
# =========================================================
def _run_single_sequence(
    accession,
    email,
    start_codons,
    min_length,
    ignore_nested,
    summary_txt,
    label=""
):

    # 1. Fetch sequence
    acc, clean_seq = validate_run(accession, email)
    if clean_seq is None:
        print(f"[ERROR] Failed for accession '{accession}'")
        return None, None, None, None

    # 2. Find ORFs
    nested, flat_list = find_orfs(
        clean_seq,
        start_codons=start_codons,
        min_length=min_length,
        ignore_nested=ignore_nested,
    )

    print_summary(nested, flat_list, label=label or accession)

    if not flat_list:
        print(f"[WARNING] No ORFs found for '{accession}'")
        return acc, clean_seq, nested, flat_list

    # =====================================================
    #ANALYSIS PART
    # =====================================================
    flat_list = calculate_orf_stats(flat_list, clean_seq)

    repeats = find_repeated_orfs(flat_list)

    print("\n[ORCA] Repeated ORFs:")
    if repeats:
        for seq, count in repeats.items():
            print(f"{seq} → {count}")
    else:
        print("None found")

    # ✅ WRITE YOUR SUMMARY FILE
    write_stats_to_file(flat_list, filename=summary_txt)

    # =====================================================

    return acc, clean_seq, nested, flat_list

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--accession", type=str)
    parser.add_argument("--accession2", type=str, default=None)
    parser.add_argument("--email", type=str)
    parser.add_argument("--min-length", type=int, default=30)
    parser.add_argument("--start-codons", nargs="+", default=["ATG"])
    parser.add_argument("--ignore-nested", action="store_true")
    parser.add_argument("--output", type=str, default="output/orfs.csv")

    args = parser.parse_args()

    accession = args.accession or input("Enter accession: ").strip()
    accession2 = args.accession2
    email = args.email or input("Enter email: ").strip()

    comparative = accession2 is not None
    start_codons = validate_start_codons(args.start_codons)

    print(f"\n[ORCA] Processing sequence 1: {accession}")

    acc1, seq1, nested1, flat1 = _run_single_sequence(
        accession,
        email,
        start_codons,
        args.min_length,
        args.ignore_nested,
        summary_txt="output/stats_summary.txt",
        label="Sequence 1",
    )

    if acc1 is None:
        sys.exit(1)

    if comparative:
        print(f"\n[ORCA] Processing sequence 2: {accession2}")

        acc2, seq2, nested2, flat2 = _run_single_sequence(
            accession2,
            email,
            start_codons,
            args.min_length,
            args.ignore_nested,
            summary_txt="output/stats_summary_seq2.txt",
            label="Sequence 2",
        )

        if acc2 is None:
            sys.exit(1)
    else:
        acc2, seq2, flat2 = None, None, None

    write_combined_csv(
        acc1=acc1, flat1=flat1, seq1=seq1,
        output_path=args.output,
        acc2=acc2 if comparative else None,
        flat2=flat2 if comparative else None,
        seq2=seq2 if comparative else None,
    )

    if comparative:
        write_comparative_report(flat1, flat2, filename="output/comparison.txt")
        write_comparative_csv(flat1, flat2, filename="output/codon_comparison.csv")

    # -------------------------------
    # PLOTS (EXISTING)
    # -------------------------------
    if comparative:
        plot_comparative_orf_map(
            flat1=flat1, seq_len1=len(seq1), acc1=acc1,
            flat2=flat2, seq_len2=len(seq2), acc2=acc2,
            output_path="output/orf_map.png",
        )
    else:
        plot_orf_map(
            flat_list=flat1,
            seq_len=len(seq1),
            accession=acc1,
            output_path="output/orf_map.png",
        )

if __name__ == "__main__":
    main()
