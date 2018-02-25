
import sys
import json
 
 #global declarations
sent_file = None # to hold AFINN file globally
tweet_log ='tweet_log.txt'
 
 # calculate tweet sentiment score by adding sent score of sent words found; 
def get_tweet_score(text):     
    tweet_score = 0 # reset current tweet score
    temp_words = set() # set does not produce duplicates during addition; holds non sent words for current text

    # 1. calclate tweet sentiment
    words = text.split(' ')
    for word in words: # Outer loop through words in the tweet
        word = word.replace('"', '').replace("'", '')
        #if  (word.isalpha()) and (len(word) > 3): # clean out not likely meanningful words
        sent_file.seek(0) # important: reset nested loop counter
        for aff_line in sent_file:   # nested loop through lines in afinn file
            aff_line = aff_line.decode("utf-8-sig").encode("utf-8").strip() # clean 
            term, score = aff_line.split("\t")  # The file is tab-delimited.  "\t" means "tab character"
            if word == term:
                # if current word match sentiment list adjust tweet score
                tweet_score += int(score)
            else:
                # add word to the temp list of non sentiment words
                temp_words.add(word)       
   
    return tweet_score
    
# parse all tweets, extract text from english tweets for analysis
def parse_tweets(tweet_file):
    tweet_scores = [] # initialize an empty list  to hold tweets scores in order of processing tweets   
    sys.stdout = open(tweet_log, 'w') # redirect all prints to this log file    
    # parse tweets
    tweet_line = tweet_file.readline()
    while tweet_line:        
        # cast tweet to dictionary
        tweet_obj = json.loads(tweet_line)
        # we assume that there are only tweets and only english tweets(assignment condition)
        if 'text' in tweet_obj: # read text filed from tweet
        #     if 'lang' in tweet_obj: # do not read tweets without 'lang' key
        #         if tweet_obj['lang'] == 'en': # read only english tweets
            text = tweet_obj['text'].encode('utf-8')  
            # call function to process tweet text and add result to the final list   
            result = get_tweet_score(text)         
            tweet_scores.append(result)   
            print  float(result)                     
            # print '\n'.join(map(float, tweet_scores))
        # iterate through tweets
        tweet_line = tweet_file.readline()

    #     # print to tweet_log file    
    # sys.stdout = open(tweet_log, 'w') # redirect all prints to this log file    
    # print '\n'.join(map(str, tweet_scores))
    sys.stdout.close()
    # or print term_scores
   
   
def main():
    global sent_file
 
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])    
    
    # do work
    parse_tweets(tweet_file)
    #print terms_score
 
   
 
if __name__ == '__main__':
    main()
