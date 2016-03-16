# Submission Program

## Contributors
- Noah Davis
- Andriy Zasypkin(a very tiny bit)

## Dependencies
- lampp(or xampp if on *dos*)
  - apache
  - php
  - mysql
- should be istalled using installer scipt

## Installation
- Run the install script in this dir (`sudo ./install.sh`)
  on a debian based machine (like a computer running ubuntu)
  - This only needs to be done once
  - And it should already have been done
- Now run the setup script in this dir (`sudo ./setup.sh`)
  - This will need to be run once per competition
- To add teams run `./create_teams.sh`
- Make sure to change the timesptamp in /var/www/html/hspc/scoreboard.php
  - Set it to the competition start time, as the number of seconds
    since the epoch(1970-01-01T00:00:00)
  - Be sure to acount for time zones
  - *Should you fail to do so, the scoreboard time will be wacky*

## Running
- reboot, maybe?
  - if not running
- or wait
