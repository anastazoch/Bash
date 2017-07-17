#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h> 
#include <pwd.h>
#include <grp.h>
#include <errno.h>
#include "file_functions.h"
 
#define BUF_SIZE 200

int copy_file_fgets(char *src_file, char *dst_file) {
	
	FILE *input_fd, *output_fd;		/* Declare input and output file descriptors */

    /* Create input file descriptor */
    input_fd = fopen(src_file, "r");
    if (input_fd == NULL) {
        perror("open");
        return 2;
    }
 
    /* Create output file descriptor */
    output_fd = fopen(dst_file, "w");
    if (output_fd == NULL) {
		perror("open");
		return 3;
    }

	/* Create buffer and dynamically allocate memory to the buffer */
 	char* buffer = malloc(sizeof(char) * BUF_SIZE);

    /* Copy process: while each line of the input_fd file is read to the buffer, 
    keep writing the line from the buffer to the output_fd file. */
	while ( fgets(buffer, BUF_SIZE, input_fd) ) {
	   fputs(buffer, output_fd);
	}
    
    /* Free buffer from heap */
    free(buffer);
    
    return (EXIT_SUCCESS); 
}

int copy_file_fread(char *src_file, char *dst_file) {
	
	FILE *input_fd, *output_fd;
	size_t bytes;
	
    /* Create input file descriptor */
    input_fd = fopen(src_file, "r");
    if (input_fd == NULL) {
        perror("open");
        return 2;
    }
 
    /* Create output file descriptor */
    output_fd = fopen(dst_file, "w");
    if (output_fd == NULL) {
		perror("open");
		return 3;
    }
	
	/* Go to end of the input file and count the number of bytes from the start of the file (= file size) */
	if (fseek(input_fd, 0L, SEEK_END) == 0) {
        int bufsize = ftell(input_fd) + 1;
        if (bufsize == -1) { 
        	printf("Error finding input file size.\n");
        	return 1;
        }

        /* Allocate our buffer to that size. */
        char *buffer = malloc(sizeof(char) * bufsize);

        /* Go back to the start of the file. */
        if (fseek(input_fd, 0L, SEEK_SET) != 0) { 
        	fputs("Error going back to the start of the file.\n", stdout);
        	return 1;
        }

        /* Read the input file into memory line by line and write each line to the output file. */
        while ( (bytes = fread(buffer, sizeof(char), bufsize, input_fd)) > 0 ) {
        	fwrite(buffer, sizeof(char), bytes, output_fd);
        }
        
        fclose(input_fd);
		fclose(output_fd);
		free(buffer);
    }
    
    return (EXIT_SUCCESS);
}

int write_stdin_to_file(char *file) {
	
	FILE *output_fd;
	char *buffer;
	
	output_fd = fopen(file, "w");
	if (output_fd == NULL) {
		perror("open");
		return 2;
	}
 	
 	buffer = (char *)malloc( sizeof(char)*BUF_SIZE );

	while ( fgets(buffer, BUF_SIZE, stdin) ) {
	   fputs(buffer, output_fd);
	}
 
	fclose(output_fd);	
	free(buffer);
 
	return (EXIT_SUCCESS);
}

int read_file_to_stdout(char *file) {
 
    FILE *input_fd;
    char *buffer; 

    input_fd = fopen(file, "r");
    if (input_fd == NULL) {
		perror("open");
		return 3;
    }
 	
 	buffer = (char *)malloc( sizeof(char)*BUF_SIZE );

	while ( fgets(buffer, BUF_SIZE, input_fd) ) {
	   fputs(buffer, stdout);
	}

    fclose(input_fd);   
    free(buffer);
 
    return (EXIT_SUCCESS);
}

void move_file(char *src_file, char *dst_file) {

	if ( rename(src_file, dst_file) == 0 ) {
		printf("File renamed successfully\n");
   	}
   	else {
   	   	printf("Error: unable to rename the file\n");
   	}
}

void remove_file(char *file) {
	
	if ( access( file, F_OK ) != -1 ) {
		if ( remove(file) == 0 ) {
			printf("File deleted successfully");
		}
		else {
			printf("Error: unable to delete the file");
		}
	}
	else {
		perror("Error");
		exit(1);
	}
}

void chmod_file(char *file, int mode) {

	if ( chmod(file, mode) != 0 ) {
		perror("Error:");
		exit(1);
	}		
}

void chown_file() {
	
	char file[50];
    char owner[50], group[50];
	struct passwd *pwd;
	struct group *grp;
	
	printf("Which file do you want to chown? : ");
	scanf("%s", file);	
	
	printf("File owner: ");
	scanf("%s", owner);
	if ( ( pwd = getpwnam(owner) ) == NULL ) {
		fprintf(stdout, "User not exists.\n");
  		exit(EXIT_FAILURE);
	}
	
	printf("File group: ");
	scanf("%s", group);
	if ( ( grp = getgrnam(group) ) == NULL ) {
		fprintf(stdout, "Group not exists.\n");
      	exit(EXIT_FAILURE);
	}
	
	if ( chown(file, pwd->pw_uid, grp->gr_gid) != 0 ) {
		perror("Error");
	}
}
