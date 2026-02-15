<?php
// FILE: api/db.php
$servername = "localhost";
$username = "root";
$password = ""; 
$dbname = "chickenarium"; // <--- ETO ANG CORRECT DATABASE MO

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    // Return JSON error kapag hindi maka-connect
    header('Content-Type: application/json');
    die(json_encode(["status" => "error", "message" => "DB Connection Failed: " . $conn->connect_error]));
}
?>