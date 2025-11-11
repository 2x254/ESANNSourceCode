# Implementation of ECCA, CCLP, and CCA-k-RFP-M1

## Important steps before testing:
1. Extract the ZIP file.
2. Open a terminal and navigate to the extracted folder using the `cd` command.
3. Install the required libraries.
4. When testing **ECCA** and **CCLP**, install **Scikit-mine** to use the LCM algorithm for mining classical itemsets.  
   - For **CCLP**, the minimum support is fixed at 0%.  
   - For **ECCA**, the minimum support varies by dataset to select only the minimal set of patterns needed for clustering.
5. When testing **CCA-k-RFP-M1**, note that on macOS the SAT solver may be blocked for security reasons.  
   If this occurs, go to **System Preferences → Security & Privacy**, allow the application, and it should work.

## Generating k-RFPs for CCA-k-RFP-M1:
Before running **CCA-k-RFP-M1**, you must generate the k-RFPs.  
Example command for the Zoo-1 dataset with a minimum support of 10% (101 × 0.1 = 10.1):
./xsat4DAR -kx=1 -ky=1 -minsupp=10 -gdar=1 -msi=10 dataset/zoofinal.txt | grep "^[1-9]" > RelaxedPatterns/patternsk1.txt


### Parameter definitions:
- `kx` → relaxation parameter (e.g., k = 1)
- `minsupp` → minimum support
- Note: `minsupp = msi` for efficiency reasons

## Scripts:
- **CCA-k-RFP-M1.py** → CCA-k-RFP-M1 approach (k-RFP generation + Integer Linear Programming model called M1)
- **ECCA.py** → Enhanced Conceptual Clustering Approach (filtered itemsets + Integer Linear Programming model called M1)
- **CCLP.py** → Ouali et al.’s approach (all itemsets + Integer Linear Programming model called M1)
