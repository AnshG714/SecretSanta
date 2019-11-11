import smtplib, ssl
from string import Template
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class PersonInfo:

    def __init__(self, names, emails):
        self.names = names
        self.emails = emails

def get_participants(filename):
    names = []
    emails = []
    with open(filename, mode = 'r', encoding = 'utf-8-sig') as contacts_file:
        for contact in contacts_file:
            split = contact.split()
            #print(split)
            names.append(split[0])
            emails.append(split[1])

    return PersonInfo(names, emails)

def read_template(filename):
    with open(filename, mode = 'r', encoding = "ISO-8859-1") as template_file:
        template_file_content = template_file.read()

    return Template(template_file_content)

def createSSPairings(names):
    secondCopy = names[:]
    random.shuffle(secondCopy)
    for i in range(len(names)):
        if names[i] == secondCopy[i]:
            secondCopy[i], secondCopy[i-1] = secondCopy[i-1], secondCopy[i]

    return secondCopy

def main():
    password = input("Type your password and press enter: ")

    context = ssl.create_default_context()

    info = get_participants('peeps.txt')
    names = info.names
    emails = info.emails
    message_template = read_template('message.txt')
    pairings = createSSPairings(names)
    smtp_server = "smtp.gmail.com"
    port = 465
    for name, email, pairing in zip(names, emails, pairings):

        message = message_template.substitute(person_name = name.title(), santee = pairing)

        with smtplib.SMTP_SSL(smtp_server, port, context = context) as server:
            server.login("sheldoncourtsecretsanta@gmail.com", password)
            print('done')
            server.sendmail(
                "sheldoncourtsecretsanta@gmail.com", email, message.encode("utf8")
            )

if __name__ == '__main__':
    main()
