#!/bin/sh
{
      sleep 60
        mongo lms --eval 'db.createUser({user:"admin", pwd:"admin", roles:[]});'
} || {
        echo "cmp already exist"
}
