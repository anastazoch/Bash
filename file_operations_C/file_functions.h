int copy_file_fgets(char *src_file, char *dst_file);
int copy_file_fread(char *src_file, char *dst_file);
int write_stdin_to_file(char *file);
int read_file_to_stdout(char *file);
void move_file(char *src_file, char *dst_file);
void remove_file(char *src_file);
void chmod_file(char *file, int mode);
void chown_file();
