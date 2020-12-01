import random
import smtplib
from string import Template

def send_emails(contacts, pairings, email, password):
    # for name in pairings.keys():
    #     print(f'{name} with email {contacts[name]} sends to {pairings[name]} with email {contacts[pairings[name]]}')
    template = read_template()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',465)
        server.ehlo()
        server.login(email, password)
    except:
        print 'Something went wrong logging into google SMTP server...'
    
    


def read_template(filename='message.txt'):
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_pairings(contacts, relationships):
    pairings = dict()
    names = list(contacts.keys())
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
    email = input("email: ")
    password = input("password: ")
    send_emails(contacts, pairings, email, password)