import os
import csv

from celery.loaders import app

from .models import User

dirpath = os.getcwd()
foldername = os.path.basename(dirpath)
path = os.path.normpath(dirpath + os.sep + os.pardir)
print (path)
users_csv_file = (os.path.join(path,"users.csv"))
print(users_csv_file)


# @app.tasks(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    with open(users_csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')
                user = User.objects.create(username=row[0], email=row[3], first_name=row[1], last_name=row[2],
                                           linked_in_url=row[4], twitter_url=row[5], blog_url=row[6])
                user.save()
