#!/bin/bash



check_status(){
    COMMAND="kaggle k status $1"
    echo "EXECUTING: $COMMAND"
    while true
    do
        sleep 30s
        KERNEL_STATUS=$($COMMAND)
        echo "OUTPUT: $KERNEL_STATUS"
        # okay now try to exit or raise error
        if [[ $KERNEL_STATUS == *"kernel must be specified"* ]]; then 
            # error
            echo "ERROR"
            exit 1

        elif [[ $KERNEL_STATUS == *"has status \"running\""* ]]; then
            echo "Notebook still running on kaggle..."

        elif [[ $KERNEL_STATUS == *"has status \"complete\""* ]]; then
            # success
            echo "Notebook finished running !"
            exit 0

        else
            # error
            echo "ERROR"
            exit 1
        fi
    done

}

KERNEL_ID=$1
check_status $KERNEL_ID