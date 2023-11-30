# JBioSeqTools - python library

#### JBioSeqTools is the Python library for gene sequence downloading, optimization, structure prediction, vector building, and visualization


<p align="right">
<img  src="https://github.com/jkubis96/GEDSpy/blob/main/fig/logo_jbs.PNG?raw=true" alt="drawing" width="250" />
</p>


### Author: Jakub Kubiś 

<div align="left">
 Institute of Bioorganic Chemistry<br />
 Polish Academy of Sciences<br />
 Department of Molecular Neurobiology<br />
</div>


## Description


<div align="justify"> 'JBioSeqTools is the Python library for biological sequence optimization (GC % content & codon frequency), restriction places removal, DNA/RNA structure prediction, and RNAi selection. It also allows the building of many plasmid vectors with the possibility of choosing sequences such as transcript, promoter, enhancer, molecular fluorescent tag, etc. Finally, the user obtains a ready-for-order construct with a whole sequence and visualization. Package description  on https://github.com/jkubis96/JBioSeqTools'
 </div>

</br>

Used databases:
* GeneScript [https://www.genscript.com/?src=google&gclid=Cj0KCQiAkMGcBhCSARIsAIW6d0CGxHmZO8EAYVQSwgk5e3YSRhKZ882vnylGUxfWuhareHFkJP4h4rgaAvTNEALw_wcB]
* VectorBuilder [https://en.vectorbuilder.com/]
* UTRdb [https://utrdb.cloud.ba.infn.it/utrdb/index_107.html]
* NCBI refseq_select_rna [ftp.ncbi.nlm.nih.gov]



# Installation

#### In command line write:

```
pip install JBioSeqTools
```

** During the first library loading additional requirements will be installed (BLAST, MUSCLE) and metadata downloaded.

# Usage

<br />

## 1. seq_tools - part of the library containing sequence optimization, structure prediction, and visualization

#### 1.1. Import part of  library

```
from jbst import seq_tools as st
```

<br />

#### 1.2. Loading metadata

```
metadata = st.load_metadata() 
```


<br />

#### 1.3. Downloading reference sequences with gene name
```
data_dict = st.get_sequences_gene(gene_name, species = 'human', max_results = 20)
```

<br />

#### 1.4. Downloading  sequences with accession numbers
```
data_dict = st.get_sequences_accesion(accesion_list)
```

<br />

#### 1.5. Creating FASTA format *.FASTA 

```
fasta_string = st.generate_fasta_string(data_dict)
```


<br />

#### 1.6. Loading FASTA format *.FASTA 

```
fasta_string = st.generate_fasta_string(data_dict)
```

<br />

#### 1.7. Writing to FASTA format *.FASTA 

```
st.write_fasta(fasta_string, path = None, name = 'fasta_file')
```


<br />

#### 1.8. Conducting Multiple Alignments Analysis (MUSCLE) form FASTA

```
alignment_file = st.MuscleMultipleSequenceAlignment(fasta_string, output = None, gapopen = 10, gapextend = 0.5)
```


<br />

#### 1.9. Display alignment plot

```
alignment_plot = st.DisplayAlignment(alignment_file, color_scheme="Taylor", wrap_length=80, show_grid=True, show_consensus=True)
alignment_plot.savefig("alignment_plot.svg")
```

** example alignment graph:

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>




<br />

#### 1.10. Decoding alignment file

```
decoded_alignment_file = st.decode_alignments(alignment_file)
```


<br />

#### 1.11. Writing to ALIGN format *.ALIGN 

```
st.write_alignments(decoded_alignment_file, path = None, name = 'alignments_file')
```


<br />

#### 1.12. Extracting consensus parts of alignments

```
consensuse = st.ExtractConsensuse(alignment_file, refseq_sequences = None)
```



<br />

#### 1.13. Passing sequence from an external source

```
sequence = st.load_sequence()
```



<br />

#### 1.14. Clearing junk characters from the sequence

```
sequence = st.clear_sequence(sequence)
```


<br />

#### 1.15. Checking that the sequence is coding protein (CDS)

```
dec_coding = st.check_coding(sequence)
```


<br />

#### 1.16. Checking that all bases in sequence are contained in the UPAC code

```
dec_upac = st.check_upac(sequence)
```


<br />

#### 1.17. Reversing the DNA / RNA sequence: 5' --> 3' and 3' --> 5'

```
reversed_sequence = st.reverse(sequence) 
```


<br />

#### 1.18. Complementing the DNA / RNA second strand sequence

```
complementary_sequence = st.complement(sequence)
```

<br />

#### 1.19. Changing DNA to RNA sequence

```
rna_sequence = st.dna_to_rna(sequence, enrichment= False)
```

<br />

#### 1.20. Changing RNA to DNA sequence

```
dna_sequence = st.rna_to_dna(rna_sequence)
```

<br />

#### 1.21. Changing DNA or RNA sequence to amino acid / protein sequence

```
protein_sequence = st.seuqence_to_protein(dna_sequence, metadata)
```


<br />

#### 1.21. Changing DNA or RNA sequence to amino acid / protein sequence

```
protein_sequence = st.seuqence_to_protein(dna_sequence, metadata)
```


<br />

#### 1.22. Prediction of RNA / DNA sequence secondary structure

```
predisted_structure, dot_structure1 = st.predict_structure(sequence, show_plot = True)
predisted_structure.savefig('predicted_structure.svg')

```

** example prediction graph:

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>



<br />

#### 1.23. Prediction of RNAi on the sequence

```
RNAi_data =  st.FindRNAi(sequence, metadata, length = 23, n = 200, max_repeat_len = 3, max_off = 1, species = 'human', output = None, database_name = "refseq_select_rna",  evalue = 1e-3, outfmt =  5, word_size = 7, max_hsps = 20, reward = 1, penalty = -3, gapopen = 5, gapextend = 2, dust = "no", extension = 'xml')    
```

<br />


#### 1.24. Correcting of RNAi_data for complementarity to the loop sequence

```
RNAi_data = st.loop_complementary_adjustment(RNAi_data, loop_seq, min_length=3)
```


<br />


#### 1.25. Correcting of RNAi_data for complementarity to the additional external sequence

```
RNAi_data = st.remove_specific_to_sequence(RNAi_data, sequence, min_length=4)
```


<br />


#### 1.26. Prediction of RNAi on the sequence

```
RNAi_data = st.loop_complementary_adjustment(RNAi_data, loop_seq, min_length=3)
```


<br />


#### 1.27. Codon optimization

```
optimized_data = st.codon_otymization(sequence, metadata, species = 'human')
```



<br />


#### 1.27. Codon optimization

```
optimized_data = st.codon_otymization(sequence, metadata, species = 'human')
```




<br />


#### 1.28. Checking susceptibility to restriction enzymes

```
all_restriction_places, reduced_restriction_places_with_indexes = st.check_restriction(sequence, metadata)
```



<br />


#### 1.29. Checking and removing susceptibility to restriction enzymes 

```
repaired_sequence_data = st.sequence_restriction_removal(sequence, metadata, restriction_places = [], species = 'human')
```

<br />

## 2. vector_build - part of the library containing building plasmid vectors with optimization elements from seq_tools

#### 2.1. Import part of  library

```
from jbst import vector_build as vb
```
<br />


#### 2.2. Creating vector plasmid:


```
project = vb.vector_create_on_dict(metadata, input_dict, show_plot=True)
```


<br />


#### 2.2.1 Creating expression of the plasmid vector

** Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':''
    
    # REQUIRED!
    # avaiable of vector types (ssAAV / scAAV / lentiviral / regular)
    'vector_type':'',
    
    # REQUIRED!
    # in this case 'vector_function':'expression'
    'vector_function':'expression',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (mouse + rat) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # list of coding sequences (CDS) provided to make expression from the vector
    # the CSD sequences the user can obtain from ...
    # amount of sequences is not restricted as the user must remember that the length of whole vector is limited
    # excide the relevant vector size can decrease vector working
    # if the user wants to not include any sequences only fluorescent_tag, provide ['']
    # sequences orientation 5' ---> 3' - sense
    'sequences':[''],
    # list of names of coding sequences
    # amount of names should be equal with amount of sequences
    # if provided no sequences, provide ['']
    'sequences_names':[''],
    
    # REQUIRED!
    # sequence of provided promoter
    # name and sequence the user can take from metadata['promoters'] (load_metadata())
    # for coding sequences the user should choose the promoter of coding genes (metadata['promoters']['type'] == 'coding')
    # sequence orientation 5' ---> 3' - sense
    'promoter_sequence':'',
    # REQUIRED!
    # name of provided promoter sequence
    'promoter_name':'',
    
    # POSSIBLE!
    # sequence of provided enhancer
    # name and sequence the user can take from metadata['regulators'] (load_metadata())
    # sequence orientation 5' ---> 3' - sense
    'regulator_sequence':'',
    # POSSIBLE!
    # name of provided enhancer sequence
    'regulator_name':'',
    
    # REQUIRED!
    # sequence of provided polyA signal
    # name and sequence the user can take from metadata['polya_seq'] (load_metadata())
    'polya_sequence':'',
    # REQUIRED!
    # name of provided polyA signal sequence
    'polya_name':'',
    
    
    # REQUIRED if more than one sequence of transcripts!
    # sequences of provided linkers
    # number of linkers_sequences should be equal number of sequences (transcripts) - 1. One linker for each pair of sequences.
    # name and sequence the user can take from metadata['linkers'] (load_metadata())
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    # sequence orientation 5' ---> 3' - sense
    'linkers_sequences':[''],
    # REQUIRED if more than one sequence!
    # names of provided linkers
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_names':[''],
    
    # POSSIBLE!
    # sequence of provided fluorescent tag
    # name and sequence the user can take from metadata['fluorescent_tag'] (load_metadata())
    # if the user does not need fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_sequence':'',
    # POSSIBLE!
    # name of provided fluorescent tag
    # if the user does not need fluorescent tag, provide ''
    'fluorescence_name':'',
    
    # WARNING! If the user wants to use an additional promoter for the fluorescent tag expression, provide data for fluorescence_promoter_sequence & fluorescence_polya_sequence!
    
    # POSSIBLE!
    # sequence of provided fluorescence promoter
    # name and sequence the user can take from metadata['promoters'] (load_metadata())
    # if the user does not need additional promoter for fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_promoter_sequence':'',
    # POSSIBLE!
    # name of provided fluorescence promoter
    # if the user does not need additional promoter for fluorescent tag, provide ''
    'fluorescence_promoter_name':'',
    
    # POSSIBLE!
    # sequence of provided fluorescence polyA signal
    # name and sequence the user can take from metadata['polya_seq'] (load_metadata())
    # if the user does not need additional promoter for fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_polya_sequence':'',
    # POSSIBLE!
    # name of provided fluorescence polyA signal
    # if the user does not need additional promoter for fluorescent tag, provide ''
    'fluorescence_polya_name':'',
    
    
    # WARNING! If provided sequences for transcripts (> 0) and do not need additional promoter for fluorescent tag, provide fluorescence_linker_sequence
    
    # POSSIBLE!
    # sequence of provided fluorescence tag linker
    # name and sequence the user can take from metadata['linkers'] (load_metadata())
    # if the user has provided additional promoter, so the fluorescence_linker_sequence is not needed, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_linker_sequence':'',
    # POSSIBLE!
    # name of provided fluorescence tag linker
    # if the user has provided additional promoter, so the fluorescence_linker_sequence is not needed, provide ''
    'fluorescence_linker_name':'',
    
    # REQUIRED!
    # sequence of provided selection marker
    # name and sequence the user can take from metadata['selection_markers'] (load_metadata())
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':'',
    
    # POSSIBLE!
    # restriction enzymes protection of transcript sequences
    # enzymes the user can take from metadata['restriction'] (load_metadata())
    # if do not need any restriction places protection, provide an empty list []
    'restriction_list':[],
    
    # REQUIRED!
    # available options (True / False)
    # decision; if the user wants the transcription sequences optimized based on the provided species
    'optimize':True
}

```


<br />


** Example dictionary:

```

input_dict = {
    
    'project_name':'test_expression',
    'vector_type':'ssAAV',
    'vector_function':'expression',
    'species':'human',
    'sequences':['ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA',
                 'ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA'],
    'sequences_names':['SMN1','SMN2'],
    'promoter_sequence':'GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT',
    'promoter_name':'TBG',
    'regulator_sequence':'CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG',
    'regulator_name':'WPRE',
    'polya_sequence':'CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA',
    'polya_name':'SV40_late',
    'linkers_sequences':['GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC'],
    'linkers_names':['T2A'],
    'fluorescence_sequence':'ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA',
    'fluorescence_name':'EGFP',
    'fluorescence_promoter_sequence':'CTCGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTCGAGGTGAGCCCCACGTTCTGCTTCACTCTCCCCATCTCCCCCCCCTCCCCACCCCCAATTTTGTATTTATTTATTTTTTAATTATTTTGTGCAGCGATGGGGGCGGGGGGGGGGGGGGGGCGCGCGCCAGGCGGGGCGGGGCGGGGCGAGGGGCGGGGCGGGGCGAGGCGGAGAGGTGCGGCGGCAGCCAATCAGAGCGGCGCGCTCCGAAAGTTTCCTTTTATGGCGAGGCGGCGGCGGCGGCGGCCCTATAAAAAGCGAAGCGCGCGGCGGGCGGGAGTCGCTGCGCGCTGCCTTCGCCCCGTGCCCCGCTCCGCCGCCGCCTCGCGCCGCCCGCCCCGGCTCTGACTGACCGCGTTACTCCCACAGGTGAGCGGGCGGGACGGCCCTTCTCCTCCGGGCTGTAATTAGCGCTTGGTTTAATGACGGCTTGTTTCTTTTCTGTGGCTGCGTGAAAGCCTTGAGGGGCTCCGGGAGGGCCCTTTGTGCGGGGGGAGCGGCTCGGGGGGTGCGTGCGTGTGTGTGTGCGTGGGGAGCGCCGCGTGCGGCTCCGCGCTGCCCGGCGGCTGTGAGCGCTGCGGGCGCGGCGCGGGGCTTTGTGCGCTCCGCAGTGTGCGCGAGGGGAGCGCGGCCGGGGGCGGTGCCCCGCGGTGCGGGGGGGGCTGCGAGGGGAACAAAGGCTGCGTGCGGGGTGTGTGCGTGGGGGGGTGAGCAGGGGGTGTGGGCGCGTCGGTCGGGCTGCAACCCCCCCTGCACCCCCCTCCCCGAGTTGCTGAGCACGGCCCGGCTTCGGGTGCGGGGCTCCGTACGGGGCGTGGCGCGGGGCTCGCCGTGCCGGGCGGGGGGTGGCGGCAGGTGGGGGTGCCGGGCGGGGCGGGGCCGCCTCGGGCCGGGGAGGGCTCGGGGGAGGGGCGCGGCGGCCCCCGGAGCGCCGGCGGCTGTCGAGGCGCGGCGAGCCGCAGCCATTGCCTTTTATGGTAATCGTGCGAGAGGGCGCAGGGACTTCCTTTGTCCCAAATCTGTGCGGAGCCGAAATCTGGGAGGCGCCGCCGCACCCCCTCTAGCGGGCGCGGGGCGAAGCGGTGCGGCGCCGGCAGGAAGGAAATGGGCGGGGAGGGCCTTCGTGCGTCGCCGCGCCGCCGTCCCCTTCTCCCTCTCCAGCCTCGGGGCTGTCCGCGGGGGGACGGCTGCCTTCGGGGGGGACGGGGCAGGGCGGGGTTCGGCTTCTGGCGTGTGACCGGCGGCTCTAGAGCCTCTGCTAACCATGTTCATGCCTTCTTCTTTTTCCTACAGCTCCTGGGCAACGTGCTGGTTATTGTGCTGTCTCATCATTTTGGCAAAGAATTG',
    'fluorescence_promoter_name':'CAG',
    'fluorescence_polya_sequence':'CTGTGCCTTCTAGTTGCCAGCCATCTGTTGTTTGCCCCTCCCCCGTGCCTTCCTTGACCCTGGAAGGTGCCACTCCCACTGTCCTTTCCTAATAAAATGAGGAAATTGCATCGCATTGTCTGAGTAGGTGTCATTCTATTCTGGGGGGTGGGGTGGGGCAGGACAGCAAGGGGGAGGATTGGGAAGAGAATAGCAGGCATGCTGGGGA',
    'fluorescence_polya_name':'bGH',
    'fluorescence_linker_sequence':'GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC',
    'fluorescence_linker_name':'T2A',
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin',
    'restriction_list':['RsaI', 'MnlI', 'AciI', 'AluI', 'BmrI'],
    'optimize':True
}

```

** Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```


```
## genes names
project['transcripts']['sequences']['name']

## proteins sequences
project['transcripts']['sequences']['sequence_aa']

## average codon frequency in the input sequence
project['transcripts']['sequences']['vector_sequence_frequence']

## GC% content in the input sequence
project['transcripts']['sequences']['vector_sequence_GC']

############################################################################

## average codon frequency in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_frequence']

## GC% content in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_GC']
    
```




<br />


#### 2.2.2 Creating RNAi / RNAi + expression of the plasmid vector

** Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':'',
    
    # REQUIRED!
    # avaiable of vector types (ssAAV / scAAV / lentiviral / regular)
    'vector_type':'ssAAV',
      
    # REQUIRED!
    # in this case 'vector_function':'rnai'
    'vector_function':'rnai',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (mouse + rat) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # REQUIRED!
    # sequence of provided non-coding promoter
    # for coding sequences the user should choose the promoter of non-coding genes (metadata['promoters']['type'] == 'non-coding')
    # sequence orientation 5' ---> 3' - sense
    'promoter_ncrna_sequence':'',
	# REQUIRED!
    # name of provided promoter sequence
	'promoter_ncrna_name':'',

    # POSSIBLE!
    # sequence of custom RNAi, which can be provided by user
    # if provided, then the algorithm of RNAi estimation is off
    # if empt '' the algorithm share the best possible RNAi based on 'rnai_gene_name'
    # sequence orientation 5' ---> 3' - sense
    'rnai_sequence':'',
    
    # REQUIRED!
    # name of the target gene for the RNAi searching algorithm (gene name for Homo sapien or Mus musculus)
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
	# 'rnai_gene_name' - provide in the HGNC nomenclature
    'rnai_gene_name':'',
    
    # REQUIRED!
    # sequence of the loop to create the structure of the hairpin of shRNA or siRNA depending on the loop sequence
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    # sequence orientation 5' ---> 3' - sense
    'loop_sequence':'',
    
    # WARNING! If the user wants to add additional CDS sequences to parallel transcript expression with silencing by RNAi in one vector; provide sequences, linkers_sequences, promoter_sequence, etc.
    
    # list of coding sequences (CDS) provided to make expression from the vector
    # amount of sequences is not restricted as the user must remember that the length of whole vector is limited
    # excide the relevant vector size can decrease vector working
    # if the user wants to not include any sequences only fluorescent_tag, provide ['']
    # sequences orientation 5' ---> 3' - sense
    'sequences':[''],
    # list of names of coding sequences
    # amount of names should be equal with amount of sequences
    # if provided no sequences, provide ['']
    'sequences_names':[''],
    
    # REQUIRED if more than one sequence of transcripts!
    # sequences of provided linkers
    # number of linkers_sequences should be equal number of sequences (transcripts) - 1. One linker for each pair of sequences.
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_sequences':[''],
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # names of provided linkers
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_names':[''],
    
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # sequence of provided promoter
    # sequence orientation 5' ---> 3' - sense
    'promoter_sequence':'',
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # name of provided promoter sequence
    'promoter_name':'',
    
    # POSSIBLE if transcript sequence occure, if not empty string ''!
    # sequence of provided enhancer
    # sequence orientation 5' ---> 3' - sense
    'regulator_sequence':'',
    # POSSIBLE if transcript sequence occure, if not empty string ''!
    # name of provided enhancer sequence
    'regulator_name':'',
    
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # sequence of provided polyA signal
    # sequence orientation 5' ---> 3' - sense
    'polya_sequence':'',
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # name of provided polyA singla sequence
    'polya_name':'',
    
    # POSSIBLE!
    # sequence of provided fluorescent tag
    # if the user does not need fluorescent tag, provide ''
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_sequence':'',
    # POSSIBLE!
    # name of provided fluorescent tag
    # if the user does not need fluorescent tag, provide ''
    'fluorescence_name':'',
    
    # WARNING! If provided sequences for transcripts (> 0) and do not need additional promoter for fluorescent tag, provide fluorescence_linker_sequence
    
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # sequence of provided fluorescence tag linker
    # sequence orientation 5' ---> 3' - sense
    'fluorescence_linker_sequence':'',
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # name of provided fluorescence tag linker
    'fluorescence_linker_name':'',
    
    # REQUIRED!
    # sequence of provided selection marker
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':'',
    
    # POSSIBLE!
    # restriction enzymes protection of transcript sequences
    # if the user does not need any restriction places protection, provide empty list []
    'restriction_list':[],
    
    # REQUIRED!
    # available options (True / False)
    # decision; if the user wants the transcription sequences optimized based on the provided species
    # if the user has omitted the additional transcript sequences, provide False
    'optimize':True
}  



```


<br />


** Example dictionary:



```
input_dict = {

    'project_name':'test_RNAi',
    'vector_type':'ssAAV',
    'vector_function':'rnai',
    'species':'human',
    'promoter_ncrna_name':'U6',
    'promoter_ncrna_sequence':'GAGGGCCTATTTCCCATGATTCCTTCATATTTGCATATACGATACAAGGCTGTTAGAGAGATAATTGGAATTAATTTGACTGTAAACACAAAGATATTAGTACAAAATACGTGACGTAGAAAGTAATAATTTCTTGGGTAGTTTGCAGTTTTAAAATTATGTTTTAAAATGGACTATCATATGCTTACCGTAACTTGAAAGTATTTCGATTTCTTGGCTTTATATATCTTGTGGAAAGGACGAAACACC',
    'rnai_sequence':'',
    'rnai_gene_name':'PAX3',
    'loop_sequence':'TAGTGAAGCCACAGATGTAC',
    'sequences':['ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA'],
    'sequences_names':['SMN1'],
    'linkers_sequences':[''],
    'linkers_names':[''],
    'promoter_sequence':'GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT',
    'promoter_name':'TBG',
    'regulator_sequence':'CGATAATCAACCTCTGGATTACAAAATTTGTGAAAGATTGACTGGTATTCTTAACTATGTTGCTCCTTTTACGCTATGTGGATACGCTGCTTTAATGCCTTTGTATCATGCTATTGCTTCCCGTATGGCTTTCATTTTCTCCTCCTTGTATAAATCCTGGTTGCTGTCTCTTTATGAGGAGTTGTGGCCCGTTGTCAGGCAACGTGGCGTGGTGTGCACTGTGTTTGCTGACGCAACCCCCACTGGTTGGGGCATTGCCACCACCTGTCAGCTCCTTTCCGGGACTTTCGCTTTCCCCCTCCCTATTGCCACGGCGGAACTCATCGCCGCCTGCCTTGCCCGCTGCTGGACAGGGGCTCGGCTGTTGGGCACTGACAATTCCGTGGTGTTGTCGGGGAAGCTGACGTCCTTTCCATGGCTGCTCGCCTGTGTTGCCACCTGGATTCTGCGCGGGACGTCCTTCTGCTACGTCCCTTCGGCCCTCAATCCAGCGGACCTTCCTTCCCGCGGCCTGCTGCCGGCTCTGCGGCCTCTTCCGCGTCTTCGCCTTCGCCCTCAGACGAGTCGGATCTCCCTTTGGGCCGCCTCCCCGCATCGG',
    'regulator_name':'WPRE',
    'polya_sequence':'CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA',
    'polya_name':'SV40_late',
    'fluorescence_sequence':'ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACCGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCCTGACCTACGGCGTGCAGTGCTTCAGCCGCTACCCCGACCACATGAAGCAGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCACCCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAA',
    'fluorescence_name':'EGFP',
    'fluorescence_linker_sequence':'GGAAGCGGAGAGGGCAGGGGAAGTCTTCTAACATGCGGGGACGTGGAGGAAAATCCCGGCCCC',
    'fluorescence_linker_name':'T2A',
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin',
    'restriction_list':['RsaI', 'MnlI', 'AciI', 'AluI', 'BmrI'],
    'optimize':True
}  
```

** Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```


```
# Top 1 designed RNAi in shRNA form information
# RNAi name
project['rnai']['name']

# RNAi sequence
project['rnai']['sequence']

# RNAi prediction structure
rnai_prediction = project['rnai']['figure']
rnai_prediction.savefig('rnai_predicted_structure.svg')
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />


```
## *if occur user-defined sequences for additional expression in the plasmid vector
## genes names
project['transcripts']['sequences']['name']

## proteins sequences
project['transcripts']['sequences']['sequence_aa']

## average codon frequency in the input sequence
project['transcripts']['sequences']['vector_sequence_frequence']

## GC% content in the input sequence
project['transcripts']['sequences']['vector_sequence_GC']

############################################################################

## average codon frequency in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_frequence']

## GC% content in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_GC']
```




<br />


#### 2.2.3 Creating plasmid vector of in-vitro transcription of mRNA

** Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':'',
    
    # REQUIRED!
    # avaiable of vector types (transcription)
    'vector_type':'transcription',
    
    # REQUIRED!
    # in this case 'vector_function':'mrna'
    'vector_function':'mrna',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (mouse + rat) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # REQUIRED!
    # list of coding sequences (CDS) provided to make expression from the vector
    # amount of sequences is not restricted as the user must remember that the length of whole vector is limited
    # excide the relevant vector size can decrease vector working
    # sequences orientation 5' ---> 3' - sense
    'sequences':[''],
    # REQUIRED!
    # list of names of coding sequences
    # amount of names should be equal with amount of sequences
    # if provided no sequences, provide ['']
    'sequences_names':[''],
    
    # REQUIRED if more than one sequence of transcripts!
    # sequences of provided linkers
    # number of linkers_sequences should be equal number of sequences (transcripts) - 1. One linker for each pair of sequences.
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    # sequence orientation 5' ---> 3' - sense
    'linkers_sequences':[''],
    # REQUIRED if transcript sequence occure, if not empty string ''!
    # names of provided linkers
    # if the number of transcript sequences is equal 1 then provide empty list []
    # if the user wants to not provide any linkers between the transcript sequences, provide an empty string '' for each pair of transcripts where the user wants to avoid linker; empty strings '' provide inside the list ['']
    'linkers_names':[''],
    
    # REQUIRED!
    # sequence of provided 5`UTR
    # sequence orientation 5' ---> 3' - sense
    'utr5_sequence':'',
    # REQUIRED!
    # name of provided 5`UTR
    'utr5_name':'',
    
    # REQUIRED!
    # sequence of provided 3`UTR
    # sequence orientation 5' ---> 3' - sense
    'utr3_sequence':'',
    # REQUIRED!
    # name of provided 3`UTR
    'utr3_name':'',
    
    # REQUIRED!
    # number (integer) of A repeat in the polyA tail
    'polya_tail_x':00,
    
    # REQUIRED!
    # sequence of provided selection marker
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':'',
    
    # POSSIBLE!
    # restriction enzymes protection of transcript sequences
    # if the user does not need any restriction places protection, provide empty list []
    'restriction_list':[],
    
    # REQUIRED!
    # available options (True / False)
    # decision; if the user wants the transcription sequences optimized based on the provided species
    'optimize':True

}
```


<br />


** Example dictionary:



```
input_dict = {
    
    'project_name':'test_invitro_transcription_mRNA',
    'vector_type':'transcription',
    'vector_function':'mrna',
    'species':'human',
    'sequences':['ATGGCGATGAGCAGCGGCGGCAGTGGTGGCGGCGTCCCGGAGCAGGAGGATTCCGTGCTGTTCCGGCGCGGCACAGGCCAGAGCGATGATTCTGACATTTGGGATGATACAGCACTGATAAAAGCATATGATAAAGCTGTGGCTTCATTTAAGCATGCTCTAAAGAATGGTGACATTTGTGAAACTTCGGGTAAACCAAAAACCACACCTAAAAGAAAACCTGCTAAGAAGAATAAAAGCCAAAAGAAGAATACTGCAGCTTCCTTACAACAGTGGAAAGTTGGGGACAAATGTTCTGCCATTTGGTCAGAAGACGGTTGCATTTACCCAGCTACCATTGCTTCAATTGATTTTAAGAGAGAAACCTGTGTTGTGGTTTACACTGGATATGGAAATAGAGAGGAGCAAAATCTGTCCGATCTACTTTCCCCAATCTGTGAAGTAGCTAATAATATAGAACAAAATGCTCAAGAGAATGAAAATGAAAGCCAAGTTTCAACAGATGAAAGTGAGAACTCCAGGTCTCCTGGAAATAAATCAGATAACATCAAGCCCAAATCTGCTCCATGGAACTCTTTTCTCCCTCCACCACCCCCCATGCCAGGGCCAAGACTGGGACCAGGAAAGCCAGGTCTAAAATTCAATGGCCCACCACCGCCACCGCCACCACCACCACCCCACTTACTATCATGCTGGCTGCCTCCATTTCCTTCTGGACCACCAATAATTCCCCCACCACCTCCCATATGTCCAGATTCTCTTGATGATGCTGATGCTTTGGGAAGTATGTTAATTTCATGGTACATGAGTGGCTATCATACTGGCTATTATATGTTTCCTGAGGCCTCCCTAAAAGCCGAGCAGATGCCAGCACCATGCTTCCTGTAA'],
    'sequences_names':['SMN1'],
    'linkers_sequences':[''],
    'linkers_names':[''],
    'utr5_sequence':'GGGCTGGAAGCTACCTTTGACATCATTTCCTCTGCGAATGCATGTATAATTTCTACAGAACCTATTAGAAAGGATCACCCAGCCTCTGCTTTTGTACAACTTTCCCTTAAAAAACTGCCAATTCCACTGCTGTTTGGCCCAATAGTGAGAACTTTTTCCTGCTGCCTCTTGGTGCTTTTGCCTATGGCCCCTATTCTGCCTGCTGAAGACACTCTTGCCAGCATGGACTTAAACCCCTCCAGCTCTGACAATCCTCTTTCTCTTTTGTTTTACATGAAGGGTCTGGCAGCCAAAGCAATCACTCAAAGTTCAAACCTTATCATTTTTTGCTTTGTTCCTCTTGGCCTTGGTTTTGTACATCAGCTTTGAAAATACCATCCCAGGGTTAATGCTGGGGTTAATTTATAACTAAGAGTGCTCTAGTTTTGCAATACAGGACATGCTATAAAAATGGAAAGAT',
    'utr5_name':'SMN1',
    'utr3_sequence':'CAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTA',
    'utr3_name':'KIT',
    'polya_tail_x':50,
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin',
    'restriction_list':['RsaI', 'MnlI', 'AciI', 'AluI', 'BmrI'],
    'optimize':True
}
```

** Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```

```
## genes names
project['transcripts']['sequences']['name']

## proteins sequences
project['transcripts']['sequences']['sequence_aa']

## average codon frequency in the input sequence
project['transcripts']['sequences']['vector_sequence_frequence']

## GC% content in the input sequence
project['transcripts']['sequences']['vector_sequence_GC']

############################################################################

## average codon frequency in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_frequence']

## GC% content in the output sequence
project['transcripts']['sequences']['optimized_vector_sequence_GC']
```



<br />


#### 2.2.3 Creating plasmid vector of in-vitro transcription of RNAi

** Empty input dictionary schema:


```
input_dict = {
    
    # REQUIRED!
    # name of current project (defined by user)
    'project_name':'',
    
    # REQUIRED!
    # avaiable of vector types (transcription)
    'vector_type':'transcription',
    
    # REQUIRED!
    # in this case 'vector_function':'rnai'
    'vector_function':'rnai',
    
    # REQUIRED!
    # avaiable options (human / mouse / rat / both (mouse + human) / both2 (mouse + rat) / multi (mouse + rat + human))
    # 'both / both2 / multi' - creating vector function adjusted for all species taking into consideration most adjustments for Homo sapiens
    'species':'human',
    
    # POSSIBLE!
    # sequence of custom RNAi, which can be provided by user
    # if provided, then the algorithm of RNAi estimation is off
    # if empt '' the algorithm share the best possible RNAi based on 'rnai_gene_name'
    # sequence orientation 5' ---> 3' - sense
    'rnai_sequence':'',
    
    # REQUIRED!
    # name of the target gene for the RNAi searching algorithm (gene name for Homo sapien or Mus musculus)
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    'rnai_gene_name':'',
    
    # REQUIRED!
    # sequence of the loop to create the structure of the hairpin of shRNA or siRNA depending on the loop sequence
    # algorithm is working when the rnai_sequence is empty ''
    # if the user defines 'rnai_sequence' this 'rnai_gene_name' is just a name for a user-supplied sequence
    # sequence orientation 5' ---> 3' - sense
    'loop_sequence':'',
    
    # REQUIRED!
    # sequence of provided selection marker
    # sequence orientation 5' ---> 3' - sense
    'selection_marker_sequence':'',
    # REQUIRED!
    # name of provided selection marker
    'selection_marker_name':''
}
```


<br />


** Example dictionary:



```
input_dict = {

    'project_name':'test_invitro_transcription_RNAi',
    'vector_type':'transcription',
    'vector_function':'rnai',
    'species':'human',
    'rnai_sequence':'',
    'rnai_gene_name':'KIT',
    'loop_sequence':'TAGTGAAGCCACAGATGTAC',
    'selection_marker_sequence':'ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGAAGCCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA',
    'selection_marker_name':'Ampicillin'
}
```

** Output:

```
# Name of project
project['project']
```

``` 
# Graph of the designed vector
vector_plot = project['vector']['graph']
vector_plot.savefig('expression_vector.svg')
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# Complete FASTA file of the designed vecotr
project['vector']['full_fasta']
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

```
# The FASTA file is divided into particular elements of the designed vector
project['vector']['fasta']
```


```
# Top 1 designed RNAi in shRNA form information
# RNAi name
project['rnai']['name']

# RNAi sequence
project['rnai']['sequence']

# RNAi prediction structure
rnai_prediction = project['rnai']['figure']
rnai_prediction.savefig('rnai_predicted_structure.svg')
```

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />







<br />

#### 3. Enter sequence

```
sequence = sq.load_sequence(coding = True)
```


<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/enter_sequence.bmp?raw=true" alt="drawing" width="600" />
</p>

<br />

#### 4. Optimization of codon frequency and GC content

```
species = 'human'

optimized_sequence = sq.codon_otymization(sequence, metadata['codons'], species)
```

* species - species-specific codon frequency (must be provided) ['human'/'mouse'] 



<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/optimized.bmp" alt="drawing" width="600" />
</p>

<br />

#### 5. Find possible restriction places in the sequence

```
sequence = optimized_sequence['sequence_na'][1]
restriction = metadata['restriction']

enzyme_restriction, restriction =  sq.check_restriction(sequence, restriction)
```
* enzyme_restriction - possible restriction enzymes' places with place coordinates in the whole sequence
* restriction - cumulative enzyme_restriction table of all restriction enzymes' indexes in sequence

<br />

#### 6. Choose restriction enzymes place to repair in the sequence

```
enzyme_list = sq.choose_restriction_to_remove(restriction)
```
* enzyme_list - list of chosen (indexes) enzymes restriction places 

<br />

#### 7. Repair chosen restriction places

```
final_sequence, not_repaired, enzyme_restriction, restriction =  sq.repair_sequences(optimized_sequence['sequence_na'][1], metadata['codons'], enzyme_restriction, metadata['restriction'], enzyme_list, 'human')
```

* final_sequence - optimized sequence for chosen restrcition places
* not_repaired - restriction enzymes' places that were unable to repair
* enzyme_restriction - possible restriction enzymes' places with place coordinates which were created during optimization
* restriction - cumulative enzyme_restriction table of all restriction enzymes' indexes in sequence


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/restriction_optimization.bmp" alt="drawing" width="600" />
</p>

<br />

## vector_graph:

#### 1. Import part of  library

```
from JBioSeqTools import graph_plot as gp
```
<br />

#### 2. Create a graph of vector 


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/final_vector_df.bmp" alt="drawing" width="600" />
</p>

** Required dataframe [vector_df]: <br />
	- data must be provided in form data frame like above <br />
	- provided in column 'elements' cells with 'backbone_element' name will not signed in graph of vector 

<br />

```
title = 'Vector_name'

pl = gp.vector_plot(vector_df, title)
```

* title - name of the vector

<br />

<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/vector_plot.png?raw=true" alt="drawing" width="600" />
</p>

<br />

## vector_build:

#### 1. Import part of  library

```
from JBioSeqTools import vector_build as vb
```
<br />

#### 2. Download required metadata

```
metadata = vb.load_metadata()    
```

<br />

#### 3. Create vector project

```
project = vb.create_project(project_name)
```

* project_name - name for the current project of the vector

<br />

#### 4. Choose a number of sequences in vector and enter them

```
project = vb.load_sequences(n, project, coding = True)
```

* n - number of transcript sequences in the vector
* coding - check trinucleotide repeats content for coding sequence [True/False]



<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/sequence.bmp" alt="drawing" width="600" />
</p>

<br />

#### 5. Choose gene promoter for vector sequence

```
project = vb.choose_promoter(metadata['promoters'], project) 
```

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/promotor.bmp" alt="drawing" width="600" />
</p>

<br />

#### 6. Choose fluorescent tag for vector sequence

```
project = vb.choose_fluorescence(metadata['fluorescent_tag'], metadata['linkers'], project)
```

<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/fluorescence.bmp" alt="drawing" width="600" />
</p>

<br />

#### 7. Choose linkers between entered transcript sequences

```
project = vb.choose_linker(n, metadata['linkers'], project)
```

* n - number of transcript sequences in the vector



<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/linker.bmp" alt="drawing" width="600" />
</p>

<br />

#### 8. Choose regulatory element for vector sequence

```
project = vb.choose_regulator(metadata['regulators'], project)
```

* n - number of transcript sequences in the vector



<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/regulator.bmp" alt="drawing" width="600" />
</p>

<br />

#### 9. Check for unnecessary stop codon between transcripts

```
project = vb.check_stop(project, metadata['codons'])
```

<br />

#### 10. Optimization of codon frequency and GC content for transcripts

```
species = 'human'

project = vb.sequence_enrichment(project, metadata['codons'], species)
```

* species - species-specific codon frequency (must be provided) ['human'/'mouse'] 

<br />

#### 11. Choose version of transcript: before or after optimization

```
project = vb.choose_sequence_variant(project)
```


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/optymalization.bmp" alt="drawing" width="600" />
</p>

<br />

#### 12. Find possible restriction places for transcripts

```
project = vb.find_restriction_vector(project, metadata['restriction'])
```

<br />

#### 13. Choose restriction enzymes place to repair in the transcripts

```
project = vb.choose_restriction_vector(project, metadata['restriction'])
```


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/restriction.bmp" alt="drawing" width="600" />
</p>

<br />

#### 14. Repair chosen restriction places

```
species = 'human'

project = vb.repair_restriction_vector(project, metadata['restriction'], metadata['codons'], species)
```

<br />

#### 15. Prepare vector to eval sequence 

```
project = vb.vector_string(project, metadata['backbone'], vector_type)
```

<br />

#### 16. Create vector sequence and data frame

```
project = vb.eval_vector(project, metadata['vectors'], vector_type)
```


<p align="center">
<img  src="https://raw.githubusercontent.com/jkubis96/JBioSeqTools/main/fig/final_vector_df.bmp" alt="drawing" width="600" />
</p>

<br />

#### 17. Create a graph of vector 

```
title = 'Vector_name'

project, pl = vb.vector_plot_project(project, title)
```


<p align="center">
<img  src="https://github.com/jkubis96/JBioSeqTools/blob/main/fig/vector_plot.png?raw=true" alt="drawing" width="600" />
</p>

<br />