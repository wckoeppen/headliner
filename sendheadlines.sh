#!/bin/sh

GIT='/usr/bin/git'
REPO_DIR='/Users/wckoeppen/work/projects/headliner'

cd ${REPO_DIR}

# headlines
${GIT} add ${REPO_DIR}/datastore/processed/*
${GIT} commit -m "add yesterday's headlines"

# logs
${GIT} add ${REPO_DIR}/headliner.log
${GIT} commit -m "daily log"

# push
${GIT} push origin master