# -*- coding: utf-8 -*-
"""
Created on Sun Feb 8 11:24:42 2014

@author: Cindy Sun

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from random import shuffle
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###

#all doctests conducted under assumption that argument is not a null entry

def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide

    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('G')
    'C'
    >>> get_complement('T')
    'A'
    """
    #added unit tests for nucleotides 'G' and 'T' to test for all possibilites since there are only 4

    if nucleotide == 'A':
        return 'T'
    if nucleotide == 'T':
        return 'A'
    if nucleotide == 'C':
        return 'G'
    if nucleotide == 'G':
        return 'C'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    >>> get_reverse_complement('')
    ''
    """

    #added a doctest for a null DNA entry

    dna = dna[::-1]
    reverse_complement = ''
    for letter in dna:
        reverse_complement += get_complement(letter)
    return reverse_complement

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("TGA")
    ''
    >>> rest_of_ORF("ATGAGA")
    'ATGAGA'
    """
    stop = ['TAG','TAA','TGA']
    for i in range(0, len(dna), 3):
        if dna[i:i+3] in stop:
            return dna[:i]
    else: 
        return dna

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG']
    """

    #added doctest to test for nested ORF 

    ORF = []
    for i in range(0, len(dna), 3):
        if dna[i:i+3] == 'ATG':
            dna = dna[i:]
            ORF.append(rest_of_ORF(dna))
            dna = dna[len(rest_of_ORF(dna)):]
    return ORF

    
def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    >>> find_all_ORFs("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG']
    """

    #added doctest to test to for nested ORF and in case of no start codon

    ORF = []
    for i in range(0, 3):
        ORF.extend(find_all_ORFs_oneframe(dna[i:]))
    return ORF


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """

    #did not add doctest since code is based on find_all_ORFs, which tested for nested ORF and no start codons

    ORF = []
    ORF.extend(find_all_ORFs(dna))
    ORF.extend(find_all_ORFs(get_reverse_complement(dna)))
    return ORF
    
def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """

    #doctest does not test for a null dna field, but assumes that the dna field will not be null 

    strand = []
    strand = find_all_ORFs_both_strands(dna)
    return max(strand) 

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random Shuffles
        returns: the maximum length longest ORF """

    #no doctest because return is based on a randomly shuffled sequence
    length = []
    for i in range(num_trials):
       dna = shuffle_string(dna)
       length.append(len(longest_ORF(dna)))

    return max(length)

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
        >>> coding_strand_to_AA("")
        ''
        >>> coding_strand_to_AA("ATGCTACATTCGCA")
        'MLHS'
    """

    #added doctest in case of no dna entry
    #second doctest tests for incomplete sequence

    aa_string = ''
    for i in range(0, len(dna), 3):
        if i < len(dna) - 2:
            aa_string += aa_table[dna[i:i+3]]
    return aa_string

def gene_finder(dna):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """

    #no doctest because code contains random shuffle
    threshold = longest_ORF_noncoding(dna, 1500)
    ORF = find_all_ORFs_both_strands(dna)
    aa_string = []
    for i in range(len(ORF)):
        if len(ORF[i]) > threshold:
            aa_string.append(coding_strand_to_AA(ORF[i]))
    return aa_string


dna = load_seq("./data/X73525.fa")
print gene_finder(dna)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
