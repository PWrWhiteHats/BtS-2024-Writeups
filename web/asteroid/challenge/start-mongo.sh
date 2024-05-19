#!/bin/bash
echo "Starting MongoDB..."
mongod --fork --logpath /var/log/mongod.log --storageEngine wiredTiger
