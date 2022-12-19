#! /bin/sh

while IFS=, read -r field1
do
    curl -Ls -o /dev/null -w %{url_effective} https://knowyourmeme.com/memes/$field1
    echo ",$field1,https://knowyourmeme.com/memes/$field1"
done < imgflip_templates.csv