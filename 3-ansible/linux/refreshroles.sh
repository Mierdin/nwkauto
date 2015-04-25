#!/bin/bash
set -euo pipefail # Unofficial bash strict mode
IFS=$'\n\t'

# This script will clone each GitHub repo containing a desired
# Ansible role, and extract the role contained within. Used to
# assemble a list of Ansible roles, specifically for demo purposes

# Create array containing repository names
declare -a REPOS=(
    ansible-role-dnsmasq
    ansible-role-quagga
    ansible-role-iscdhcp
    ansible-role-router
)

# Create roles dir if needed, and delete all existing roles
echo "Resetting 'roles' dir..."
mkdir roles/ && rm -rf roles/*

# Create function to download repo
function dlrepo {
    if [ -d "$1" ]; then
        rm -rf $1
    fi

    git clone -q git@github.com:Mierdin/$1 tmpworkspace/$1

    # Copy all subdirectories
    cp -r tmpworkspace/$1/roles/* roles/
}

# Need to create a temp working dir if needed here
echo "Creating temporary workspace..."
if [ -d "tmpworkspace" ]; then
    rm -rf tmpworkspace
fi
mkdir tmpworkspace

# Loop through the array, cloning into working directory
echo "Cloning repositories..."
for i in "${REPOS[@]}"
do
    dlrepo $i
done

# Clean up temporary workspace
echo "Cleaning up..."
rm -rf tmpworkspace
