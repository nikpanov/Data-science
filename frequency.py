
import sys
import json
 
 #global declarations

terms_count = {} # dictionary to hold scores for non sent words like {word : score}
frequency_log ='frequency_log.txt'
texts_count = 0 # incremental number of texts 
words_count = 0 # variable to hold incremental number of words in all texts
 

 
def calculate_word_count(text):
    global words_count

    words = text.split(' ') # create list of words
    
    for word in words: # Outer loop through words in the tweet
        if  (word.isalpha()): #and (len(word) > 3): # clean out not likely meaningful words
            words_count += 1 # count only cleaned words
            occurences = float(text.count(word))            
            if len(terms_count) == 0:
                # if no dictionary created yet add first element to the dictionary
                terms_count[word] = 1.0
            elif terms_count.get(word,0) == 0:
                # if word not in the dictionary yet add new word to the dictionary
                terms_count[word] = 1.0
            else:
                # if the word is in dictionary increment count for word   
                new_count = float(terms_count[word]) + occurences 
                terms_count.update({word : new_count})



    
# parse all tweets, extract text for analysis
def parse_tweets(tweet_file):
    global texts_count     

    # parse tweets
    tweet_line = tweet_file.readline()
    while tweet_line:        
        # cast tweet to dictionary
        tweet_obj = json.loads(tweet_line)
        if 'text' in tweet_obj: # read text filed from tweet
            # we read all languages
            # if 'lang' in tweet_obj: # do not read tweets without 'lang' key
            # if tweet_obj['lang'] == 'en': # read only english tweets
            text = tweet_obj['text'].encode('utf-8') 
            texts_count += 1 
                # call function to process tweet text and add result to the final list 
            calculate_word_count(text)                                     
                   
        # iterate through tweets
        tweet_line = tweet_file.readline()

    # # DEBUG -----------------
    # # print out term counts
    # termcount_log='termcount_log.txt'
    # sys.stdout = open(termcount_log, 'w') 
    # for index, value in enumerate(terms_count):
    #     print  value , terms_count[value]
    # sys.stdout.close()  
    # # -----------------------

    # normalize words count into frequency
    for key, value in terms_count.iteritems():
	terms_count[key] = float(value/words_count)
   
    sys.stdout = open(frequency_log, 'w') # redirect all prints to this log file
    for index, value in enumerate(terms_count):
        #print  value , terms_count[value]
        print (value + ' ' +   "%1.6f" % (terms_count[value])) # formatted
    sys.stdout.close() 
   
def main():      
    tweet_file = open(sys.argv[1])    

    # do work
    parse_tweets(tweet_file)
    #print terms_score
 
   
 
if __name__ == '__main__':
    main()
