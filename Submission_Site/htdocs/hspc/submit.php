<?php
function get_client_ip() {
		$ipaddress = '';
		if (getenv('HTTP_CLIENT_IP'))
				$ipaddress = getenv('HTTP_CLIENT_IP');
		else if(getenv('HTTP_X_FORWARDED_FOR'))
				$ipaddress = getenv('HTTP_X_FORWARDED_FOR');
		else if(getenv('HTTP_X_FORWARDED'))
				$ipaddress = getenv('HTTP_X_FORWARDED');
		else if(getenv('HTTP_FORWARDED_FOR'))
				$ipaddress = getenv('HTTP_FORWARDED_FOR');
		else if(getenv('HTTP_FORWARDED'))
			 $ipaddress = getenv('HTTP_FORWARDED');
		else if(getenv('REMOTE_ADDR'))
				$ipaddress = getenv('REMOTE_ADDR');
		else
				$ipaddress = 'UNKNOWN';
		return $ipaddress;
}

function join_paths() {
		// shamelessly stolen form:
		// http://stackoverflow.com/questions/1091107/how-to-join-filesystem-path-strings-in-php
		$paths = array();

		foreach (func_get_args() as $arg) {
				if ($arg !== '') { $paths[] = $arg; }
		}

		return preg_replace('#/+#','/',join('/', $paths));
}

if (!isset($_FILES["submission"])) {
	header("Location: index.php");
}

include("connections.php");

// Directory settings
$target_dir = "/opt/lampp/submissions/";

// Create a random file name that does not currently exist
do {
	// Generate a random 8 character long filename
	// It might be a better idea to use hashes - such as sha1
	//	 using the php funtion `sha1_file(FILE)`
	//	 but it's too late for that now...
	$filename = "";
	$characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	$charactersLength = strlen($characters);
	for ($i = 0; $i < 8; $i++) {
		$filename .= $characters[rand(0, $charactersLength - 1)];
	}

	// Assign variables regarding the file information
	$sub_dir = join_paths($target_dir . $filename);

} while (file_exists($sub_dir));// works for dirs as well

// File settings
$uploadOk = 1;

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
		echo "Sorry, your file was not uploaded.";
		//header("Location: submissions.php?code=0");
// if everything is ok, try to upload file
}
else
{
	if (isset($_COOKIE["n"]) && isset($_POST["problemNumber"]))
	{
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

			// Check if the team has already submitted the correct solution to this problem
			$stmt2 = $conn->prepare("SELECT * FROM submissions WHERE team_id=? AND problem_id=? AND grade=1");
			$stmt2->bind_param("ii", $team_id, $problem_id);
			$stmt2->execute();
			$res = $stmt2->get_result();
			$row = $res->fetch_assoc();
			if ($row == NULL) {
				// Team IP address
				$team_ip = get_client_ip();

				// Prepared statement for entering the submission
				$stmt = $conn->prepare("INSERT INTO submissions (submission_name, problem_id, team_id, grade, time, submission_ip) VALUES (?, ?, ?, ?, ?, ?)");
				$stmt->bind_param("siiiis", $filename, $problem_id, $team_id, $grade = 0, $time = time(), $team_ip);
				$stmt->execute();

				$success = true;
				echo "<pre>";
				var_dump($_FILES);
				echo "</pre>";
				//if ($_FILES["submission"]["error"] == UPLOAD_ERR_OK) {
						echo "Making directory<br>";
						mkdir($sub_dir, 0777);
						chmod($sub_dir, 0777);
						echo "Moving files<pre>";
						for ($i = 0; $i < count($_FILES["submission"]["name"]); $i++)
						{
							move_uploaded_file($_FILES["submission"]["tmp_name"][$i], join_paths($sub_dir, $_FILES["submission"]["name"][$i]));
							echo join_paths($sub_dir, $_FILES["submission"]["name"][$i]);
							echo "<br>";					
						}
						echo "</pre><br>Files moved";
		/*				foreach ($_FILES["submission"] as $key => $a) {
						$tmp_name = $_FILES["submission"]["tmp_name"][$key];
						$name = $_FILES["submission"]["name"][$key];
						$abcd = join_paths($sub_dir, $name);
						echo $abcd;
						if(!move_uploaded_file($tmp_name, join_paths($sub_dir, $name)))
							$success = false;
						}*/
				//}


				if($success) // I feel like this should be `!$success`
				{
					// Done
					echo "Done - The logic for this submission has completed and the file was uploaded";
					header("Location: submissions.php?code=3");
				}
			}
			else
			{
				// The team has already completed this problem
				echo "Done - User already passed this problem";
				header("location: submissions.php?code=8");
			}	
		}
	else
	{
		header("Location: submissions.php?code=2");
	}
}
?>
