
import sys
import json

'''
changes: 02/25/2018 prepare to read only english tweets; deleted hello world

'''

#global declarations
tweet_log = 'tweet_log.txt'

# calculate tweet sentiment score by adding sent score of sent words found;


def get_tweet_score(text, sent_file):
    tweet_score = 0  # reset current tweet score

    # 1. calclate tweet sentiment
    words = text.split(' ')
    for word in words:  # Outer loop through words in the tweet
        # word =word.encode("utf-8").strip()
        # if  (word.isalpha()) and (len(word) > 3): # clean out not likely meanningful words
        sent_file.seek(0)  # important: reset nested loop counter
        for sent_line in sent_file:   # nested loop through lines in afinn file
            sent_line = sent_line.decode(
                "utf-8-sig").encode("utf-8").strip()  # clean
            # The file is tab-delimited.  "\t" means "tab character"
            term, score = sent_line.split("\t")
            if word == term:
                # if current word match sentiment list adjust tweet score
                tweet_score += int(score)
            else:
                pass

    # 2. Assign tweet score to each non sentiment word
    #get_term_score(tweet_score, temp_words)

    return tweet_score


# parse all tweets, extract text from english tweets for analysis
def parse_tweets(tweet_file, sent_file):

    sys.stdout = open(tweet_log, 'wb')  # redirect all prints to this log file
    # parse tweets
    tweet_line = tweet_file.readline()
    while tweet_line:       
        # cast tweet to dictionary
        tweet_obj = json.loads(tweet_line)
        if 'text' in tweet_obj:  # read text filed from tweet
            text = tweet_obj['text'].encode('utf-8')
            # call function to process tweet text and add result to the final list
            result = get_tweet_score(text, sent_file)
            str_result = str(result) +'\n'
            # print to tweet_log file
        #    sys.stdout.write(str_result)
            print result
        tweet_line = tweet_file.readline()

    # or print term_scores
    # sys.stdout = open(term_log, 'w') # redirect all prints to this log file
    # print term_scores


def main():
    global sent_file

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

      
    # do work
    parse_tweets(tweet_file, sent_file)
    #print terms_score


if __name__ == '__main__':
    main()
