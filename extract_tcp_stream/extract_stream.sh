#!/bin/bash

pcapfile=$1

for stream1 in $(tshark -r $pcapfile -T fields -e tcp.stream | sort -n | uniq)
do
    tshark -r $pcapfile -w $3/stream-$2-$stream1.pcap -Y "tcp.stream==$stream1"
done
