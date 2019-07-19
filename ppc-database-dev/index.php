<?php

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

echo "LKLCTF{17dkwmn56_d035n7_u53_9w3777_dud3}\n";

?>
