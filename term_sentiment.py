
import sys
import json

#global declarations
sent_file = None  # to hold AFINN file globally
terms_score = {}  # dictionary to hold scores for non sent words like {word : score}
term_log = 'term_log.txt'

 # calculate tweet sentiment score by adding sent score of sent words found;
 # calculate non sent words score by adding tweets score where these words are found


def get_tweet_score(text):
    global terms_score  # to hold terms:values dictionary globally
    tweet_score = 0  # reset current tweet score
    # set does not produce duplicates during addition; holds non sent words for current text
    temp_words = set()

    # 1. calclate tweet sentiment
    words = text.split(' ')
    for word in words:  # Outer loop through words in the tweet
        word = word.replace('"', '').replace("'", '')
        # if (word.isalpha()) and (len(word) > 3):  # clean out not likely meanningful words
        if len(word) > 1:
            sent_file.seek(0)  # important: reset nested loop counter
            for aff_line in sent_file:   # nested loop through lines in afinn file
                aff_line = aff_line.decode(
                    "utf-8-sig").encode("utf-8").strip()  # clean
                # The file is tab-delimited.  "\t" means "tab character"
                term, score = aff_line.split("\t")
                if word == term:
                    # if current word match sentiment list adjust tweet score
                    tweet_score += int(score)
                else:
                    # add word to the temp list of non sentiment words
                    temp_words.add(word)

    # 2. Assign tweet score to each non sentiment word
    get_term_score(tweet_score, temp_words)

    return tweet_score


def get_term_score(tweet_score, temp_words):
    exists_flag = False
    for temp_word in temp_words:
        if len(terms_score) > 0:   # dictionary exists
            for k, v in terms_score.items():  # read existing key/value pair
                if k == temp_word:  # if current word found in the dictionary we adding current tweet score
                    v += tweet_score
                    exists_flag = True  # flag sohs that word was found
                else:
                    exists_flag = False
        else:
            exists_flag = False   # new empty dictionary

        if exists_flag == False:
            # add word with score to the dicionary
            #item ={temp_word, tweet_score}
            terms_score.update({temp_word: tweet_score})
        else:
            # updating current word with new score
            terms_score.update({temp_word: v})
    # end


# parse all tweets, extract text from english tweets for analysis
def parse_tweets(tweet_file):
    tweet_scores = []  # initialize an empty list

    # parse tweets
    tweet_line = tweet_file.readline()
    while tweet_line:
        # cast tweet to dictionary
        tweet_obj = json.loads(tweet_line)
        if 'text' in tweet_obj:  # read text filed from tweet
            if 'lang' in tweet_obj:  # do not read tweets without 'lang' key
                if tweet_obj['lang'] == 'en':  # read only english tweets
                    text = tweet_obj['text'].encode('utf-8')
                    # call function to process tweet text and add result to the final list
                    result = get_tweet_score(text)
                    tweet_scores.append(str(result) + '\n')

        # iterate through tweets
        tweet_line = tweet_file.readline()
        # print to tweet_log file
    # sys.stdout = open(tweet_log, 'w') # redirect all prints to this log file
    # print tweet_scores
    # or print term_scores
    sys.stdout = open(term_log, 'w')  # redirect all prints to this log file
    for index, value in enumerate(terms_score):
        print value, terms_score[value]


def main():
    global sent_file

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # do work
    parse_tweets(tweet_file)
    #print terms_score


if __name__ == '__main__':
    main()
