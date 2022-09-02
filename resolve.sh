o#! /bin/sh

while IFS=, read -r field1 field2
do
    curl -Ls -o /dev/null -w %{url_effective} https://knowyourmeme.com/memes/$field2
    echo ",$field1,https://knowyourmeme.com/memes/$field2"
done < query.csv