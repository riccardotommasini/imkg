#!/bin/bash
#java -jar mapper.jar -m ./mappings/kym.parent.media.frames.yaml.ttl -o ./rdf/kym.media.frame.parent.nt
# for mfile in ./mappings/kym.*.ttl; do 
#     echo $mfile;
#     java -jar mapper.jar -m ./mappings/${mfile} -o $mfile.nt
   
# done

# java -jar mapper.jar -m ./mappings/kym.media.frames.yaml.ttl -o ./rdf/full/kym.media.frames.nt
# java -jar mapper.jar -m ./mappings/kym.parent.media.frames.yaml.ttl -o ./rdf/full/kym.parent.media.frames.nt
# java -jar mapper.jar -m ./mappings/kym.children.media.frames.yaml.ttl -o ./rdf/full/kym.children.media.frames.nt
# java -jar mapper.jar -m ./mappings/kym.siblings.media.frames.yaml.ttl -o ./rdf/full/kym.siblings.frames.nt
# java -jar mapper.jar -m ./mappings/kym.types.media.frames.yaml.ttl -o ./rdf/full/kym.types.media.frames.nt
java -jar mapper.jar -m ./mappings/kym.media.visual.enrichment.frames.yaml.ttl -o ./rdf/full/kym.visual.enrichment.media.frames.nt
java -jar mapper.jar -m ./mappings/kym.media.frames.textual.enrichment.yaml.ttl -o ./rdf/full/kym.textual.enrichment.media.frames.nt

# java -jar mapper.jar -m ./mappings/kym.seed.media.frames.yaml.ttl -o ./rdf/seed/kym.media.frames.nt
# java -jar mapper.jar -m ./mappings/kym.seed.parent.media.frames.yaml.ttl -o ./rdf/seed/kym.parent.media.frames.nt
# java -jar mapper.jar -m ./mappings/kym.seed.children.media.frames.yaml.ttl -o ./rdf/seed/kym.children.media.frames.nt
# java -jar mapper.jar -m ./mappings/kym.seed.siblings.media.frames.yaml.ttl -o ./rdf/seed/kym.siblings.frames.nt
# java -jar mapper.jar -m ./mappings/kym.seed.types.media.frames.yaml.ttl -o ./rdf/seed/kym.types.media.frames.nt
# java -jar mapper.jar -m ./mappings/seeds.to.kym.media.frames.yaml.ttl -o ./rdf/seed/seeds.to.kym.media.frames.nt
java -jar mapper.jar -m ./mappings/kym.seed.media.visual.enrichment.frames.yaml.ttl -o ./rdf/full/kym.visual.enrichment.media.frames.nt
java -jar mapper.jar -m ./mappings/kym.seed.media.frames.textual.enrichment.yaml.ttl -o ./rdf/full/kym.textual.enrichment.media.frames.nt
