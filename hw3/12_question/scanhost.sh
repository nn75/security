#! /bin/bash

nmap -iL host -sV -p 22| perl -ne '/^Nmap scan report for (.*) \((.*)\)/ and print "$1\t$2\n"'
