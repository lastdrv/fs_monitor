#!/bin/bash

/usr/bin/find / -size +50M -exec ls -s --block-size=M {} \; > /root/fs_monitor/data/$(date \+\%Y-%m-%d-%H).log
