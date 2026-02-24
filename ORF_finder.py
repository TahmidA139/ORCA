#!/usr/bin/env python3
"""
ORF_finder.py

Overall Purpose:
    Detect all open reading frames (ORFs) within a DNA sequence
    across multiple reading frames and collect metadata.
"""

from typing import List, Dict

START_CODON = "ATG"
STOP_CODONS = {"TAA", "TAG", "TGA"}

def _scan_frame(dna_sequence: str, frame: int) -> List[Dict]:
    """
    Scan a single reading frame for ORFs.

    Returns:
        List of dictionaries with frame, start, end.
    """
    orfs = []
    seq_len = len(dna_sequence)

    i = frame
    while i <= seq_len - 3:
        codon = dna_sequence[i:i + 3]

        if codon == START_CODON:
            start_index = i
            j = i + 3

            while j <= seq_len - 3:
                stop_codon = dna_sequence[j:j + 3]

                if stop_codon in STOP_CODONS:
                    orfs.append({
                        "frame": frame,
                        "start": start_index,
                        "end": j + 3
                    })
                    break

                j += 3

        i += 3

    return orfs


def find_orfs(dna_sequence: str) -> List[Dict]:
    """
    Identify ORFs across all three reading frames.

    Returns:
        List of dictionaries containing:
            - frame
            - start
            - end
    """
    dna_sequence = dna_sequence.upper()
    all_orfs = []

    for frame in range(3):
        frame_orfs = _scan_frame(dna_sequence, frame)
        all_orfs.extend(frame_orfs)

    return all_orfs


def orfs_metadata(dna_sequence: str) -> List[Dict]:
    """
    Add sequence and length metadata to each detected ORF.

    Returns:
        List of dictionaries containing:
            - frame
            - start
            - end
            - sequence
            - length
    """
    dna_sequence = dna_sequence.upper()
    orfs = find_orfs(dna_sequence)

    metadata = []

    for orf in orfs:
        start = orf["start"]
        end = orf["end"]
        sequence = dna_sequence[start:end]

        metadata.append({
            "frame": orf["frame"],
            "start": start,
            "end": end,
            "sequence": sequence,
            "length": len(sequence)})

    return metadata
