<?php

// Connection variables
$servername = "localhost";
$connusername = "root";
$connpassword = "password";

// Create connection
$conn = new mysqli($servername, $connusername, $connpassword, "hspc");

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

// Connection was successful

// If the user is not currently logged in navigate them to the login page
if (isset($_COOKIE["n"]) == false || isset($_COOKIE["p"]) == false) {
	header("Location: login.php");
	exit;
}

$username = $_COOKIE["n"];
$password = $_COOKIE["p"];

$sql = "SELECT * FROM teams WHERE team_name='$username'";

$results = $conn->query($sql);

if ($results->num_rows == 1) {
	while($row = $results->fetch_assoc()) {	
		// Test whether passwords match
		$data = explode("|", $row["team_password"]);
		$salt = $data[0];
		
		$iterations = 1000;
		$hash = hash_pbkdf2("sha256", $password, $salt, $iterations, 32);
		
		if ($hash == $data[1]) {
			// We're already here!
		} else {
			header("Location: login.php");
		}
	}
} else {
    header("Location: login.php");
}

$conn->close();
?>

<html>
	<head>
		<link rel="stylesheet" type="text/css" href="styles.css">
	</head>
	<body>
		<div id="header">
			<div class="navbutton">
				LCPS HSPC
			</div>
		</div>
		<div id="logout">
			<a href="logout.php">Logout</a>
		</div>
		<div id="content" style="display: inline-block; text-align: center;">
			<br>
			<div id="small">
				<?php
					if (isset($_GET["code"])) {
						$code = $_GET["code"];
						if ($code == 0) {
							// Invalid file type (.zip needed)
							echo "<h5 class='text'>Invalid file type.<br>Please use a .zip</h5><hr>";
						} else if ($code == 1) {
							// File too large (1MB max)
							echo "<h5 class='text'>File size must be less than 1MB</h5><hr>";
						} else if ($code == 2 ) {
							// Unknown error
							echo "<h5 class='text'>Could not upload the file</h5><hr>";
						} else if ($code == 3 ) {
							// Unknown error
							echo "<h5 class='text'>File uploaded</h5><hr>";
						}
					}
				?>
				<form action="submit.php" method="post" enctype="multipart/form-data">
					<input type="file" name="submission" id="submission" class="noborder text">
					<br>
					<input class="hover" type="submit" value="Submit">
				</form>
			</div>
		</div>
	<body>
</html>