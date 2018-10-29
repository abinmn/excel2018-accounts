import csv
from register.models import userinfo, paid_userinfo

def generatecsv(file):

    mUser = userinfo.objects.filter(outsider=True)
    pUser = paid_userinfo.objects.filter(outsider=True)

    rows = [['Name', 'College', 'Email', 'Phone']]

    for user in mUser:
        temp = [user.name, user.college, user.email, user.phone]
        rows.append(temp)

    for user in pUser:
        temp = [user.name, user.college, user.email, user.phone]
        rows.append(temp)


    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerows(rows)
    file.close()
