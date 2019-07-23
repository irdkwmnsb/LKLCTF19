<!DOCTYPE html>
<html>
<head>
<title>LKL-Bank auth system v0.1</title>
<meta name="flag" content="lol">
</head>
<body>
<style>
html {
    height: 100%;
}
body {
    display: flex;
    height: 60%;
    flex-flow: column;
    justify-content: center;
    align-items: center;
}
</style>


<?php

if (!isset($_GET['login']) || !isset($_GET['pass'])) {
    echo "<p>LKL-Bank auth system v0.1</p><br>";
    echo "<form method='get' action='/'>";
    echo "<input name='login' placeholder='Login'><br>";
    echo "<input name='pass' type='password' placeholder='Password'><br>";
    echo "<button type='submit'>Enter</button>";
    echo "</form>";
    exit();
}

$login = $_GET['login'];
$pass = $_GET['pass'];

if ($login != 'irdkwmnsb' || $pass != 'qwerty') {
    echo "Invalid login or password";
    exit();
}

echo "<p>Access granted</p>";
echo "<p>LKLCTF{17dkwmn56_d035n7_u53_9w3777_dud3}</p>";

?>

</body>
</html>
