# Grading Program

## Contributors
- Andriy Zasypkin

## Dependancies
- python3
- javalang
- watchdog
- mysql.connector
- tkinter

## Problems
The grader will need both input and output files for testing purposes.
Here is a partial tree of the directory structure:
```
problems_dir/
├── 01/
│   ├── input
│   └── output
├── 02/
│   ├── input
│   └── output
├── -3/
│   ├── input
│   └── output
...
```

- `problems_dir` is defined via the comand line, or the config file
- input/output files should not have .txt at the end, and are case sensitive
  - also they use *nix line endings - `\n` (NOT `\r` nor `\r\n`)

## Instalation
1. install python3 and pip(on a debian based GNU/Linux distro - like ubuntu).
  - `sudo apt-get update && sudo apt-get install python3-pip python3`
2. install other dependancies
  - `sudo pip3 install javalang watchdog`
  - `sudo apt-get install python3-mysql.connector python3-tk`

## Running
1. Edit the confguration file(conf.ini)
  - the config file will have comments on all of the options
2. run `./grader-program.py`
  - for help on command line options run `grader-program.py -h`
