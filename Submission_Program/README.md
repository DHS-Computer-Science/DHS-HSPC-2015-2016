# Scoreboard

## Contributors
- NONE

## Specification
- Login at start
  - to check attemt to ssh to host(Grading/Scorboard server)
- Take in multitple files
- Zip
  - See sample_packet/
- dropdown to select assignment number/name
- send to grading host
  - ~~using scp/rsync~~ (terrible idea)
  - ~~to the *"/submissions/<team id>/"* dir on host~~ (also bad)
  - ~~figure this out on your own, and tell the grading team where to find the submissions~~
  - The exact directory I won't be sure about until I get an installation of XAMPP fully configured, however based on my local installation the submissions will most likely go into the "C:\xampp\" or "C:\xampp\htdocs" directory. If PHP can write to disk anywhere, then the destination does not matter and can be configured to whatever.
  - Submissions are required to be zipped, and must be less than 1MB (File size can change if needed)
- recive notifications from grading server
  - TODO(tell Grading Program contributors how you want this done)

## Additional Toughts
- TODO
