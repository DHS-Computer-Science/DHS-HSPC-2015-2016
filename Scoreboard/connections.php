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
		exit;
	} 
?>
