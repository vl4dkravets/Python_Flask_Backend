import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_restful import Api, Resource, reqparse
import scripts.jobs_to_db as jobs_to_db
import scripts.retrieve_from_db

app = Flask(__name__)
api = Api(app)

args = reqparse.RequestParser()
args.add_argument('job_title', type=str, help='Job name is required')
args.add_argument('location', type=str, help='Location is required')


@api.resource('/api/v1')
class Jobs_API(Resource):

    def get(self):
        keywords = args.parse_args()
        job = keywords['job_title']
        location = keywords['location']

        results = scripts.retrieve_from_db.return_jobs(job, location)
        return results


@app.route('/')
def home():
    return '<h1>Hello, Team Panda!</h1>'


def job_function():
    # function that runs automatically & fills the table
    jobs_to_db.fill_the_table()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(job_function, 'interval', days=1)

# Explicitly kick off the background thread
scheduler.start()

# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__ == '__main__':
    app.run()
