import os


def update_logs(update_info):
    dir_name = "Logs"
    file_name = "last_update.txt"

    create_directory(dir_name)
    update_log_file(file_name, dir_name, update_info)


# Check if the directory exists
def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


# Start working with the log file & writing to it
def update_log_file(file_name, dir_name, data):
    path = dir_name + '/' + file_name
    if not os.path.isfile(path):
        write_file(path, data)
    else:
        append_to_file(path, data)


# Create file if it doesn't exist yet
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# Append to the log file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data)


