<?php

if (isset($_GET["name"])) {
	
	include("connections.php");

	// Get the username
	$username = $_GET["name"];
	
	// Generate the salt and password
	$password = "";
	$salt = "";
	$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    for ($i = 0; $i < 16; $i++) {
        $password .= $characters[rand(0, $charactersLength - 1)];
    }
	for ($i = 0; $i < 16; $i++) {
        $salt .= $characters[rand(0, $charactersLength - 1)];
    }
	
	// Hash the password with the salt
	$iterations = 1000;
	$hash = hash_pbkdf2("sha256", $password, $salt, $iterations, 32);
	
	// Combine the salt and hash for the database
	$teampass = $salt."|".$hash;
	
	// SQL query for entering the username and teampass into the database
	$sql = "INSERT INTO teams (team_name, team_password)
			VALUES ('$username', '$teampass')";
	
	// Display the password, salt, hash, and the teampass
	echo "Password: ".$password."<br>Salt: ".$salt."<br>Hash: ".$hash."<br>Teampass: ".$teampass;
	
	// Display a status message
	if ($conn->query($sql) == TRUE) {
		echo "<br>User added";
	} else {
		echo "<br>".$conn->error;
		exit;
	}
	
} else {
	die("No \"name\" parameters supplied");
	exit;
}

?>