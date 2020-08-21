# qintervals
[![Build Status](https://travis-ci.org/JimMadge/qintervals.svg?branch=master)](https://travis-ci.org/JimMadge/qintervals)
[![codecov](https://codecov.io/gh/JimMadge/qintervals/branch/master/graph/badge.svg)](https://codecov.io/gh/JimMadge/qintervals)

An interval training program written in Python with a Qt GUI.

## Installation
### User Installation with pip

To use qintervals you will need to ensure you have Qt5 installed

Clone the repository

```
$ git clone https://github.com/JimMadge/qintervals.git
```

Install using pip
```
$ cd qintervals
$ pip3 install --user .
````

`qintervals` will be installed to `~/.local/bin` so ensure this directory is in
your `$PATH`.

## Usage

`qintervals` takes a single positional argument, the path to a YAML workout
file. Example workout files may be found in the [examples](./examples) directory.

To run one of the examples

```
$ qintervals qintervals/examples/threshold.yml
```

## Workout File Format

A workout is a series of intervals, or blocks (groups of repeated intervals).

Workout files are written in [YAML](https://yaml.org/). There are two top-level
keys

| key         | description                                            |
| ---         | ---                                                    |
| `title`     | title of the workout                                   |
| `intervals` | ordered list of `interval`s or `block`s in the workout |

Each interval has the following keys

| key      | description                                                                               |
| ---      | ---                                                                                       |
| `type`   | type of interval, one of `warmup`, `warmdown`, `work` or `rest`                           |
| `name`   | interval label that is displayed by the program, can be used to give instructions         |
| `length` | length of the interval given as a whole number of minutes or seconds _e.g._ `30s` or `5m` |

A block has the following keys

| key              | description                              |
| ---              | ---                                      |
| `repeats`        | number of times to repeat a block        |
| `intervals`      | ordered list of intervals or blocks      |
| `skip_last_rest` | skip the last interval if it is a rest*  |

(*useful when a block is followed by a rest interval and you want to avoid having two rest intervals in a row)

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
