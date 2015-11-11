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
	      <table>
	        <tr>
	          <th>Team</th>
            <th>Done</th>
            <th>Total Time</th>
			    <?php
			      // Create 2 header rows:
			      // Team | Done | Time |      P1     |      P2     | ...
			      //                    | Trys | Time | Trys | Time | ...
				    $number_of_problems = 6;
				    $penalty_time       = 600; // TODO - set penalty time - in seconds
            
            for ($i=1; $i<=$number_of_problems; $i++) {
              echo "            <th colspan = \"2\">Problem ".$i."</th>\n";
            }
            echo "          </tr>";
            echo "          <tr>";
            echo "            <th colspan = "3"></th>";
            
            for ($i=1; $i<=$number_of_problems; $i++) {
              echo "            <th>Trys</th>\n";
              echo "            <th>Time</th>\n";
            }
            echo "          </tr>";
				
				    // First get the teams in order and store them into a PHP array
					    // This array will then be looped in the correct order and the data will be parsed
					
				    // Get all of the team_ids
				    // Does not need to be a prepared statement because we are not inputting any values
				    $sql = "SELECT team_id FROM teams";
				    $result = $conn->query($sql);
				
				    // Create an array of team_ids
				    $teams = $result->fetch_array(MYSQLI_NUM);
				
				    foreach ($teams as $team) {
				      // Add a row for each team
				      echo "          <tr>";
				      
				      // Set default values for variables 
				      $table      = "";
				      $total_time = 0;
              $complete   = 0;
					    
					    // For loop that repeates 6 times for the 6 problems we have
					    // TODO - may need to make next line "$number_of_problems-1" instead of "$number_of_problems"
					    for ($problem_id = 0; $problem_id < $number_of_problems; $problem_id++) {
						    $num_submissions = 0;
						    
						    // Get all the submission data for each problem for each time
						    $stmt = $conn->prepare("SELECT * FROM submissions WHERE team_id=? AND problem_id=?");
						    $stmt->bind_param("si", $team, $problem_id);
						    $stmt->execute();
						    $res = $stmt->get_result();
						    while($row = $res->fetch_assoc()) {
							    $num_submissions++; // Don't touch
							    
							    $team_name  = ""; // TODO - get team name
							    $time       = 0;  // Don't touch
							    if($res['grade'] === 1) {// TODO - fix this line to if the grade value is 1
							      $complete++;
							      //Yes the next three lines go here
							      $time       = $res['time']; // TODO - get time for this problem in seconds
							      $time      *= ($num_submissions-1)*$penalty_time; // Don't touch
							      $total_time = 0;
							    }
						    }
						    $table .= "            <td>".$num_submissions."</td>\n";
                $table .= "            <td>".gmdate("H:i:s", $time)."</td>\n";
					    }
					    echo "            <td>".$complete."</td>\n";
              echo "            <td>".gmdate("H:i:s", $total_time)."</td>\n";
              echo $table;
				      echo "          </tr>";
				    }
			    ?>
	      </table>
			</div>
		</div>
	<body>
</html>
