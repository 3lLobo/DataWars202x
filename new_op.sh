#/bin/bash

# Push new .zip file to github

file_name=$1

# split at _ and take first part if _ exists and lowercase
dir_name=$(echo $file_name | cut -d'_' -f 1 | tr '[:upper:]' '[:lower:]')

echo $dir_name

mkdir -p ./opdrachten/$dir_name

unzip $file_name -d ./opdrachten/$dir_name  
git add ./opdrachten/$dir_name
git commit -m "Added $dir_name"
git push

gh pr create --title "Added $dir_name" --body "Added $dir_name" --base main 

echo "Done"