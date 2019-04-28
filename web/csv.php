<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE); ini_set('display_errors', '1');
include("config.php");
include("inc/db.php");
include("inc/http.php");

$headers = new http_helper($_GET, array());
$cqrdb = new cqrdb($db_hostname, $db_username, $db_password, $db);
$entry_list = $cqrdb->get_last_n_lines($headers->get_limit(), $cqrdb->band_to_id($headers->get_band()), $cqrdb->mode_to_id($headers->get_mode()), $headers->get_skimmer(),  $cqrdb->source_to_id($headers->get_source()));
foreach ($entry_list as $entry)
{
    echo 
    $entry["DE_CALL"] 
    . "^" . $entry["QRG"] 
    . "^" . $entry["DX_CALL"] 
    . "^" . $entry["BAND"] 
    . "^" . $entry["MODE"] 
    . "^" . $entry["COMMENT"]
    . "^" . $entry["SPEED"] 
    . "^" . $entry["DB"]  
    . "^" . $entry["timestamp"]
    . "^" . (int)$entry["skimmer"]
    . "^" . $cqrdb->id_to_source($entry["source"])
    
    .  "\n";
}
?>