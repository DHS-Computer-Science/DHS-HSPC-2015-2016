<?php
	include("connections.php");

	// If the user is not currently logged in navigate them to the login page
	if (isset($_COOKIE["n"]) == false || isset($_COOKIE["p"]) == false) {
		header("Location: login.php");
		exit;
	}
?>
<html>
	<head>
		<meta http-equiv="refresh" content="30" />
		<link rel="stylesheet" type="text/css" href="styles.css">
	</head>
	<body>
		<div id="header">
			<div class="navbutton">
				<a href="submissions.php">LCPS HSPC</a>
			</div>
		</div>
		<div id="content" style="display: inline-block; text-align: center; width: 95%; margin-left: 2.5%">
			<div class="text">
				<br>
				<table>
				<tr>
					<th>Team</th>
					<th>Completed</th>
					<th>Total Time</th>
					<?php
						// Create 2 header rows:
						// Team | Done | Time |      P1     |      P2     | ...
						//                    | Trys | Time | Trys | Time | ...
						$number_of_problems = 6;
						$penalty_time       = 600; // TODO - set penalty time - in seconds
						
						$start_time = 0;
						
						$stmt = $conn->prepare("SELECT value FROM data WHERE name=?");
						$stmt->bind_param("s", $param = "start_time");
						$stmt->execute();
						$results = $stmt->get_result();

						if ($results->num_rows == 1) {
							$row = $results->fetch_assoc();
							$start_time = $row["value"];
						}
						
						for ($i = 1; $i <= $number_of_problems; $i++) {
							echo "<th colspan = \"2\">Problem ".$i."</th>\n";
						}
						echo "</tr>";
						echo "<tr>";
						echo "<th colspan=\"3\"></th>";
				
						for ($i = 1; $i <= $number_of_problems; $i++) {
							echo "<th>Attempts</th>\n";
							echo "<th>Time</th>\n";
						}
						echo "</tr>";
					
						// First get the teams in order and store them into a PHP array
							// This array will then be looped in the correct order and the data will be parsed
						
						// Get all of the team_ids
						// Does not need to be a prepared statement because we are not inputting any values
						$sql = "SELECT team_id FROM teams";
						$result = $conn->query($sql);
					
						// Create an array of team_ids
						$teams = array();
						while ($t = $result->fetch_assoc()) {
							array_push($teams, $t["team_id"]);
						}
						/* This will not display the teams in ascending order of total time.
							How do we want to go about doing this?
							I think we could either:
								- Create a team class that stores all the data
								- Store all the data into a multidimensional array (Dictionary?)
						*/
						
						// Here's my attempt at a class
						// Amazing isn't it?
						class TeamData {
							public $total_time = 0;
							public $html_data = "";
						}
						
						$teamsWithData = array();
						
						foreach ($teams as $team) {
							// TeamData class for this class
							$teamData = new TeamData();
							
							// HTML data for this team
							$html_data = "";
							
							// Add a row for each team
							$html_data .= "<tr>";
						  
							// Set default values for variables
							$table      = "";
							$total_time = 0;
							$complete   = "";
							
							// For loop that repeates 6 times for the 6 problems we have
							// TODO - may need to make next line "$number_of_problems-1" instead of "$number_of_problems"
							// This line was made to start at 1 and end at $number)of_problems+1
								// This is because the problem ids start at 1, instead of 0
									// This is because the submission page uses a "problem number" of 0 as "problem not selected"
								// If $problem_id started at 0, and went to $number_of_problems then the data for problem 1 would appear under problem 2 and so on
								
							for ($problem_id = 1; $problem_id < $number_of_problems + 1; $problem_id++) {
								$num_submissions = 0;
								
								// Get all the submission data for each problem for each time
								$stmt = $conn->prepare("SELECT * FROM submissions WHERE team_id=? AND problem_id=?");
								$stmt->bind_param("si", $team, $problem_id);
								$stmt->execute();
								$res = $stmt->get_result();
								$problem_time = 0;
								while($row = $res->fetch_assoc()) {
									$num_submissions++; // Don't touch
									
									if($row['grade'] === 1) {// TODO - fix this line to if the grade value is 1
										$complete = $complete . $problem_id . ", ";
										//Yes the next three lines go here
										$problem_time       = ($row['time'] - $start_time); // TODO - get time for this problem in seconds
										$problem_time      += (($num_submissions-1)*$penalty_time); // I touched this. Was this suppose to be +=?
											// If you had 1 submission it would do *= (1-1)*600 which would be *= (0)*600 which is 0...so it resets the time to 0
										$total_time += $problem_time;
									}
								}
								$table .= "<td>".$num_submissions."</td>\n";
								$table .= "<td>".gmdate("H:i:s", $problem_time)."</td>\n";
							}
							$html_data .=  "<td>".$_COOKIE["n"]."</td>\n"; // This needs to change. Every team name on the scoreboard will appear as the logged in teams name.
							$html_data .=  "<td>".substr($complete, 0, strlen($complete)-2)."</td>\n";  // Substring to cut off the last ", "
							$html_data .=  "<td>".gmdate("H:i:s", $total_time)."</td>\n";
							$html_data .=  $table;
							$html_data .=  "</tr>";
							
							$teamData->html_data = $html_data;
							$teamData->total_time = $total_time;
							
							array_push($teamsWithData, $teamData);
						}
						
						usort($teamsWithData, function($a, $b)
						{
							return strcmp($b->total_time, $a->total_time); // Lowest to greatest
						});
						
						foreach ($teamsWithData as $teamData) {
							// Calculate the winner here using
							// $teamData->total_time
							// To get the total time of a team in seconds (This is not formatted into H:i:s, it is in seconds)
							echo $teamData->html_data;
						}
					?>
				</table>
			</div>
		</div>
	<body>
</html>
