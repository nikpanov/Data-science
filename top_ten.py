
import sys
import json
import operator
 
 #global declarations

hashtags_count = {} # dictionary to hold scores for non sent words like {word : score}
frequency_log ='frequency_log.txt'

    
# parse all tweets, extract text from english tweets for analysis
def parse_tweets(tweet_file):

    hashtags_count={}
    # parse tweets
    tweet_line = tweet_file.readline()
    while tweet_line:        
        # cast tweet to dictionary
        tweet_obj = json.loads(tweet_line)
        # if 'text' in tweet_obj: # read text filed from tweet 
            # if 'lang' in tweet_obj: # do not read tweets without 'lang' key
            #     if tweet_obj['lang'] == 'en': # read only english tweets 
        if 'text' in tweet_obj:          
            hashtags = []
            # read tweet's hashtags into list
            hashtags = [hashtag['text'] for hashtag in tweet_obj['entities']['hashtags']]

                
            for tag in hashtags:
                utag = tag.encode("utf-8")
                if len(hashtags_count) == 0 :
                    # starting new list
                    hashtags_count[utag] = 1
                else:
                    for k, v in hashtags_count.items(): # read existing key/value pair
                        if k == utag: #
                            hashtags_count[utag] = v + 1
                        else: #introducing new item in dictionary
                            tagcount =({utag : 1})
                            hashtags_count.update(tagcount) 
        else:
            pass


                           
                   
        # iterate through tweets
        tweet_line = tweet_file.readline()

    # # print hashtag counts
    top_ten_log='top_ten_log.txt'
    sys.stdout = open(top_ten_log, 'w') 


    sorted_tags = sorted(hashtags_count.items(), key= operator.itemgetter(1), reverse=True)     
   
    for  x in sorted_tags[:9]:
        print x[0], x[1]
    
       
    line =  sorted_tags[10][0] + ' ' + str(sorted_tags[10][1])
    sys.stdout.write(line)

    sys.stdout.close()
   
   
def main():      
    tweet_file = open(sys.argv[1])    
 
    # do work
    parse_tweets(tweet_file)
    #print hashtags_score
 
   
 
if __name__ == '__main__':
    main()
