# Spark Installation

## Prerequisite 

1. Configure portforward.yaml first
1. [Lauch port forward](../portforward/readme.md)

## Usage

```bash
fab install # Install sparks
fab start-spark # start spark cluster
fab stop-spark  # stop spark cluster
```

Install additional Python libraries

```bash
fab pip scikit_learn
```