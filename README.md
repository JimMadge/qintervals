# qintervals

An interval training program written in python with a Qt GUI.

## Requirements

- Python3
- setuptools
- PyQt5

## Installation

Clone the repository and change into the root directory, then run `pip3 install .`

## Usage

After installation the command `qintervals` should be installed to your local path. The program takes a single positional argument, which is the path to the YAML workout file you want to use. An example is included in the examples directory.

`qintervals qintervals/examples/threshold.yml`

## Workout File Format

The workout files are written in yaml with the following keys,

- `title` - the title of the workout
- `intervals` - the ordered list of intervals in the workout

Each interval in the list has the following keys,

- `type` - the type of interval, which can take the values warmup, warmdown, work and rest
- `name` - a label for the interval that is displayed by the program, which can be used to give instructions
- `length` - the length of the interval given as a number immediately followed by 's' for seconds and 'm' for minutes _e.g._ '30s' or '5m'

For example
```yaml
title: Threshold
intervals:
- type: warmup
  name: Warm up
  length: 10m

- type: work
  name: Zone 3
  length: 10m

- type: rest
  name: Rest
  length: 5m

...
```
