<?php
	include("connections.php");
?>
<html>
	<head>
		<meta http-equiv="refresh" content="30" />
		<link rel="stylesheet" type="text/css" href="styles.css">
	</head>
	<body>
		<div id="header">
			<div class="navbutton">
				LCPS HSPC
			</div>
		</div>
		<div id="content" style="display: inline-block; text-align: center;">
			<div class="text">
			<?php
				// This is here all of the work needs to be done
				
				// First get the teams in order and store them into a PHP array
					// This array will then be looped in the correct order and the data will be parsed
					
				// Get all of the team_ids
				// Does not need to be a prepared statement because we are not inputting any values
				$sql = "SELECT team_id FROM teams";
				$result = $conn->query($sql);
				
				// Create an array of team_ids
				$teams = $result->fetch_array(MYSQLI_NUM);
				
				foreach ($teams as $team) {
					// For loop that repeates 6 times for the 6 problems we have
					for ($problem_id = 0; $problem_id < 5; $problem_id++) {
						// Get all the submission data for each problem for each time
						$stmt = $conn->prepare("SELECT * FROM submissions WHERE team_id=? AND problem_id=?");
						$stmt->bind_param("si", $team, $problem_id);
						$stmt->execute();
						$res = $stmt->get_result();
						while($row = $res->fetch_assoc()) {
							// Each row is a different submission for this problem, for this team.
							echo print_r($row) . "<hr>";
						}
					}
				}
			?>
			</div>
		</div>
	<body>
</html>