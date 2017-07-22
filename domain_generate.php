<?php
for($i=0; $i<128; $i++){
	if(($i>=48 && $i<=57) || ($i>=65 && $i<=90) || ($i>=97 && $i<=122)){
		$str = chr($i);
		echo "\"".$str."\",";
	}
}

echo "<br>";
echo "<br>";
echo "<br>";

$arr=array("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z");
//echo $arr[34];
//foreach ($arr as $k1 => $v1) {
	for($i=0; $i<=35; $i++){
		//foreach ($arr as $k2 => $v2) {
			for($k=0; $k<=35; $k++){
				echo "0f".$arr[$i].$arr[$k]."<br>";
			}
		//}
	}
//}

?>