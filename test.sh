#!/bin/sh
read -p "Please input PeopleID:" id
read -p "Please input startframe:" startframe
read -p "Please input endframe:" endframe
python3 pythonscript/Others/test.py $((endframe - startframe+1))
