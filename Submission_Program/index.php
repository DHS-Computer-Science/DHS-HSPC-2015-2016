<?php

include("connections.php");

// Connection was successful

// If the user is not currently logged in navigate them to the login page
if (isset($_COOKIE["n"]) == false || isset($_COOKIE["p"]) == false) {
	header("Location: login.php");
	exit;
}

$username = $_COOKIE["n"];
$password = $_COOKIE["p"];

$stmt = $conn->prepare("SELECT * FROM teams WHERE team_name=?");
$stmt->bind_param("s", $username);
$stmt->execute();
$results = $stmt->get_result();

if ($results->num_rows == 1) {
	while($row = $results->fetch_assoc()) {	
		// Test whether passwords match
		$data = explode("|", $row["team_password"]);
		$salt = $data[0];
		
		$iterations = 1000;
		$hash = hash_pbkdf2("sha256", $password, $salt, $iterations, 32);
		
		if ($hash == $data[1]) {
			header("Location: submissions.php");
		} else {
			header("Location: login.php");
		}
	}
} else {
    header("Location: login.php");
}

$conn->close();
?>
