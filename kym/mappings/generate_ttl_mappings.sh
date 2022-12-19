#!/bin/bash

for file in ./*.yaml; do 
    echo $file;
    docker run --rm -it -v $(pwd)/:/data rmlio/yarrrml-parser:latest -i /data/$file > ${file}.ttl
 
done