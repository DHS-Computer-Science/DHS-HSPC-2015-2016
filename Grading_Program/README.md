# Grading Program

## Contributors
- Andriy Zasypkin

## Specification
- Accept Packeted Subbisions
- Grade right or wrong
  - input/output files for problem must be already made
  - program's output will be compared against master output for correctness
  - if program runs for more than 60 seconds, it will be terminated and submission will be marked as wrong
- Will use a queueing system
  - so that the test of submissions will not interfere with each other

## Setup/Installation
Make sure that these things are intalled/working on the machine running the grader:
- python3
- watchdog(python modual use pip to install)
- [mysql](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html "documentation")(standard python me thinks, but just in case...)

## Additional Toughts
- The computer running this program will have accounts for all the teams
  - rsync/scp can be used to transfer the submission packets
- Packets will be zips
  - name must be in format `<team id>_<submission no.>`
    - team id will be a number
    - submission number should be stored by the submission program, starts at 1
  - must contain info file
    - sample can be found in sample_packet/
  - will contain .java file(s)
  - only one class with main method
    - the name of this class does not matter
    - if there are more, only the first such class will be run
  - *may* contain .class files
    - these will be ignored
- Score board creation
  - since this program willl track if an assignmet is complete, it will also do scoreboard managment
  - tracking of scores will be done in a file(from which database will be read)
  - sorting will be done(by this program) when scores are writen
  - reading before computation
    - number of attempt will need to be read, as they are not stored by the program
    - other entries will need to be read for sorting purposes
