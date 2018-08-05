#!/bin/sh

# set git identity
git config --global user.email "${GIT_EMAIL:-}"
git config --global user.name "${GIT_NAME:-Circle CI}"

# clone the wiki repo
git clone "git@github.com:$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME.wiki" .wiki

# run the python script
parse -o ".wiki"

# navigate to the output directory
cd .wiki

# stage changes
git add .

# commit using the last commit SHA as the message
git commit -m "$CIRCLE_SHA1"

# push the wiki repo
git push origin master
