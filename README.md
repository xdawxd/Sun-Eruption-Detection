# Sun Eruption Detection

Detection of sun eruptions threatening telecommunications satellites

## Description

TODO

## Getting Started

### Prerequisites/Dependencies

* **Python** = ">=3.10,<3.13"
* **Poetry**
* **Docker** (optional) - application can be started without python and poetry

### Installing & Running the application
All commands from this section should be run from within the `Sun-Eruption-Detection/` directory.

#### Locally
1. Create a python virtual environment or use poetry environment
2. Install the packages using poetry
   * **GNU Make** - `make poetry-install` 
   * **Terminal** - `poetry install`
   * `python -m sun_eruption_detection`

#### Docker
**GNU Make**:
1. `make build`
2. `make run`

**Terminal**
1. `docker build --tag sun_eruption_detection .`
2. `docker run sun_eruption_detection`

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

#### Dawid Schwinge

## Contents

TODO