import scripts.jobs_retrieval as jobs_retrieval
import psycopg2
import datetime
import scripts.manage_log_files as manage_log_files

DB_NAME = "rolidahd"
DB_USER = "rolidahd"
DB_PASS = "zSidePZAFRFRWsLmEhM5kgqa_B_lCWJJ"
DB_HOST = "lallah.db.elephantsql.com"
DB_PORT = "5432"


# DB_NAME = "jjvqoodr"
# DB_USER = "jjvqoodr"
# DB_PASS = "6PjWRXPt25Kvp6JSEWCLpJrGvgEwC6Hx"
# DB_HOST = "otto.db.elephantsql.com"
# DB_PORT = "5432"


def fill_the_table():
    # get the job from API
    list_with_jobs = jobs_retrieval.get_the_jobs()
    # var that counts numbers of newly inserted rows to DB
    rows_inserted = 0
    # DB connection var instance
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER,
                                password=DB_PASS, host=DB_HOST,
                                port=DB_PORT)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        for job in list_with_jobs:
            # retrieve data for a single job
            job_title = job['title']
            company = job['company']
            job_description = job['description']
            # since we don't hav due_data, we store NULL to DB
            due_date = None
            location = job['location']
            url = job['url']

            # If the subquery returns at least one row, the result of EXISTS is true.
            # values are passed separately in the execute method - safe way against SQL injections
            exist_statement = "SELECT EXISTS(SELECT 1 FROM test_jobs WHERE url = %s);"
            cursor.execute(exist_statement, [url])

            # Returns result in a list; contains only one value
            # boolean - result of the EXIST command
            check_if_data_in_table = bool(cursor.fetchone()[0])

            if check_if_data_in_table:
                # if data is already in table - skip the job & move to the next one
                continue
            else:
                # if data isn't in the table => we gonna proceed with adding it & updating the # of inserted rows
                rows_inserted += 1

            # check order of columns
            # create SQL INSERT command
            # special format against SQL injections
            sql_command = """INSERT INTO test_jobs
                                    (job_title,company,job_description,due_date,location, url)
                                    VALUES (%s, %s, %s, %s, %s, %s);"""

            # Executing SQL command using the execute() method
            cursor.execute(sql_command, [job_title, company, job_description, due_date, location, url])
            # commit each new data to the table
            conn.commit()

        date = datetime.datetime.now()
        time = date.strftime("%y-%m-%d %H:%M:%S")

        log_info = "Last DB update on " + time + \
                   "\nNew jobs added: " + str(rows_inserted) + "\n\n"

        # Store info on the latest table to the log file
        # Store the time & # of updated rows
        manage_log_files.update_logs(log_info)

    except(Exception, psycopg2.DatabaseError) as error:
        # Store the error code to the log file
        log_info = "Date of update: " + str(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")) \
                   + "\nFailed to update the table" + "\nError: " + str(error) + "\n\n"
        manage_log_files.update_logs(log_info)
    finally:
        # Closing the connection
        conn.close()
        cursor.close()
