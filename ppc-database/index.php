<?php

echo '<form method="get" action=""><input name="login" placeholder="Login"/><input name="pass" type="pass" placeholder="Password"/><input type="submit"></form>';

if (!isset($_GET['login']) || !isset($_GET['pass'])) {
    echo "Login and password shouldn't be empty\n";
    exit();
}

$login = $_GET['login'];
$pass = $_GET['pass'];

if ($login != 'irdkwmnsb' || $pass != 'qwerty') {
    echo "Invalid login or password\n";
    exit();
}

echo "Access granted\nLKLCTF{17dkwmn56_d035n7_u53_9w3777_dud3}\n";

?>
