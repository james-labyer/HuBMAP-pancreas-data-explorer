#!/bin/bash

declare -a files=("P1-14A/P1_14A1_ KRT19 green INS white stack" 
                "P1-14A/P1_14A1_KRT green INS white stack higher res"
                "P1-14A/P1_14A1_KRT green INS white stack_Stitch"
                "P1-14A/P1_14A2_CD31 red INS white stack high res 2x"
                "P1-14A/P1_14A2_CD31 red INS white stack high res"
                "P1-19A/P1_19A1 KRT green INS white stack 2x"
                "P1-19A/P1_19A1 KRT green INS white stack"
                "P1-19A/P1_19A2 CD31 red INS white stack"
                "P1-7A/P1_7A2_KRT CD31 INS tile stack_Stitch"
                "P1-7A/P1_7A2_KRT CD31 INS higher res_Stitch"
                "P1-7A/P1_7A2_KRT CD31 INS tile stack higher res 2_Stitch"
                "P1-7A/P1_7A2_CD31 INS tile and stack_Stitch"
                )

from=''
to=''
key=''

for i in "${files[@]}"
do
  fname=${i#*/}
  scp -i $key "${from}${i}/${fname}.czi" "${to}${i}"
done
