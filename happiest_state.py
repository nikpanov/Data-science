import json
import operator
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#global declarations
sent_file = None  # to hold AFINN file globally
tweet_infos = {}  # dictionary to hold location's happiness data

happy_log = 'happy_log.txt'
states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


 # calculate tweet sentiment score by adding sent score of sent words found;
def get_tweet_score(text):
    
    tweet_score = 0  # reset current tweet score
    # set does not produce duplicates during addition; holds non sent words for current text
    temp_words = set()

    # 1. calclate tweet sentiment
    words = text.split(' ')
    for word in words:  # Outer loop through words in the tweet
        if (word.isalpha()) and (len(word) > 3):  # clean out not likely meanningful words
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

    return tweet_score


def get_tweet_state(info):
    # looking for State name or abbreviation in the text
    for key, value in states.iteritems():
        if info.count(key) > 0:
            state = key or '' # value or ''
            break
        elif info.count(value) > 0:
            state = key or '' # value or ''
            break
        else:
            state = ''
    return state


# parse all tweets, extract text from english tweets for analysis
def parse_tweets(tweet_file):
    global tweet_infos

    # print to test_log file
    # sys.stdout = open('test_log.txt', 'w')  # redirect all prints to this log file

    # parse tweets
    tweet_line = tweet_file.readline()
    while tweet_line:
        state = ''
        # cast tweet to dictionary
        tweet_obj = json.loads(tweet_line)
        if 'text' in tweet_obj:  # read text filed from tweet
            if 'lang' in tweet_obj:
                if tweet_obj['lang'] == 'en':  # read only english tweets
                    text = tweet_obj['text'].encode('utf-8')
                    # user: location
                    location = tweet_obj['user']['location']
                    if not location:
                        location = ''
                    else:
                        location.encode('utf-8')
                        # print location

                    if 'coordinates' in tweet_obj:
                        coordinates = tweet_obj['coordinates'] or ''
                    else:
                        coordinates = ''
                    if 'place' in tweet_obj:
                        place = tweet_obj['place'] or ''
                    else:
                        place = ''

                    info = text + ' ' + str(location) + ' ' + str(coordinates) + ' ' + str(place) 
                    state = get_tweet_state(info)

                    if len(state) > 0:
                        tweet_score = get_tweet_score(text)

                        if (state in tweet_infos) == False:  # if state is not introduced yet we  ad it
                            tweet_infos[state] = tweet_score
                        else:
                            # increment
                            new_count = (tweet_infos[state]) + tweet_score
                            tweet_infos.update({state: new_count})

        # iterate through tweets
        tweet_line = tweet_file.readline()

    # sys.stdout.close()
        


        # print to happy_log file
    sys.stdout = open(happy_log, 'w')  # redirect all prints to this log file
    sorted_infos = sorted(tweet_infos.items(), key=operator.itemgetter(1), reverse=True)

    if not sorted_infos:
         sys.stdout.write('NA')
    else:
        sys.stdout.write(sorted_infos[0][0]) # zero based 

    sys.stdout.close
  
   

def main():
    global sent_file

    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
   
    # do work
    parse_tweets(tweet_file)
  


if __name__ == '__main__':
    main()
