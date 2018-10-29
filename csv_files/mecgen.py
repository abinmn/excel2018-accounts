
import csv
from register.models import userinfo

def generateId(classcode, year, file):
    college="Model Engineering College"
    id = classcode+year
    csv_file = open(file, 'r')
    csv_reader = csv.reader(csv_file, delimiter=",")
    count = 0
    for row in csv_reader:
        if count!=0 and len(row[0])>0:
            name = row[0]
            email = row[1]
            phone_number = row[2]
            if count<10:
                excel_id = 'EX' + year + classcode + '0' + str(count)
            else:
                excel_id = 'EX' + year + classcode + str(count)
            object = userinfo(excelid=excel_id, name=name, college=college, email=email, phone=phone_number, outsider=False, present=True)
            object.save()
        count += 1
