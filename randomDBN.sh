#!/bin/bash

function experiment()
{
    python randomDBN.py > "dbn$1.log"
}

pushd .

experiment 01
experiment 02
experiment 03
experiment 04

popd
