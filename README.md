# qintervals
[![Build Status](https://travis-ci.org/JimMadge/qintervals.svg?branch=master)](https://travis-ci.org/JimMadge/qintervals)
[![codecov](https://codecov.io/gh/JimMadge/qintervals/branch/master/graph/badge.svg)](https://codecov.io/gh/JimMadge/qintervals)

An interval training program written in Python with a Qt GUI.

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
- `intervals` - the ordered list of intervals or blocks in the workout

The value of workout is a mixed list of intervals or blocks (with key `block`).

Each interval has the following keys,

- `type` - the type of interval, which can take the values warmup, warmdown, work and rest
- `name` - a label for the interval that is displayed by the program, which can be used to give instructions
- `length` - the length of the interval given as a number immediately followed by 's' for seconds and 'm' for minutes _e.g._ '30s' or '5m'

A block is a collection of intervals (or other blocks) that are repeated. A
block has the following keys,

- `repeats` - the number of times to repeat a block
- `intervals` - the ordered list of intervals or blocks to be repeated
- `skip_last_rest` - whether to skip the last interval of a block if it is a
  rest (useful when a block is followed by a rest interval and you want to avoid
  having two rest intervals in a row)

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

  - block:
      repeats: 2
      skip_last_rest: true
      intervals:
        - type: work
          name: Zone 4, low
          length: 5m
        - type: rest
          name: Rest
          length: 60s

...
```
