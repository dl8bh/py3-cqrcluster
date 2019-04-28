<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE); ini_set('display_errors', '1');
include("config.php");
include("inc/db.php");
$database_connection = new cqrdb($db_hostname, $db_username, $db_password, $db);
print_r ($database_connection->get_bands());
?>