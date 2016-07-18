cat out.tr | grep " 2 3 cbr " | grep ^r | ./column 1 10 | awk '{printf("%d\t%f\n", $2, ($1 - timeOld) ) ; timeOld = $1; }' > jitter.txt
