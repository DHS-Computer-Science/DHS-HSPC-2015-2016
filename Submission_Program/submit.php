<?php
if (!isset($_FILES["submission"])) {
	header("Location: index.php");
}

$target_dir = "C:/xampp/submissions/";
$target_file = $target_dir . basename($_FILES["submission"]["name"]); // File name needs to be assigned here. This needs configuration
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);

// Not needed because we will assign the names
// Check if file already exists
//if (file_exists($target_file)) {
//    echo "Sorry, file already exists.";
//    $uploadOk = 0;
//}

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
        header("Location: submissions.php?code=3");
    } else {
        header("Location: submissions.php?code=2");
    }
}

header("Location: index.php");
?>