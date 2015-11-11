<?php
if (!isset($_FILES["submission"])) {
	header("Location: index.php");
}

include("connections.php");

// Directory settings
$target_dir = "C:/xampp/submissions/";

// Create a random file name that does not currently exist
do {
	// Generate a random 8 character long filename
	$filename = "";
	$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	$charactersLength = strlen($characters);
	for ($i = 0; $i < 8; $i++) {
		$filename .= $characters[rand(0, $charactersLength - 1)];
	}

	// Asign variables regarding the file information
	$target_file = $target_dir . $filename . ".zip";
	
} while (file_exists($target_file));

// File settings
$uploadOk = 1;
$imageFileType = pathinfo($target_file, PATHINFO_EXTENSION);

// Check file size
if ($_FILES["submission"]["size"] > 1000000) {
    header("Location: submissions.php?code=1");
    $uploadOk = 0;
}
// Allow certain file formats
if($imageFileType != "zip") {
    header("Location: submissions.php?code=0");
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["submission"]["tmp_name"], $target_file)) {
		// Get the team name
		if (isset($_COOKIE["n"]) && isset($_POST["problemNumber"])) {
			$teamname = $_COOKIE["n"];
			
			// Prepared statement for getting the id of the user
			$stmt = $conn->prepare("SELECT team_id FROM teams WHERE team_name=?");
			$stmt->bind_param("s", $teamname);
			$stmt->execute();
			$res = $stmt->get_result();
			$row = $res->fetch_assoc();
			
			// Team ID
			$team_id = $row["team_id"];
			$problem_id = $_POST["problemNumber"];
	
			// Prepared statement for entering the submission
			$stmt = $conn->prepare("INSERT INTO submissions (submission_name, problem_id, team_id, grade, time) VALUES (?, ?, ?, ?, ?)");
			$stmt->bind_param("siiii", $filename, $problem_id, $team_id, $grade = 0, $time = time());
			$stmt->execute();
			
			header("Location: submissions.php?code=3");
		}
    } else {
        header("Location: submissions.php?code=2");
    }
}
?>