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
							echo "						<th colspan = \"2\">Problem ".$i."</th>\n";
						}
						echo "					</tr>";
						echo "					<tr>";
						echo "						<th colspan=\"3\"></th>";
				
						for ($i = 1; $i <= $number_of_problems; $i++) {
							echo "						<th>Attempts</th>\n";
							echo "						<th>Time</th>\n";
						}
						echo "					</tr>";
					
						// First get the teams in order and store them into a PHP array
							// This array will then be looped in the correct order and the data will be parsed
						
						// Get all of the team_ids and team_names
						// Does not need to be a prepared statement because we are not inputting any values
						$sql = "SELECT team_id, team_name FROM teams";
						$result = $conn->query($sql);
					
						// Create an array of team_ids
						$teams = array();
						while ($t = $result->fetch_assoc()) {
							array_push($teams, $t);
						}
						/* This will not display the teams in ascending order of total time.
							How do we want to go about doing this?
							I think we could either:
								- Create a team class that stores all the data
								- Store all the data into a multidimensional array (Dictionary?)
						*/
						
						// Here's my attempt at a class
						// Amazing isn't it?
						// (It's more like a struct)
						class TeamData {
							public $total_time = 0;
							public $completed = 0;
							public $html_data = "";
						}
						
						class GroupOfTeams {
							// Publicly accessible variable for an array of teams
							public $teams = array();
							
							// At first this methof was suppose to just get the $teams variable (defined above)
							// But it was having a hissy fit and thought $teams (When I knew it wasn't) was a null value
							// This method technically doesn't need to be in here now, but whatever
							function order($t) {
								usort($t, function($a, $b) {
									if($a->total_time == $b->total_time){ return 0 ; }
									return ($a->total_time) ? 1 : -1;
								});
								
								return $t; // Return the sorted array
							}
						}
						
						$teamsWithData = array();
						
						foreach ($teams as $team) {
							// TeamData class for this class
							$teamData = new TeamData();
							
							// HTML data for this team
							$html_data = "";
							
							// Add a row for each team
							$html_data .= "					<tr>";

							// Set default values for variables
							$table          = "";
							$total_time     = 0;
							$complete       = "";
							$complete_count = 0;
							
							// For loop that repeates 6 times for the 6 problems we have
							// This line was made to start at 1 and end at $number)of_problems+1
								// This is because the problem ids start at 1, instead of 0
									// This is because the submission page uses a "problem number" of 0 as "problem not selected"
								
							for ($problem_id = 1; $problem_id <= $number_of_problems; $problem_id++) {
								$num_submissions = 0;
								
								// Get all the submission data for each problem for each time
								$stmt = $conn->prepare("SELECT * FROM submissions WHERE team_id=? AND problem_id=?");
								$stmt->bind_param("si", $team["team_id"], $problem_id); // Bind only the team_id of the $team object to the SQL statement
								$stmt->execute();
								$res = $stmt->get_result();
								$problem_time = 0;
								while($row = $res->fetch_assoc()) {
									$num_submissions++; // Increase the number of submission to display for this problem
									
									if($row['grade'] === 1) {
										$complete_count++;
										// Set the problem time to the time of the completed attempt
										//	 then add penalty time for all incorrect submissions
										$problem_time      = ($row['time'] - $start_time);
										$problem_time     += (($num_submissions-1)*$penalty_time);
										$total_time += $problem_time;// Then add on to the total team time
									}
								}
								$table .= "						<td>".$num_submissions."</td>\n";
								$table .= "						<td>".gmdate("H:i:s", $problem_time)."</td>\n";
							}
							$html_data .= "						<td>".$team["team_name"]."</td>\n"; // Extract the team_name value from the $team array object
							$html_data .= "						<td>".$complete_count."/";
							$html_data .= "$total_time.</td>\n";
							$html_data .= $table;
							$html_data .= "					</tr>";

							// Set the $teamData object variables
							$teamData->html_data  = $html_data;
							$teamData->total_time = $total_time;
							$teamData->completed  = $complete_count;

							// Add the $teamData object to an array of $teamData objects
							array_push($teamsWithData, $teamData);
						}
						
						// Now that we have them sorted by time, we need to actually sort them in a specific order
							// 1. Sort by # problems completed
							// 2. Group all teams that have the same # problems completed into an array (Multiple arrays will be created)
							// 3. Sort each array by time
						// This is because if a team submits only 1 problem in 10 minutes, and never submits another, they'll appear as the first place forever
						// Scoreboard currently shows simply based on total_time, needs to be based on problems_completed(sub((total_time))
						
						// Put all the teamdata objects that have the same amount of completed problems into an array
						// Keep this order! (6 -> 0) it helps organization later!
						// Being in this order "sorts" the problems for us from (largest number of problems compelted) to (smallest number of problems completed)
						
						//Using a for loop to populate, in case # of problems changes later...
						$groups = array();
						for($i = $number_of_problems; $i >= 0; $i--) {
							array_push($groups, "".$i => array());
						}
						
						// Put the teamData objects into an array with all other teamData objects that have the same number of completed problems
						foreach ($teamsWithData as $team) {
							array_push($groups[$team->completed], $team);
						}
						
						// Create an array of groups of teams (Wow)
						$AllGroupOfTeams = array();
						
						// Create GroupOfTeam objects that store the array we created earlier and put them into the AllGroupOfTeams array
						foreach ($groups as $group) {
							$newGroup = new GroupOfTeams();
							$newGroup->teams = $group;
							array_push($AllGroupOfTeams, $newGroup);
						}
						
						// Go through each GroupOfTeams, order its data from smallest to largest time, and then echo their html_data
						foreach ($AllGroupOfTeams as $group) {
							$orderedGroup = $group->order($group->teams);
							foreach ($orderedGroup as $team) {
								echo $team->html_data;
							}
						}
						
						// Keeping this here in case needed at a later time?
						/*
						// Sort the $teamsWithData array based on the total time, with smaller total_times having smaller indexes
						usort($teamsWithData, function($a, $b) {
							if($a->total_time == $b->total_time){ return 0 ; } // Teams have the same score (Extremely low odds, amazing huh?)
							return ($a->total_time) ? 1 : -1;
						});
						
						// Print the sorted teamData object html_data values to display the scoreboard
						foreach ($teamsWithData as $teamData) {
							echo $teamData->html_data;
						}
						*/
					?>
				</table>
			</div>
		</div>
	<body>
</html>
