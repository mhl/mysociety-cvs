<?

$u = $_GET['u'];
$file = file_get_contents($u);
header('Content-Type: image/png');
print $file;

