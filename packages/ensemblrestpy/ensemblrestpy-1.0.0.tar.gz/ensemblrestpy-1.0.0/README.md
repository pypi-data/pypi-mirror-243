INSTALLATION
============

```bash
pip install ensemblrestpy
```
quick start
========

**Python client for Ensembl REST API**
```python
import pprint

from ensembl import Ensembl

ensembl = Ensembl()
pprint.pprint(ensembl.variant_recoder("rs137853120", fields="id", var_synonyms=1))
pprint.pprint(ensembl.variation("rs137853120", pops=1))
pprint.pprint(ensembl.vep_id("rs137853120", dbNSFP="gnomAD_genomes_EAS_AF,gnomAD_genomes_EAS_AC,gnomAD_genomes_EAS_AN"))

```