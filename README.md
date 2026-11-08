# DictPurge

> An advanced dictionary manipulation & wordlist merging tool — written purely in Python — which takes wordlists and merges them into one dynamic, optimized dictionary for security auditing and dictionary-based attacks.

## About

DictPurge is a Python 3 modernization of the original Dymerge project.

Originally developed by **Nickolas Kamarinakis**.
Ported and modified by **Aryan Kumar Shrivastav**.
- Compatible with Python 3.x
- Author: **Aryan Kumar Shrivastav**

---

## Installation & Running

### 1. Direct Terminal Execution
Clone the repo and run `DictPurge` directly in your terminal:

```bash
cd dictpurge/
DictPurge
```
*(or `python dictpurge.py`)*

### 2. Global Installation (via setup.py)
To make `DictPurge` accessible from any terminal anywhere on your system:

```bash
cd dictpurge/
pip install -e .
```
Now, simply typing `DictPurge` in any terminal will launch the tool immediately!


<img width="1053" height="743" alt="Screenshot 2026-11-09 021021" src="https://github.com/user-attachments/assets/67019639-4360-4377-a712-9ec2eb201b81" />


---

## Usage

```
Usage: DictPurge {dictionaries} [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        output filename
  -i INCLUDE_VALUES, --include=INCLUDE_VALUES
                        include specified values in dictionary
  -z ZIP_TYPE, --zip=ZIP_TYPE
                        zip file with specified archive format
  -s, --sort            sort output alphabetically
  -u, --unique          remove dictionary duplicates
  -r, --reverse         reverse dictionary items
  -f, --fast            finish task asap

Examples:
  DictPurge ~/dictionaries/ -s -u -o ~/powerful.txt
  DictPurge /usr/share/wordlists/rockyou.txt /lists/cewl.txt -s -u
  DictPurge /lists/cewl.txt /lists/awlg.txt -s -u -i and,this
  DictPurge ~/fsocity.dic -u -r -o ~/clean.txt
  DictPurge /dicts/crunch.txt /dicts/john.txt -u -f -z bz2
```

To view all available options run:

```bash
DictPurge -h
```

---

## Developer

- **Aryan Kumar Shrivastav**

## License

Copyright 2024 by Aryan Kumar Shrivastav. Some rights reserved.

DictPurge is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the license file.

