#! /bin/bash

for d in */ ; do
    cd $d
    echo "java -jar ./mapper.jar -m ./mapping.tt -o ../${d%?}.nt"
    java -jar mapper.jar -m mapping.ttl -o ../${d%?}.nt
    cd ..
done

cat *.nt >> imgflip_subset.nt