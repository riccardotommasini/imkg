
To generate the turtle file run
```
docker run --rm -it -v $(pwd)/:/data rmlio/yarrrml-parser:latest -i /data/{mapping_file}.yaml >> {mapping_file}.ttl
```
