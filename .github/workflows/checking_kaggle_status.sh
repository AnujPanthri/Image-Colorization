#!/bin/bash



check_status(){
    COMMAND="kaggle k status $1"
    while true
    do
        echo "EXECUTING: $COMMAND"
        sleep 2s
        KERNEL_STATUS=$($COMMAND)
        echo "OUTPUT: $KERNEL_STATUS"
        # okay now try to exit or raise error
        if [[ $KERNEL_STATUS == *"kernel must be specified"* ]]; then 
            # error
            echo "ERROR"
            exit 1
            
        elif [[ $KERNEL_STATUS == *"has status \"complete\""* ]]; then
            # success
            echo "Notebook finished running !"
            exit 0
        
        else
            echo "Notebook still running on kaggle..."
        fi
    done

}

KERNEL_ID=$1
check_status $KERNEL_ID