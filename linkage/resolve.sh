#! /bin/sh

while IFS=, read -r field1
do
    curl -Ls -o /dev/null -w %{url_effective} $field1
    echo ",$field1"
done < file.csv