<?php

if (isset($_GET['file'])) {
    $file = 'examples/' . str_replace('../', '', $_GET['file']);
    if (file_exists($file)) {
        echo file_get_contents($file);
    } else {
        echo 'File not found!';
    }
} else {
    echo 'No file specified!';
}

?>
