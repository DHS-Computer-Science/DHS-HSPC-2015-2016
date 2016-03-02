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

// Prepared statement for getting the data associated with the stored username
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
				<a href="scoreboard.php">LCPS HSPC</a>
			</div>
		</div>
		<div id="logout">
			<a href="logout.php">Logout</a>
		</div>
		<div id="content" style="display: inline-block; text-align: center;">
			<br>
			<div id="small">
				<h5 class="text">Problem Submissions</h5>
				<hr>
				<div id="errorMessages">
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
				</div>
				<div id="noFileErrorMessage"></div>
				<script>
					function checkSelect() {
						var selectObject = document.getElementById("problemNumberSelect");
						var selectValue = selectObject.options[selectObject.selectedIndex].value;
						var errorMessages = document.getElementById("errorMessages");
						errorMessages.innerHTML = "";
						if (selectValue == 0) {
							errorMessages.innerHTML = "<h5 class='text'>Please select a problem number</h5><hr>";
							return false;
						} else {
							errorMessages.innerHTML = "";
							return true;
						}
					}
					function doSubmit() {
						if (checkSelect() == true) {
							if (document.getElementById("submission").files.length == 1) {
								document.getElementById("submitForm").submit();
							} else {
								document.getElementById("noFileErrorMessage").innerHTML = "<h5 class='text'>Please select a file</h5><hr>";
							}
						}
					}
				</script>
				<form action="submit.php" method="post" enctype="multipart/form-data" id="submitForm">
					<input type="file" name="submission" id="submission" class="noborder text" required>
					<br>
					<select name="problemNumber" style="width:100%; margin-top:8px; margin-bottom:8px; padding:8px;" id="problemNumberSelect" onchange="checkSelect()">
						<option value="0" selected disabled hidden>Please choose a problem</option>
						<option value="1">Problem 1</option>
						<option value="2">Problem 2</option>
						<option value="3">Problem 3</option>
						<option value="4">Problem 4</option>
						<option value="5">Problem 5</option>
						<option value="6">Problem 6</option>
					<select>
					<br>
					<hr>
					<input class="hover" type="button" onClick="doSubmit()" value="Submit">
				</form>
			</div>
		</div>
	<body>
</html>