import getpass
import createDicts
import nn
import csv

# Read password to connect to DB
#pw = getpass.getpass()

# Create dictionaries for player and team names
names, teams = createDicts.createDicts()

w = csv.writer(open("players.csv", "w"))
for key, val in names.items():
    w.writerow([key, val])

#Start tensorflow model
nn.train_model(names, teams)



