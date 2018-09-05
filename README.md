# qintervals

An interval training program written in python with a Qt GUI.

## Requirements

- Python3
- Qt5
- setuptools
- PyQt5
- PyYAML

## Installation

Clone the repository and change into the root directory, then run `pip3 install --user .`

## Usage

After installation the command `qintervals` should be installed to your local path (_i.e._ `~/.local/bin/`). The program takes a single positional argument, which is the path to the YAML workout file you want to use. An example is included in the examples directory.

`qintervals qintervals/examples/threshold.yml`

## Workout File Format

The workout files are written in yaml with the following keys,

- `title` - the title of the workout
- `workout` - the ordered list of intervals or blocks of intervals in the workout

The value of workout is a mixed list of intervals (with key `interval`) or
blocks (with key `block`).

Each interval has the following keys,

- `type` - the type of interval, which can take the values warmup, warmdown, work and rest
- `name` - a label for the interval that is displayed by the program, which can be used to give instructions
- `length` - the length of the interval given as a number immediately followed by 's' for seconds and 'm' for minutes _e.g._ '30s' or '5m'

A block is a collection of intervals that are repeated. A block has the
following keys,

- `repeat` - the number of times to repeat a block
- `intervals` - the ordered list of intervals (as defined above) to be repeated

For example
```yaml
title: Threshold
workout:
  - interval:
    type: warmup
    name: Warm up
    length: 10m

  - interval:
    type: work
    name: Zone 3
    length: 10m

  - interval:
    type: rest
    name: Rest
    length: 5m

  - block:
    repeat: 2
    intervals:
      - type: work
        name: Zone 4, low
        length: 5m
      - type: rest
        name: Rest
        length: 60s

...
```
