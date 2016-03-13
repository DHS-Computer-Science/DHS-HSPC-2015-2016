# Problems Archive

This is here for achival purposes only.
DO NOT PUT UPCOMING PROBLEMS HERE

## Directory Format
- YYYY is the current year
- NN is the problem number
- DHS_HSPC_Rules_YYYY.odt will contain the packet(s) that will be handed out
  during the competiton
```
YYYY
├── NN
│   ├── input
│   ├── output
│   └── SolutionNN.java
└── DHS_HSPC_Rules_YYYY.odt
```

## Problem Creation
- The target competitiors are *NOT* APCS students
  - Therefore the problems should be *very* easy
    - Only use data types:
      - int
      - double
      - string
      - char
      - 1D arrays of any of the above
    - No hard logic(see next point)
  - However *some* APCS students may chose to come so the last one or two
    problems should be challenging
  - The 2016 problems were hard

- The problem desciption must be clear and consistent
  - There should not be any room for doubt on what the problem is asking
  - Peer review these problems ahead of time(preferably with the teacher)
  - Peer review sample **and** judging(grading) input and outputs
    - also preferably with the teacher
  - The 2016 problems faild at this as well
    - integers are not doubles
    - integers are not longs

- Grading intput should be long
  - *Not* the sample input that is in the packet
    - that should have at most 5 cases
  - Grading input should have 40 to 500 cases
    - This should test corner cases
    - And efficency of the program(<1 min run)
    - Exception - the practice problem
  - The 2016 problems did not meet this criteria for the most part