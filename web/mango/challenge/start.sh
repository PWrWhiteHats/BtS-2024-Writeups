#!/bin/bash

# Start MongoDB
mongod --fork --logpath /var/log/mongod.log

# Set the environment variable for MongoDB URI
export MONGODB_URI=mongodb://127.0.0.1:27017/ctfDB

node index.js
