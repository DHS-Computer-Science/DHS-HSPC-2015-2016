# Submission Program

## Contributors
- Noah Davis

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
  - ~~The exact directory I won't be sure about until I get an installation of XAMPP fully configured, however based on my local installation the submissions will most likely go into the "C:\xampp\" or "C:\xampp\htdocs" directory. If PHP can write to disk anywhere, then the destination does not matter and can be configured to whatever.~~
  - Submissions are saved to "C:/xampp/submissions" as a zip file
  - Submissions are required to be zipped, and must be less than 1MB (File size can change if needed)
- recive notifications from grading server
  - TODO(tell Grading Program contributors how you want this done)

## MySQL Configuration
  - [Download and install MySQL Workbench](http://dev.mysql.com/downloads/file/?id=459897)
    - The installer now includes a MySQL server alongside with it. Choose all of the default options when downloading and installing this.
  - Create a new database
  - Create a new schema in the database, name it "hspc"
  - Add a new table named "teams"
  - Add 3 columns to the "teams" table
	- id INT(10)
	  - Primary Key
	  - Not Null
	  - Unique
	  - Unsigned
	  - Auto Increment
	- team_name VARCHAR(256)
	  - Default/Expression: NULL
	- team_pass VARCHAR(256)
	  - Default/Expression: NULL
  
## Additional Toughts
- TODO
