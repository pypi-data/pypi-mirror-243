
Translator ARS Pass/Fail Testing 
==========================================================

This testing framework performs single level pass/Fail analysis on queries it receives from the Test Runner. 

### ARS_Test Implementation
```bash
pip install ARS_Test_Runner 
```

### CLI
The command-line interface is the easiest way to run the ARS_Test_Runner
After installation, simply type ARS_Test_Runner --help to see required input arguments & options
- `ARS_Test_Runner`
    - env : the environment to run the queries against (dev|ci|test|prod)
    - query_type: treats(creative)
    - expected_output: TopAnswer|Acceptable|BadButForgivable|NeverShow
    - input_curie: normalized curie taken from assest.csv
    - output_curie: target output curie to do analysis on

- example:
  - for single output
    - ARS_Test_Runner --env 'test' --query_type 'treats_creative' --expected_output 'TopAnswer' 'MONDO:0015564' 'PUBCHEM.COMPOUND:5284616'
  - for multi outputs
    - ARS_Test_Runner --env 'ci' --query_type 'treats_creative' --expected_output '["TopAnswer","TopAnswer"]' --input_curie 'MONDO:0005301' --output_curie '["PUBCHEM.COMPOUND:107970","UNII:3JB47N2Q2P"]'


### python
``` python 
from ARS_Test_Runner.semantic_test import run_semantic_test
report = run_semantic_test(env, query_type, expected_output, input_curie, output_curie)
```







