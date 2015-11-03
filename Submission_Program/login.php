<?php

if (isset($_POST["teamname"]) && isset($_POST["password"]) && isset($_GET["action"])) {
	$teamname = $_POST["teamname"];
	$password = $_POST["password"];
	$action = $_GET["action"];
	
	if (strcasecmp($action, "login") == 0) {
		// Perform login attempt
		
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

		// The query
		$sql = "SELECT * FROM teams WHERE team_name='$teamname'";

		// Perform the query
		$results = $conn->query($sql);
	
		// If we got at least 1 result back
		if ($results->num_rows == 1) {
			while($row = $results->fetch_assoc()) {
				
				// Test whether passwords match
				$data = explode("|", $row["team_password"]);
				$salt = $data[0];
				
				$iterations = 1000;
				$hash = hash_pbkdf2("sha256", $password, $salt, $iterations, 32);
				
				if ($hash == $data[1]) {
					// Create a cookie
					// While not the safest approach because the user 
					// can view the cookie, this should be fine
					// Using 1 letter names for "better" security
					setcookie("n", $teamname, mktime()+60*60*5); // 60 seconds, times 60 minutes, times 5 hours
					setcookie("p", $password, mktime()+60*60*5);
					
					// Navigate to submissions page
					header("Location: submissions.php");
				} else {
					header("Location: login.php?action=error");
				}
			}
		} else {
			header("Location: login.php?action=error");
		}
		$conn->close();
	}
}

/* Hashing functions. Salting was done differently for usernames and passwords due to incorrect db encoding
$password = "password";
$iterations = 1000;

$salt = mcrypt_create_iv(16, MCRYPT_DEV_URANDOM);

$hash = hash_pbkdf2("sha256", $password, $salt, $iterations, 32);
echo $salt."|".$hash;
*/

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
		<div id="content" style="display: inline-block; text-align: center;">
			<div id="small">
				<h4 class="text"> Login </h4>
				<hr>
				<?php
					if (isset($_GET["action"])) {
						if ($_GET["action"] == "error") {
							echo "<h5 class='text'>Invalid username or password</h5><hr>";
						}
					}
				?>
				<form action="login.php?action=login" method="post">
					<input type="text" name="teamname" placeholder="Team Name">
					<br>
					<input type="text" name="password" placeholder="Password">
					<br>
					<input class="hover" type="submit" value="Submit">
				</form>
			</div>
		</div>
	<body>
</html>