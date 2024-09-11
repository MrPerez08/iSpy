<?php
$servername = "localhost";
$username = "root";
$password = getenv(""); 
$dbname = "userinput";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $inp = $_POST['userInput']; // Get the user input from the form
    $link = $_POST['server-link']; // Get the user input from the form
    $description = $_POST['context-desc']; // Get the description

    // Prepare and bind SQL statement
    $stmt = $conn->prepare("INSERT INTO storage (predator_un, server_link, incident_desc) VALUES (?,?,?)");
    $stmt->bind_param("sss", $inp, $link, $description);

    // Execute statement
    if ($stmt->execute()) {
        header("Location: Final.html");
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
