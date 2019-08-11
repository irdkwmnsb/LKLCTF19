<?php

function gen($text, $color = '#EE0000', $meta = 'denied') {
    echo <<<SEP
    <!DOCTYPE html>
    <html>
    <head>
    <title>LKLBank TODO list</title>
    <meta name="flag" content="$meta">
    </head>
    <body>
    <style>
    html {
        height: 100%;
    }
    body {
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: monospace;
        height: 60%;
        font-size: 3em;
        color: $color;
    }
    </style>
    <p>$text</p>
    </body>
    </html>
SEP;
}

$q = 'null';

if (!isset($_COOKIE['s3ssion1d'])) {
    setcookie('s3ssion1d', 'null');
    
} else {
    $q = $_COOKIE['s3ssion1d'];
}
    
switch ($q) {
    case 'test':
    case 'creator':
    case 'admin':
    case 'god':
        gen('Outdated session');
        break;
    case 'lastutf445':
    case 'irdkwmnsb':
        gen('kek', '#0000EE', 'nope');
        break;
    case '@lklbank-4dm1n-1337':
        gen('LKLCTF{h1j4ck_th3_pl4n3_t0n1ght}', '#00BB00', 'internal error');
        break;
    default:
        gen('Unauthorized access');
}

?>
