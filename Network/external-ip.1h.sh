#!/bin/bash

# external-ip
# BitBar plugin
#
# by Mat Ryer
#
# Gets the current external IP address.

EXTERNAL_IP=$(dig +short myip.opendns.com @resolver1.opendns.com)

if [ "$1" = "copy" ]; then
  # Copy the IP to clipboard
  echo $EXTERNAL_IP | pbcopy
fi

echo $EXTERNAL_IP
echo "---"
echo "(External IP address)"
echo "Copy IP | terminal=false bash=$0 param1=copy"
