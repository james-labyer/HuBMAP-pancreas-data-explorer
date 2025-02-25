#!/bin/bash

declare -a files=("P2-1A/P2-1A GCG 405 INS 488 tile Z 20um" 
                "P2-1A/P2-1A INS 488 tile Z 20um"
                "P2-13A/P2 13A GCG 405 TH 633 5 um stack 20x"
                "P2-19A/P2 19A GCC 405 CPep 488 CD31 456 PGP 647Parasym 488 TH 633 test tile z 9"
                "P2-19A/P2 19A GCG 405 Parasym 488 CD31 546 TH 633"
                "P2-19A/P2 19A GCG 405 TH 633 tile z 6um"
                "P2-19A/P2 19A GCG 405 TH 633 tile z 6um_Maximum intensity projection"
                "P2-19A/P2 19A Parasym 488 TH 633 tile z 25"
                )

from='/Users/jlabyer/Projects/HuBMAP-pancreas-data-explorer/HuBMAP-pancreas-data-explorer/app/assets/scientific-images/'
to='hubmap-pancreas-data-explorer-display-app-1:/app/assets/config/scientific-images/'

for i in "${files[@]}"
do
  fname=${i#*/}
  docker cp "${from}${i}/${fname}.czi" "${to}${i}"
done