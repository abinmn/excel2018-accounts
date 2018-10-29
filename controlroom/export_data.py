import csv
from register.models import userinfo, paid_userinfo
from controlroom.models import event


def generatepaidcsv(file):

    pUser = paid_userinfo.objects.filter(outsider=True)

    rows = [['Name', 'College', 'Email', 'Phone', 'Event', 'Price', 'Short Listed']]

    for user in pUser:
        event_obj = event.objects.get(event_id=user.event)
        eName = event_obj.event_name
        shortlisted = False
        if user.excelid in event_obj.short_list:
            shortlisted=False
        temp = [user.name, user.college, user.email, user.phone, eName, user.price, shortlisted]
        rows.append(temp)


    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerows(rows)
    file.close()

def generateusercsv(file):

    mUser = userinfo.objects.filter(outsider=True)

    rows = [['Name', 'College', 'Email', 'Phone', 'Event',]]

    for user in mUser:
        eName = user.participated_events
        temp = [user.name, user.college, user.email, user.phone, eName,]
        rows.append(temp)


    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerows(rows)
    file.close()
