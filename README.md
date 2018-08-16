# SuperManager

### Predicting Basketball Player Performance Using Neural Networks

Under development...

This project is an attempt to predict future performance of basketball players in the Spanish Basketball league (acb.com) based on the statistics from the past 5 seasons.


### My Solution
Current solution: Feedforward Neural networks
Future solution: RNNs (LSTMs)
Future goal: Create a simple web interface to allow anyone to use the tool and make predictions with it.



### File Description

main.py: main file to run.

populateDB.py: reads stats from URLs, parses HTML code using Beautiful Soup, and stores stats in the sqlite DB.

createDicts.py: creates Python dictionaries to convert player/team names into numbers, to feed to the NN.

readDB.py: reads some rows from DB and returns them.

parseData.py: parses DB data to convert it into numbers to be fed to the NN.

nn.py: Neural Network architecture and training details.

