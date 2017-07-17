#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "file_functions.h"
 
int main(int argc, char **argv) {
    
    const char *commands[] = {"cp", "mv", "rm", "chmod", "chown"};
    char command[5];
	size_t num_of_commands = 0;
	bool command_found = false;
    char mode[4];
    int mode_int;
	char file[50], src_file[50], dst_file[50];
	int i;
	
	while ( commands[num_of_commands] != NULL ) num_of_commands++;
	
	while ( !command_found ) {
		printf("Which command do you want to execute? [cp, mv, rm, chmod, chown]: ");
		scanf("%s", command);
		for (i = 0; i < num_of_commands; i++) {
			if ( strcmp(command, *(commands + i)) == 0 ) {
				command_found = true;
				break;
			}
		}
		if ( !command_found ) printf("Wrong command inserted.\n");
	}
	
	/* Match used-inserted command to the command options */
	if ( strcmp(command, "cp") == 0 ) {
		printf("Which file do you want to copy: ");
		scanf("%s", src_file);
		printf("Which file do you want to copy the above file to: ");
		scanf("%s", dst_file);
		copy_file_fread(src_file, dst_file);
	}
	else if ( strcmp(command, "mv") == 0 ) {
		printf("Which file to move: ");
		scanf("%s", src_file);
		printf("New file name: ");
		scanf("%s", dst_file);
		move_file(src_file, dst_file);
	}
	else if ( strcmp(command, "rm") == 0 ) {
		printf("Which file to remove: ");
		scanf("%s", file);
		remove_file(file);
	}
	else if ( strcmp(command, "chmod") == 0 ) {
		printf("Which file do you want to chmod? : ");
		scanf("%s", file);
		printf("Which mode do you want to change the file to? : ");
		scanf("%s", mode);
		mode_int = strtol(mode, 0, 8);
		chmod_file(file, mode_int);
	}
	else if ( strcmp(command, "chown") == 0 ) {
		chown_file();
	}
	
	return 0;
}
