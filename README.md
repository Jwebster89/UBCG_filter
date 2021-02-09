# UBCG_filter

UBCG_filter.py is for filtering the results of a UBCG output and producing alignments of any reference isolates that contain all UBCGs as well as keeping particular isolates, supplied in a list, that meet the threshold (for example, keeping isolates that were sequenced in the study).

In the following example, with a threshold=5, Isolate 2, Reference 2 and Reference 3 would be removed (&#x26A0;) from the analysis if a list containing Isolate 1 and Isolate 2 is supplied to -s. These isolates are removed because they are missing (&#x274C;) too many genes (references are expected to contain all UBCG and sequenced isolates must pass a threshold). In this example, filtered alignments are produced for all genes but Gene 1.

|   |  Gene 1 &#x26A0;|  <span style="font-weight:normal">Gene 2</span>  |  Gene 3  | Gene 4   |  Gene 5  | Gene 6 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
|Isolate 1   | &#x274C; |   |   |   |   |   |
|**Isolate 2**  &#x26A0; |   |   |   |  &#x274C; |  &#x274C; |   |
|Reference 1   |   |   |   |   |   |   |
|**Reference 2**  &#x26A0; |   |   |   |  &#x274C; |   |   |
|**Reference 3**  &#x26A0;|   |  &#x274C; |   |   | &#x274C;   |   |
|Reference 4   |   |   |   |   |   |   |

### Creating the isolate list file
The isolate list can be created easily from a folder that contains all the isolates of interest. `.fasta` can be replaced with whatever the file extension is e.g. ".fna". The last two commands just enclose the filenames in ' ', as UBCG adds ' ' either side of the sample names and the names listed with ls need to match the names from UBCG.

```
ls ./folder_of_isolates > isolate.list
sed -i "s/.fasta//g" isolate.list
sed -i "s/^/'/g" isolate.list
sed -i "s/$/'/g" isolate.list
```
### But why does UBCG_filter remove any reference that doesn't have a *complete* UBCG profile?

In my testing, with large datasets, if references genomes are kept above the threshold set (default 85) but below a complete repertoire of UBCGs, UBCG will filter out too many gene alignments. This will be less of a problem with smaller, more complete datasets. If UBCG_filter is removing references you would like to keep, these references can be added to the isolate.list file to ensure they are retained for your analysis.

### Usage
` ./UBCG_filter.py -p <UBCG output path> -i <isolate list> [-t threshold]`

### Recommendations
UBCG filter is great for running all your isolates and references as a general first pass and inspecting the "unused.txt" file to see which genomes won't be retained in the final filtering (rather than waiting for this first pass of filtering to complete, you can ctrl+c UBCG_fitler after it says "List of unused samples saved to 'unused.txt'"). From here, you may add references to your isolate.list to retain important references, change your threshold setting to keep important samples and use the unused.txt to remove references/samples from your bcg folder. Once these references have been removed, you are free to rerun UBCG align followed by UBCG_filter to produce filtered alignments of only genes that contain all genomes. These can then for example be recombination filtered with [ClonalFrame](https://github.com/xavierdidelot/ClonalFrameML) and ML phylogenies produced with RAxML.

