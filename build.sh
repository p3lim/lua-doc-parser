#!/bin/sh

if [[ -z "$CI" ]]; then
	echo "No CI"
	exit 1
fi

if [[ -n "$CIRCLECI" ]]; then
	COMMIT_SHA="$CIRCLE_SHA1"
	REPO_PATH="$CIRCLE_PROJECT_USERNAME/$CIRCLE_PROJECT_REPONAME"
fi
if [[ -n "$GITHUB_ACTION" ]]; then
	COMMIT_SHA="$GITHUB_SHA"
	REPO_PATH="$GITHUB_REPOSITORY"
fi

# set git identity
git config --global user.email "<>"
git config --global user.name "${GIT_NAME:-CI}

# clone the wiki repo
git clone "git@github.com:$REPO_PATH.wiki" .wiki

# run the python script
parse -o ".wiki" || exit 1

# navigate to the output directory
cd .wiki

# stage changes
git add .

# commit using the last commit SHA as the message
git commit -m "$COMMIT_SHA"

# push the wiki repo
git push origin master
