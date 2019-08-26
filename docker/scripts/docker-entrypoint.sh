#!/bin/bash
set -e
$JMETER_HOME/bin/jmeter-server \
            -Dserver.rmi.localport=50000 \
            -Dserver_port=1099