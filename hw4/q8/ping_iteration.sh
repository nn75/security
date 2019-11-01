#! /bin/bash

for i in {41..99};
do  ping -c 1 kali-vcm-$i.vm.duke.edu &> /dev/null && echo kali-vcm-$i.vm.duke.edu ok || echo kali-vcm-$i.vm.duke.edu down;
done


