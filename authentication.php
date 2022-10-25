<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "db";

$conn = mysqli_connect($servername, $username, $password, $dbname);

//checks that a connection was successful
if(!$conn){
    die("Failed to connect with error " . mysqli_connect_error())
}



//creates a new MySQL table that stores a message id, the sender, the recipient, and the actual message content.
$sql = "CREATE TABLE `messages` ( 
    `message_id` INT(11) NOT NULL AUTO_INCREMENT, 
    `sent_from` INT(11) NOT NULL, 
    `sent_to` INT(11) NOT NULL, 
    `messageContent` TEXT, 
    PRIMARY KEY (`message_id`) 
)"; 

if(mysqli_query($conn, $sql)){
    echo "SQL table created";
} else{
    echo "Failed to create table with error " . mysqli_error($conn);
}

mysqli_close($conn);
?>