# qalx-orcaflex

Tools to help you run OrcaFlex on [qalx](https://qalx.net).

> To use this package you'll need a **qalx** API key.
> This can be obtained by registering at [qalx.net](https://qalx.net#section-contact). 
>
## Features

The current features are:

- **Batches**: build batches of OrcaFlex data files from various sources
- **Results**: attach some required results which will be extracted automatically when the simulation is complete. The results will also be summarised for each batch
- **Load case information**: results in a batch can be linked to information about the load case
- **Model views**: define a set of model views that will be automatically captured at the end of the simulation
- **Smart statics**: allows you to add object tags that will be used to iteratively find a model that solves in statics

Some planned features:

-  Custom results specification
-  Linked Statistics and Extreme Statistics
-  Model views at key result points (e.g. max of a time history)
-  Model video extraction
-  Optional progress screenshots
-  Automatic batch cancellation on result breach
-  Allowed to define “Model deltas” from a base model
-  Option to extract all model data into qalx (useful if you want to do analytics/ML on model/sim data over time)

## Installation

```bash
pip install qalx-orcaflex
```

## Documentation

[This can be found here.](https://orcaflex.qalx.net)

## Questions?

Please [send us an email (info@qalx.net)](mailto:info@qalx.net)! 
