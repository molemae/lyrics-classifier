# Lyrics Classifier

Built a text classification model using Logistic Regression on song lyrics with an automated process of scraping for artist and their song lyrics using Python packages of Selenium and Beautiful Soup. The user is asked to input atleast one artist name. As the code runs, the user is also asked if they would like to download the URLs and the all or a number of songs for that artist. Once the songs are downloaded logistic regression is applied on the lyrics to find its accuracy on test and train data. 

Before logistic regression, CountVectorizer is applied to tokenise the lyrics and TfidfTransformer to add weights to the frequency of the tokens

![lyrics_classifier](https://user-images.githubusercontent.com/79316344/222850633-34647959-275d-4684-a082-7203939c1a0e.gif)

### Requirements
- Python 3.8 and above
- Selenium

### Usage
- Run the main.py file along with atleast one Artist in a string format. 

### Collaborators
- Moritz
- Simantini
