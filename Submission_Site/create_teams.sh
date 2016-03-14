#!/bin/bash

printf "Enter team name(blank to exit): "
read username
while [ ! -z "$username" ] ; do
echo " <?php
\$servername = \"localhost\";
\$connusername = \"root\";
\$connpassword = \"andriy2432\";

// Create connection
\$conn = new mysqli(\$servername, \$connusername, \$connpassword, \"hspc\");

// Check connection
if (\$conn->connect_error) {
  die(\"Connection failed: \" . \$conn->connect_error);
  echo \"Could not connect\\n\";
  exit;
}
\$username = \"$username\";
\$password = \"\";
\$salt = \"\";
\$characters = \"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\";
\$charactersLength = strlen(\$characters);
for (\$i = 0; \$i < 16; \$i++) {
  \$password .= \$characters[rand(0, \$charactersLength - 1)];
}
for (\$i = 0; \$i < 16; \$i++) {
  \$salt .= \$characters[rand(0, \$charactersLength - 1)];
}

// Hash the password with the salt
\$iterations = 1000;
\$hash = hash_pbkdf2(\"sha256\", \$password, \$salt, \$iterations, 32);

// Combine the salt and hash for the database
\$teampass = \$salt.\"|\".\$hash;

// SQL query for entering the username and teampass into the database
\$sql = \"INSERT INTO teams (team_name, team_password)
    VALUES ('\$username', '\$teampass')\";

// Display the password, salt, hash, and the teampass
echo \"Username: \".\$username.\"\\nPassword: \".\$password;
// Display a status message
if (\$conn->query(\$sql) == TRUE) {
  echo \"\\nUser added\\n\\n\";
} else {
  echo \"\\n\".\$conn->error.\"\\n\\n\";
  exit;
}" | php -f /dev/stdin | tee -a "users"
printf "Enter team name(blank to exit): "
read username
done