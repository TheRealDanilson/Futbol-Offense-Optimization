#!/bin/sh
./removeTrash.sh
git add .
echo "What did you change?"
read comment
git commit -m "$comment"
git push