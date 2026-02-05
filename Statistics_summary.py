#Maybe putting in this file:
#Total number of ORFs with (maybe) start and stop position 
#Number of repeated ORFs (potential gene duplications)
#Longest ORF
#Any other stats??
#!/usr/bin/env python3
#!/usr/bin/env python3
"""
statistics_summary.py

Overall File Purpose:
    Generate summary statistics from analyzed ORF data to support
    biological interpretation and reporting.
"""

def count_total_orfs(orf_list):
    """
    Purpose:
        Determine the total number of ORFs identified in the dataset.

    Input:
        orf_list (list):
   
    Output:
        An integer representing the total number of ORFs detected.

    High-level steps:
        1. Receive a list of ORFs.
        2. Count the number of entries in the list.

        3. Return the total ORF count.
    """
    pass

def count_repeated_orfs(flagged_orfs):
    """
    Purpose:
        Count the number of ORFs that are repeated or flagged as
        potential gene duplications based on similarity analysis.

    Input:
        flagged_orfs (list):

    Output:
        An integer representing the number of repeated ORFs.

    High-level steps:
        1. Receive a list of flagged ORFs or duplication records.
        2. Identify unique ORFs involved in duplication events.
        3. Count the number of repeated ORFs.
        4. Return the duplication count.
    """
    pass

def find_longest_orf(orf_list):
    """
    Purpose:
        Identify the longest ORF in the dataset based on sequence length
        or genomic span.

    Input:
        orf_list (list)

    Output:
        The ORF record corresponds to the longest ORF identified.

    High-level steps:
        1. Receive a list of ORFs and determine the length of each ORF.
        3. Compare ORF lengths.
        4. Identify the longest ORF.
        5. Return the longest ORF record.
    """
    pass
  def summarize_orf_statistics(orf_list, flagged_orfs):
    """
    Purpose:
        Aggregate ORF-related stats into a single file for reporting or downstream analysis.

    Input:
        orf_list (list) and flagged_orfs (list)

    Output:
        A structured summary file containing key ORF
        statistics such as total ORFs, repeated ORFs, and longest ORF.

    High-level steps:
        1. Call count_total_orfs(), count_repeated_orfs(), and find_longest_orf()        
        4. Combine all stats into one file.
    """
    pass

