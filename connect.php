<?php
$servername = "localhost";
$username = "root";
$password = getenv("CodeMaster$01"); 
$dbname = "userinput";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $link = $_POST['userInput']; // Get the user input from the form

    // Prepare and bind SQL statement
    $stmt = $conn->prepare("INSERT INTO storage (server_link) VALUES (?)");
    $stmt->bind_param("s", $link);

    // Execute statement
    if ($stmt->execute()) {
        echo "Server Link Captured Successfully...";
    } else {
        echo "Error: " . $stmt->error;
    }

    // Close statement and connection
    $stmt->close();
    $conn->close();
} else {
    echo "No data received.";
}
?>

