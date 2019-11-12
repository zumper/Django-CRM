#!/bin/bash

NEW_MODEL=''
while [[ $1 = -* ]] ; do
  case $1 in
    --model ) NEW_MODEL=$2; shift 2;;
    -- )        shift; break;;
    * )         break;;
  esac
done

echo "making new model called: ${NEW_MODEL}"
mkdir $NEW_MODEL
touch $NEW_MODEL/__init__.py
touch $NEW_MODEL/models.py
mkdir $NEW_MODEL/migrations
touch $NEW_MODEL/migrations/__init__.py
mkdir $NEW_MODEL/templates
touch $NEW_MODEL/templates/__init__.py
git add $NEW_MODEL/*
