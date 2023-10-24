# Wireless Indoor Localization

Wireless Localization using fingerprinting. Final year ECE project. 
Offline Phase
- Calibration
Online Phase
- Usage, Real Time Localization

## Introduction

Implements a localization system with two commandline applications for using it:
- app1: for calibration of the system
- app2: for localization 

Viewing tables
cmd: py read_db.py db_name tb_name n_rows
eg:  py read_db.py devdb.db fingerprints 10

Collecting a radio map
cmd: py app_main.py 

Clean and reset db to its initial state
    use with caution
cmd: py clean_db.py db_name
eg:  py clean_db.py devdb.py    

## Features

## Getting Started

### Prerequisites

### Installation

## Usage

1. app_main.py
- caputures the fingeprint of the current location. THis is the only way a fingerprint
- can be addded. 

2. read_db.py
- reads and formats the contents of the table that stores the fingerprints

3. clean_db.py
- resets the database that stores the fingperprints. 
- should be used with caution. 

## Contributing
- Ngari Crisphine: crisphine96@gmail.com
- Asogwa Emmanuel: asogwaemmanuel36@gmail.com 

## License

## Acknowledgments
