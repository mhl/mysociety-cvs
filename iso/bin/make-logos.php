#!/usr/bin/php -d display_errors=On
<?

$array = array(
    array(48, 'Mapumental', 'title', 'lightblue'),
    array(48, 'Mapumental', 'title-orange', 'orange'),
    array(40, 'Mapumental', 'title-small', 'lightblue'),
    array(40, 'Mapumental', 'title-small-orange', 'orange'),
    array(20, 'How far will you go?', 'subtitle', 'lightblue'),
);

foreach ($array as $row) {
    generate($row[0], $row[1], $row[2], $row[3]);
}

`convert logo.jpg -fuzz 60% -transparent white -fill white -opaque black -resize 160x160 logo-c4.png`;
`convert logo.jpg -fuzz 60% -transparent white -fill white -opaque black -resize 80x80 logo-c4-small.png`;

function generate($size, $text, $out, $col) {
    $font = "../../C4HeaReg.ttf";

    $extraW = floor(0.4 * $size);

    $descenders = false;
    if (preg_match('#[gjpqy]#', $text))
        $descenders = true;

    $box = imagettfbbox($size, 0, $font, $text);
    $minx = $box[0]; $maxx = $box[2];
    $maxy = $box[1]; $miny = $box[5];
    $bbwidth = $maxx - $minx;
    $bbheight = $maxy - $miny;
    $width = $bbwidth + $extraW;
    $height = $bbheight;
    if ($descenders) {
        $height += floor(0.6 * $size);
    }

    $image = imagecreatetruecolor($width, $height);
    #imagealphablending($image, false);
    #imagesavealpha($image, true);
    #$trans = imagecolorallocatealpha($image, 255, 255, 255, 127);

    $black = imagecolorallocate($image, 0, 0, 0);
    $white = imagecolorallocate($image, 255,255,255);
    #$darkblue = imagecolorallocate($image, 5, 23, 54);
    $lightblue = imagecolorallocate($image, 74, 133, 148);
    $orange = imagecolorallocate($image, 255, 105, 8);

    #imagefilledrectangle($image, 0, 0, $width-1, $height-1, $white);
    #imagettftext($image, $size, 0, $extraW/2, $bbheight, $black, $font, $text);
    if ($col=='lightblue') {
        imagefilledrectangle($image, 0, 0, $width-1, $height-1, $lightblue);
    } else {
        imagefilledrectangle($image, 0, 0, $width-1, $height-1, $orange);
    }
    imagettftext($image, $size, 0, $extraW/2, $bbheight, $white, $font, $text);

    imagepng($image, "$out.png");
}

