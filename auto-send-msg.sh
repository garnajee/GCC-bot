#!/usr/bin/env bash

# channel blablabla
WEBHOOK_URL="https://discord.com/api/webhooks/1234567890123456789/randomecaractersherexxxxxxxx"

function send_msg () {
    while true
    do
        MESSAGE="Updating CTFs..."
        curl -H "Content-Type: application/json" -X POST -d '{ "content":"'"${MESSAGE}"'" }' ${WEBHOOK_URL}
        sleep $((168*60*60)) # once a week
    done
}

send_msg # call function
