# coar

**coar** is implementation of clustering of association rules based on user defined thresholds.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **coar**.

```bash
pip install coar
```

## Usage

Usage is displayed on association rules mined using [Cleverminer](https://www.cleverminer.org/) using modified version of [CleverMiner quickstart example](https://www.cleverminer.org/docs-page.html#section-3). You need to install **cleverminer** first.

```bash
pip install cleverminer
```

Mining association rules using **cleverminer**:

```python
# imports
import json
import pandas as pd
from cleverminer import cleverminer

# getting the source file
df = pd.read_csv(
    'https://www.cleverminer.org/hotel.zip', 
    encoding='cp1250', 
    sep='\t'
)

# selecting the columns
df = df[['VTypeOfVisit', 'GState', 'GCity']]


# mining association rules
clm = cleverminer(
    df=df, proc='4ftMiner',
    quantifiers={'conf': 0.6, 'Base': 50},
    ante={
        'attributes': [
            {'name': 'GState', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
            {'name': 'GCity', 'type': 'subset', 'minlen': 1, 'maxlen': 1},
        ], 'minlen': 1, 'maxlen': 2, 'type': 'con'},
    succ={
        'attributes': [
            {'name': 'VTypeOfVisit', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
        ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
)

# saving rules to file
with open('rules.json', 'w') as save_file:
    save_file.write(json.dumps(clm.rulelist))


```

Clustering rules using **coar**:

```python
# imports
import json
import pandas as pd

from coar.cluster import agglomerative_clustering, cluster_representative


# loading rules
rule_file = open('rules.json')
rule_list = json.loads(rule_file.read())

# creating dataframe
df = pd.DataFrame.from_records([{
    'antecedent': set(attr for attr in rule['cedents_str']['ante'].split(' & ')),
    'succedent': set(attr for attr in rule['cedents_str']['succ'].split(' & ')),
    'support': rule['params']['rel_base'],
    'confidence': rule['params']['conf']
} for rule in rule_list])

# clustering
clustering = agglomerative_clustering(
    df,
    abs_ante_attr_diff_threshold=1,
    abs_succ_attr_diff_threshold=0,
    abs_supp_diff_threshold=1,
    abs_conf_diff_threshold=1,
)

# getting cluster representatives
clusters_repr = cluster_representative(clustering)

```

## Contributing

If you find a bug 🐛, please open a [bug report](https://github.com/jmichalovcik/coar/issues/new?assignees=jmichalovcik&labels=bug).
If you have an idea for an improvement, new feature or enhancement 🚀, please open a [feature request](https://github.com/jmichalovcik/coar/issues/new?assignees=jmichalovcik&labels=enhancement).

## License
[MIT](https://github.com/jmichalovcik/coar/blob/master/LICENSE)