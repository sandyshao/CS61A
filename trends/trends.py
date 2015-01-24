"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


###################################
# Phase 1: The Feelings in Tweets #
###################################

# tweet data abstraction (A), represented as a list
# -------------------------------------------------

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python list.

    Arguments:
    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2014, 9, 29, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    122
    >>> tweet_string(t)
    '"just ate lunch" @ (122, 37)'
    """
    return [text, time, lat, lon]

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    "*** YOUR CODE HERE ***"
    return tweet[0]
def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    "*** YOUR CODE HERE ***"
    return tweet[1]
def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet[2],tweet[3])

# tweet data abstraction (B), represented as a function
# -----------------------------------------------------

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2014, 9, 29, 13, 0)
    >>> latitude(tweet_location_fn(t))
    122
    """
    # Please don't call make_tweet in your solution
    "*** YOUR CODE HERE ***"
    def get(index):
        if index=='text':
            return text
        elif index=='time':
            return time
        elif index=='lat':
            return lat
        elif index=='lon':
            return lon
    return get

def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    return tweet('text')

def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    return tweet('time')

def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    return make_position(tweet('lat'), tweet('lon'))

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_string(tweet):
    """Return a string representing a tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)

def tweet_words(tweet):
    """Return the words in a tweet."""
    return extract_words(tweet_text(tweet))

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    "*** YOUR CODE HERE ***"
    def helper(text,a):
        list1=[]
        for i in text:
            if i in ascii_letters:
                a=a+i
            else:
                if a!='':                   
                    list1=list1+[a]
                a=''
        if a!='':
            list1=list1+[a]
        return list1
    return helper(text,'')




          # You may change/remove this line

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert (value is None) or (-1 <= value <= 1), 'Bad sentiment value'
    "*** YOUR CODE HERE ***"
    return value

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    if s==None:
        return False
    else:
        return True
def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    "*** YOUR CODE HERE ***"
    return s
def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))

def analyze_tweet_sentiment(tweet):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet('berkeley golden bears!', None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    "*** YOUR CODE HERE ***"
    total_sentiment,count=0,0
    a=tweet_words(tweet)
    for i in a:
        if has_sentiment(get_word_sentiment(i))==True:
            total_sentiment=total_sentiment+sentiment_value(get_word_sentiment(i))
            count=count+1
    if count==0:
        return make_sentiment(None)
    return make_sentiment(total_sentiment/count)

#################################
# Phase 2: The Geometry of Maps #
#################################

def apply_to_all(map_fn, s):
    return [map_fn(x,y,x1,y1) for x,y,x1,y1 in s]

def apply_to_all_2(map_fn,s):
    return [map_fn(x,y,z) for x,y,z in s]

def keep_if(filter_fn, s):
    return [x for x in s if filter_fn(x)]

def reduce(reduce_fn, s, initial):
        reduced = initial
        for x in s:
            reduced = reduce_fn(reduced, x)
        return reduced

def find_centroid(polygon):
    """Find the centroid of a polygon. If a polygon has 0 area, use the latitude
    and longitude of its first position as its centroid.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    Arguments:
    polygon -- A list of positions, in which the first and last are the same

    Returns 3 numbers: centroid latitude, centroid longitude, and polygon area.

    >>> p1 = make_position(1, 2)
    >>> p2 = make_position(3, 4)
    >>> p3 = make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1] # First vertex is also the last vertex
    >>> round_all = lambda s: [round(x, 5) for x in s]
    >>> round_all(find_centroid(triangle))
    [3.0, 2.0, 6.0]
    >>> round_all(find_centroid([p1, p3, p2, p1])) # reversed
    [3.0, 2.0, 6.0]
    >>> apply_to_all(float, find_centroid([p1, p2, p1])) # A zero-area polygon
    [1.0, 2.0, 0.0]
    """
    "*** YOUR CODE HERE ***"
    area_value,cx_value,cy_value=0,0,0
    length=len(polygon)
    for i in range(length-1):
        area_value=area_value+(latitude(polygon[i])*longitude(polygon[i+1])-latitude(polygon[i+1])*longitude(polygon[i]))/2
    if area_value==0:
        return [latitude(polygon[0]),longitude(polygon[0]),area_value]
    for i in range(length-1):
        cx_value=cx_value+(latitude(polygon[i])+latitude(polygon[i+1]))*(latitude(polygon[i])*longitude(polygon[i+1])-latitude(polygon[i+1])*longitude(polygon[i]))/(area_value*6)
    for i in range(length-1):
        cy_value=cy_value+(longitude(polygon[i])+longitude(polygon[i+1]))*(latitude(polygon[i])*longitude(polygon[i+1])-latitude(polygon[i+1])*longitude(polygon[i]))/(area_value*6)
    area_value=abs(area_value)
    return[cx_value,cy_value,area_value]


def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in
    polygons, weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    "*** YOUR CODE HERE ***"
    if len(polygons)==1:
        centroid=find_centroid(polygons[0])
        return make_position(centroid[0],centroid[1])
    elif len(polygons)>1:
        cx=lambda x, y, area: x*area
        cy=lambda x, y, area: y*area
        sum_area=lambda x, y, area:area
        list_of_centroid=[]
        i=range(len(polygons))
        for numbers in i:
            centroid=find_centroid(polygons[numbers])
            list_of_centroid.append(centroid)
        cx_value=(sum(apply_to_all_2(cx, list_of_centroid)))/(sum(apply_to_all_2(sum_area, list_of_centroid)))
        cy_value=(sum(apply_to_all_2(cy, list_of_centroid)))/(sum(apply_to_all_2(sum_area, list_of_centroid)))
        return make_position(cx_value,cy_value)
###################################
# Phase 3: The Mood of the Nation #
###################################


def group_by_key(pairs):
    """Return a dictionary that relates each unique key in [key, value] pairs
    to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_key(example)
    {1: [2, 3, 2], 2: [4], 3: [2, 1]}
    """
    # Optional: This implementation is slow because it traverses the list of
    #           pairs one time for each key. Can you improve it?
    keys = [key for key, _ in pairs]
    return {key: [y for x, y in pairs if x == key] for key in keys}

def state_center_list():
    list_center=[]
    for state in us_states:
        center=find_state_center(us_states[state])
        list_center.append(center)
    return list_center

def get_back_to_states(center):
    for state in us_states:
        center1=find_state_center(us_states[state])
        if center1==center:
            return state

def group_tweets_by_state(tweets):
    """Return a dictionary that groups tweets by their nearest state center.

    The keys of the returned dictionary are state names and the values are
    lists of tweets that appear closer to that state center than any other.

    Arguments:
    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> len(two_tweets_by_state)
    2
    >>> california_tweets = two_tweets_by_state['CA']
    >>> len(california_tweets)
    1
    >>> tweet_string(califojrnia_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    "*** YOUR CODE HERE ***"
    list_center=state_center_list()
    distance_list=[]
    state_tweet=[]
    for i in tweets:
        position=tweet_location(i)
        for center in list_center:
            distance=geo_distance(position,center)
            distance_list.append(distance)
        closest=min(distance_list)
        for i in tweets:
            position=tweet_location(i)
            for center in list_center:
                distance=geo_distance(position,center)
                if distance==closest:
                    combo=[get_back_to_states(center)]+[i]
                    state_tweet.append(combo)
                    distance_list=[]
    return group_by_key(state_tweet)

def dictionary(pairs):
    """Return a dictionary that relates each unique key in [key, value] pairs
    to a list of all values that appear paired with that key.

    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_key(example)
    {1: [2, 3, 2], 2: [4], 3: [2, 1]}
    """
    main_dictionary={}
    for element in pairs:
        dictionary={element[0]:element[1]}
        main_dictionary.update(dictionary)
    return main_dictionary 


def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely. Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0. 0 represents neutral sentiment, not unknown
    sentiment.

    Arguments:
    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    "*** YOUR CODE HERE ***"
    new_list=[]
    count=0
    sentiment=0
    for states in tweets_by_state:
        tweets=tweets_by_state[states]
        for each_message in tweets:
            a=analyze_tweet_sentiment(each_message)
            if has_sentiment(a):
                sentiment=sentiment+sentiment_value(a)
                count=count+1    
        if count!=0:
            total_sentiment=sentiment/count
            combo=[states]+[total_sentiment]
            new_list.append(combo)
        sentiment,count=0,0   
    return dictionary(new_list)
    



##########################
# Command Line Interface #
##########################

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    centers = {name: find_state_center(us_states[name]) for name in us_states}
    center = centers[center_state.upper()]
    distance = lambda name: geo_distance(center, centers[name])
    for name in sorted(centers, key=distance)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    Arguments:
    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        draw_state(shapes, state_sentiments.get(name))
    for name, shapes in us_states.items():
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_query(term='my job', file_name='tweets2014.txt'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term, file_name)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', type=str)
    parser.add_argument('--tweets_file', '-t', type=str, default='tweets2014.txt')
    parser.add_argument('--use_functional_tweets', '-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    if args.draw_map_for_query:
        print("Using", args.tweets_file)
        draw_map_for_query(args.draw_map_for_query, args.tweets_file)
        return
    for name, execute in args.__dict__.items():
        if name != 'text' and name != 'tweets_file' and execute:
            globals()[name](' '.join(args.text))
