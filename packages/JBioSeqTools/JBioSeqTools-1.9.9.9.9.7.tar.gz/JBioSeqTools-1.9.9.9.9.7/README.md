# JBioSeqTools - python library

#### JBioSeqTools is the python library for gene sequence optymalization and vector build

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


<div align="justify"> JBioSeqTools is the python library for biological sequence optimization (GC % content & codon frequency) for better expression of different species cells in vivo. It also allows building AAV vectors with the possibility of choosing sequences between ITRs such as transcript, promoter, enhancer, and molecular fluorescent tag. Finally, the user obtains ready for order construct with a whole sequence and visualization </div>

</br>

Used data bases:
* GeneScript [https://www.genscript.com/?src=google&gclid=Cj0KCQiAkMGcBhCSARIsAIW6d0CGxHmZO8EAYVQSwgk5e3YSRhKZ882vnylGUxfWuhareHFkJP4h4rgaAvTNEALw_wcB]
* VectorBuilder [https://en.vectorbuilder.com/]



## Installation

#### In command line write:

```
pip install JBioSeqTools
```

## Usage

<br />

## seq_tools:

#### 1. Import part of  library

```
from JBioSeqTools import seq_tools as sq
```

<br />

#### 2. Download required metadata

```
metadata = sq.load_metadata()
```

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