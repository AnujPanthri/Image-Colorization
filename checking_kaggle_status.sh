#!/bin/bash


check_status(){
    KERNEL_STATUS=$(kaggle k status)
    RESULT=$?
    while true
    do
        sleep 2s
        echo $KERNEL_STATUS
    done

}

check_status