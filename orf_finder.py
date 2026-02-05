#!/usr/bin/env python3
Purpose: 
This script detects all open reading frames (ORFs) within a DNA sequence across multiple reading frames.
Input: 
The polished DNA sequence from input_validate.py script
Output: 
List of ORFs with positions and sequences.
High level steps:
  1.Define start and stop codons.
  2.Iterate through all three reading frames.
  3.Scan the sequence codon by codon.
  4.Detect start codons.
  5.Continue until a stop codon is found.
  6.Record ORF sequence and location.
  7.Return all detected ORFs.
