## GeneBe Utils
Welcome to GeneBe Utils, a Python package that complements the innovative GeneBe platform. GeneBe is a cutting-edge genetics platform designed to empower individuals with insights into their health and well-being.

Using this client, you can easily annotate your DNA variants with the GeneBe API. Annotations include:
* Gene, transcript, and effect
* ClinVar phenotype
* GnomAD frequency
* ACMG score

### Usage

If you want to annotate thousands of variants, please log in to genebe.net, generate an API Key, and provide it using `username` and `api_key`.


```python
from genebe import annotate_variants_list_to_dataframe, annotate_variants_list as gb

input = ['7-69599651-A-G']

# output as a list, with all transcripts
list = gb.annotate_variants_list(input,flatten_consequences = False)

# output as a pandas dataframe, flat
df = gb.annotate_variants_list_to_dataframe(input, flatten_consequences=True)

```

### Installation
You can install GeneBe Utils using pip:

```
pip install genebe
```

For more information about GeneBe, visit GeneBe website, https://genebe.net .




