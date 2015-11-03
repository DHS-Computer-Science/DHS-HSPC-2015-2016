<?php
	if (isset($_COOKIE["n"])) {
		unset($_COOKIE["n"]);
		setcookie("n","",time()-1);
	}
	
	if (isset($_COOKIE["p"])) {
		unset($_COOKIE["p"]);
		setcookie("p","",time()-1);
	}
		
	header("Location: index.php");
?>