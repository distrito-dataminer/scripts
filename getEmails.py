from utils import ddmdata, cleaner
import sys

base = cleaner.clean(ddmdata.readcsv(sys.argv[1]))

email_list = []

for startup in base:
    if startup['E-mail'] != '' and ('Tirar?' not in startup or startup['Tirar?'] == ''):
        emails = startup['E-mail'].replace('[', '').replace(' ', '').replace("'", '').replace(']', '')
        emails = emails.split(',')
        for email in emails:
            new_email = {}
            new_email['Startup'] = startup['Startup']
            new_email['Startup ID'] = startup['ID']
            new_email['E-mail'] = email.strip()
            email_list.append(new_email)

ddmdata.writecsv(email_list, 'base_emails_startups.csv')
