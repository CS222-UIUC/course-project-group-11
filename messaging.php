<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "db";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if(!$conn){
    die("Failed to connect with error " . mysqli_connect_error())
}
$sql= "SELECT `user_id`,`user_name` FROM `users` WHERE `user_name` LIKE '%?%'";

$sql = "INSERT INTO messages (message_id, sent_from, sent_to, message_content)
VALUES ('0', 'user_id', 'You', "Hello World!")"; //Did not implement recipient id

if($conn->query($sql) === TRUE){
    echo "Message was saved to database";
} else{
    echo "Failed to save message with error " . $conn->error;
}
?>