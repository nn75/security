#! /bin/bash

filename="hostlist"
while read line; do

    var1=$(nmap  -sV -p 22 $line | perl -ne '/^Nmap scan report for (.*) \((.*)\)/ and print "$1\n"')
    var2=$(nmap  -sV -p 22 $line | perl -ne '/^Nmap scan report for (.*) \((.*)\)/ and print "$2\n"')
    var3=$(sudo scanssh -s ssh $line | perl -ne '/(SSH-.*)/ and print "$1\n"')

    echo -e "$var1:$var2:$var3" >> out.csv

done < "$filename"


