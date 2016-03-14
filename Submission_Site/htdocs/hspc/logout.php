<?php
	
	// Unset and expire the cookie
	if (isset($_COOKIE["n"])) {
		unset($_COOKIE["n"]);
		setcookie("n","",time()-1);
	}
	
	// Unset and expire the cookie
	if (isset($_COOKIE["p"])) {
		unset($_COOKIE["p"]);
		setcookie("p","",time()-1);
	}
	
	// Navigate to the index page, it will handle redirections
	header("Location: index.php");
?>