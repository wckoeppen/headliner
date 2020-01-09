#!/bin/sh

GIT='/usr/bin/git'
REPO_DIR='/home/will/Projects/headliner'

cd ${REPO_DIR}

# headlines
${GIT} add ${REPO_DIR}/headline-store-json/*
${GIT} commit -m "add yesterday's headlines"

# logs
${GIT} add ${REPO_DIR}/headliner.log
${GIT} commit -m "daily log"

# push
${GIT} push origin master