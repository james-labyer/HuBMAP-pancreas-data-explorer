#!/bin/bash

# STR="ABCDE-12345" 
# var1=${STR%-*} # ABCDE
# var2=${STR#*-} # 12345

# echo $var1
# echo $var2

# STR="P1_19A AF_CD310051.png"
# var1=${STR%31*}
# var2=${STR#*31}
# echo $var1
# echo $var2
# var3=${var1}"31_C0"${var2}
# echo $var3

for f in *.png; do
  str1=${f%pling*}
  str2=${f#*pling}
  str3=${str1}"pling_C0"${str2}
  mv "$f" "$str3"
done 