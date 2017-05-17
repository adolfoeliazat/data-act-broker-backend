import calendar

from dataactcore.interfaces.db import GlobalDB
from dataactvalidator.health_check import create_app

from dataactcore.models.jobModels import Submission
from dataactcore.models.userModel import User

from datetime import datetime

if __name__ == '__main__':
    with create_app().app_context():
        count = 0
        sess = GlobalDB.db().session
        query = sess.query(Submission).filter(Submission.d2_submission==False)
        for submission in query:
            # Check submission.reporting_end_date, it should not be the first
            date = submission.reporting_end_date
            if date.day == 1 and submission is not None:
                print('Starting Submission {}'.format(submission.submission_id))
                new_day = calendar.monthrange(date.year, date.month)[1]
                date = datetime(date.year, date.month, new_day).date()
                submission.reporting_end_date = date
                sess.add(submission)
                sess.commit()
                print('Finished Submission {}'.format(submission.submission_id))
                count = count + 1
        print('{} Submissions Updated'.format(count))