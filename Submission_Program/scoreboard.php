<?php
	include("connections.php");
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
			<?php
				// This is here all of the work needs to be done
				
				// First get the teams in order and store them into a PHP array
					// This array will then be looped in the correct order and the data will be parsed
					
				// Get all of the team_ids
				$sql = "SELECT team_id FROM teams";
				$result = $conn->query($sql);
				
				// Create an array of team_ids
				$teams = $result->fetch_array(MYSQLI_NUM);
				
				foreach ($teams as $team) {
					$stmt = $conn->prepare("SELECT * FROM submissions WHERE team_id=?");
					$stmt->bind_param("s", $team);
					$stmt->execute();
					$res = $stmt->get_result();
					$row = $res->fetch_assoc();
					echo print_r($row);
				}
			?>
		</div>
	<body>
</html>