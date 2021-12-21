# secret_santa
TL;DR - Generate emails for secret santa based on relationship constraints.

To make this work you should create a fresh gmail account that will be used to generate the secret santa emails. You must then:
- edit the message to a message of your choosing
- edit the contacts.csv file to contain the names and emails of everyone in your secret santa
- edit the relationships.csv file to contain pairs of names of couples who should not get eachother for secret santa. (i.e. my brother and his girlfriend should not get eachother as this would spoil the fun).

After setting up your gmail account to allow third party applications, you can simply run the program. Each person will be assigned a person for whom they have to buy a present and emails will be sent automatically. This code guarantees that:
- Everyone will get one person to buy a present for
- Nobody will miss out
- People in relationships will not get eachother
- If A has to buy a present for B, then B doesn't have to buy a present for A (the graph representing gift giving is a fully connected digraph)

Happy Holidays!
