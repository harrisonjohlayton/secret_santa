import random
import smtplib
import traceback
from string import Template
from getpass import getpass

def send_emails(contacts, pairings, email, password):
    
    in_fd = open('message.txt','r')
    template = Template(in_fd.read())
    in_fd.close()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        print("got here")
        server.login(email, password)
        for name in pairings.keys():
            sender_name = name
            sender_email = contacts[name]
            sendee_name = pairings[name]
            server.sendmail(email, sender_email, template.substitute({'sender_email':sender_email, 'sender_name':sender_name, 'sendee_name': sendee_name}))
        print('emails sent!')
        server.close()
    except Exception:
        print('Something went wrong logging into google SMTP server...')
        traceback.print_exc()
        
    

def read_template(filename='message.txt'):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_pairings(contacts, relationships):
    pairings = dict()
    names = list(contacts.keys())
    random.shuffle(names)
    random.shuffle(names)
    random.shuffle(names)

    for i in range(len(names)):
        pairings[names[i]] = names[(i + 1)%len(names)]
    
    for name in pairings.keys():
        if (is_related(relationships, name, pairings[name])):
            return get_pairings(contacts, relationships)
    
    if (paired_together(pairings)):
        return get_pairings(contacts, relationships)
    return pairings

def paired_together(pairings):
    for name in pairings.keys():
        if (name == pairings[pairings[name]]):
            return True
    return False

def is_related(relationships, name_1, name_2):
    if ((name_1 in relationships[name_2]) or
        (name_2 in relationships[name_1])):
        return True
    return False

def get_contacts(filename='contacts.csv'):
    contacts = dict()
    NAME = 0
    EMAIL = 1

    in_fd = open(filename, 'r')
    lines = in_fd.readlines()
    lines.pop(0)
    in_fd.close()

    for line in lines:
        words = line.split(',')
        if (len(words) < 2):
            continue
        contacts[words[NAME].strip().strip('\n')] = words[EMAIL].strip().strip('\n')
    return contacts

def get_relationships(contacts, filename='relationships.csv'):
    relationships = dict()
    for name in contacts.keys():
        relationships[name] = []
    
    in_fd = open(filename, 'r')
    lines = in_fd.readlines()
    lines.pop(0)
    in_fd.close()

    for line in lines:
        words = line.split(',')
        if (len(words) < 2):
            continue
        if ((not words[0].strip().strip('\n') in relationships.keys()) or 
            (not words[1].strip().strip('\n') in relationships.keys())):
            continue
        relationships[words[0].strip().strip('\n')].append(words[1].strip().strip('\n'))
        relationships[words[1].strip().strip('\n')].append(words[0].strip().strip('\n'))
    return relationships

if __name__ == '__main__':
    contacts = get_contacts()
    relationships = get_relationships(contacts)
    pairings = get_pairings(contacts, relationships)
    email = input("Email: ")
    password = getpass()
    send_emails(contacts, pairings, email, password)