import psycopg2

DB_NAME = "rolidahd"
DB_USER = "rolidahd"
DB_PASS = "zSidePZAFRFRWsLmEhM5kgqa_B_lCWJJ"
DB_HOST = "lallah.db.elephantsql.com"
DB_PORT = "5432"


def return_jobs(job, location):
    conn = None
    cursor = None
    res = []

    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER,
                                password=DB_PASS, host=DB_HOST,
                                port=DB_PORT)

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        sql_command = ''

        # if field are empty => checking for it in the first place & returning the res
        # otherwise, more work & checking is needed
        if (not job) and (not location):
            cursor.execute("SELECT * FROM test_jobs")
            conn.commit()
            return cursor.fetchall()

        # remove whitespace before & after the word
        job = job.strip()
        location = location.strip()

        # "~*" symbol means => Matches regular expression, case insensitive
        if job != '' and location != '':
            sql_command = "SELECT * FROM test_jobs WHERE job_title ~* %s AND location ~* %s"
            # Executing SQL command using the execute() method
            cursor.execute(sql_command, [job, location])
        elif job != '' and (not location):
            sql_command = "SELECT * FROM test_jobs WHERE job_title ~* %s"
            cursor.execute(sql_command, [job])
        elif location != '' and (not job):
            sql_command = "SELECT * FROM test_jobs WHERE location ~* %s"
            cursor.execute(sql_command, [location])

        conn.commit()
        res = cursor.fetchall()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        cursor.close()
        conn.close()

    return res
