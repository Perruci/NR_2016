cat out.tr | grep ^d | awk '{old_data=old_data + 1;  print $2, old_data;}' > drops.txt

