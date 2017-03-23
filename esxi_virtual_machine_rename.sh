#!/bin/bash

ORIGINAL_NAMES=(<space-seperated_name_list>)
NEW_NAMES=(<space-seperated_name_list>)
DATASTORE=<datastore_name>

for $i in "${!ORIGINAL_NAMES[@]}"
do
	VMID=`vim-cmd vmsvc/getallvms | grep ${ORIGINAL_NAMES[$i]}`
	vim-cmd vmsvc/power.shutdown $VMID
	vim-cmd vmsvc/unregister $VMID
	
	cd /vmfs/volumes/$DATASTORE/${ORIGINAL_NAMES[$i]}
	
	# vmkfstools -i "${ORIGINAL_NAMES[$i]}.vmdk" "${NEW_NAMES[$i]}.vmdk"
	vmkfstools -E "${ORIGINAL_NAMES[$i]}.vmdk" "${NEW_NAMES[$i]}.vmdk"
	
	sed -i 's/${ORIGINAL_NAMES[$i]}/${NEW_NAMES[$i]}/g' ${ORIGINAL_NAMES[$i]}.vmx
	
	for file in *.vmx *.nvram 
	do	
		extension=${file##*.}
		mv $file ${NEW_NAMES[$i]}.$extension
	done
	
	cd ..

	mv ${ORIGINAL_NAMES[$i]} ${NEW_NAMES[$i]}

	vim-cmd solo/registervm ${NEW_NAMES[$i]}/${NEW_NAMES[$i]}.vmx
	vim-cmd vmsvc/power.on $VMID
	:'
	The following commands have to be executed for each virtual machine in order to answer that you have either copied or moved the virtual machine, otherwise the virtual machine will hang up indefinitely and not complete the boot process:
	'
	MESSAGE_ID=`vim-cmd vmsvc/message $VMID | grep "Virtual machine message" | awk -F ' ' '{print $4}'` # Gather the message ID from the "Virtual machine message <message_ID>:" line of the output.
	vim-cmd vmsvc/message $VMID $MESSAGE_ID <option_number>	# Option number can be 0 = Cancel, 1 = "I moved it", or 2 = "I copied it">
done
