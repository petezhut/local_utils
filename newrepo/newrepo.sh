#!/bin/bash

name=$1

mkdir ${name}
cd ${name}
git init 
touch README
git add .
git commit -m "beginning...."
git checkout -b develop
echo "DEV" >> README
git add .
git commit -m "Adding dev branch"

echo "Done..."
