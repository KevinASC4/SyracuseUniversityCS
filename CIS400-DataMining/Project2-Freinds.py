import twitter
import json
from functools import partial
from sys import maxsize as maxint
import sys
import time
from urllib.error import URLError
from http.client import BadStatusLine
import networkx as nx
# getTwitter object
def oauth_login():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://developer.twitter.com/en/docs/basics/authentication/overview/oauth
    # for more information on Twitter's OAuth implementation.
    #Authorization
    CONSUMER_KEY = "5hxPiteIhuzXBDk35BsDzdT8U"
    CONSUMER_SECRET = "Vqt1kSm01UdgJ4hxPfH12OW78Fs2uyOjXrMA6dIXHbFyqIT9md"
    OAUTH_TOKEN = "1182358903436263427-jszOyBJxRhnZFPxksL7rkECekD2NLF"
    OAUTH_TOKEN_SECRET = "UMjXUxIknhtGKv9hGQN7sHNNvh41qlawvBJO5SsDHpmbC"
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
# Sample usage
twitter_api = oauth_login()
#DO REQUESTS
def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw): 
    
    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
    
        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e
    
        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes
    
        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429: 
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'                  .format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function
    
    wait_period = 2 
    error_count = 0 

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0 
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

def get_friends_followers_ids(twitter_api, screen_name=None, user_id=None,
                              friends_limit=5000, followers_limit=5000):
    
    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None),     "Must have screen_name or user_id, but not both"
    
    # See http://bit.ly/2GcjKJP and http://bit.ly/2rFz90N for details
    # on API parameters
    
    get_friends_ids = partial(make_twitter_request, twitter_api.friends.ids, 
                              count=5000)
    get_followers_ids = partial(make_twitter_request, twitter_api.followers.ids, 
                                count=5000)

    friends_ids, followers_ids = [], []
    
    for twitter_api_func, limit, ids, label in [
                    [get_friends_ids, friends_limit, friends_ids, "friends"], 
                    [get_followers_ids, followers_limit, followers_ids, "followers"]
                ]:
        
        if limit == 0: continue
        
        cursor = -1
        while cursor != 0:
        
            # Use make_twitter_request via the partially bound callable...
            if screen_name: 
                response = twitter_api_func(screen_name=screen_name, cursor=cursor)
            else: # user_id
                response = twitter_api_func(user_id=user_id, cursor=cursor)

            if response is not None:
                ids += response['ids']
                cursor = response['next_cursor']
        
            print('Fetched {0} total {1} ids for {2}'.format(len(ids),                  label, (user_id or screen_name)),file=sys.stderr)
        
            # XXX: You may want to store data during each iteration to provide an 
            # an additional layer of protection from exceptional circumstances
        
            if len(ids) >= limit or response is None:
                break

    # Do something useful with the IDs, like store them to disk...
    return friends_ids[:friends_limit], followers_ids[:followers_limit]
#GET Recirpocal friends from myFriends
def reciprocalFreinds(friendObject):
    friendsID= friendObject[0]
    followerID= friendObject[1]
    finalList = []
    for i in friendsID:
        for j in followerID:
            if i == j:
                finalList.append(i)
    return finalList
#FindPopularFriends
def get_user_profile(twitter_api, screen_names=None, user_ids=None):
   
    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None),     "Must have screen_names or user_ids, but not both"
    
    items_to_info = {}

    items = screen_names or user_ids
    
    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See http://bit.ly/2Gcjfzr for details.
        
        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup, 
                                            screen_name=items_str)
        else: # user_ids
            response = make_twitter_request(twitter_api.users.lookup, 
                                            user_id=items_str)
        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else: # user_ids
                items_to_info[user_info['id']] = user_info

    return response
# Get top Follower count from list
def getFollowerCountFromList(listOfFriends):
    maxFriendofFive = []
    if len(listOfFriends)==0:
        return maxFriendofFive
    if len(listOfFriends)<=5:
        for i in listOfFriends:
            maxFriendofFive.append(i)
        return maxFriendofFive
    for i in range(0,5,1):
        maxStart = listOfFriends[0]
        for j in listOfFriends:
            if get_user_profile(twitter_api,str(j))[0]["followers_count"] > get_user_profile(twitter_api, str(maxStart))[0]["followers_count"]:
                maxStart = j
        maxFriendofFive.append(maxStart)
        listOfFriends.remove(maxStart)
    return maxFriendofFive
def crawl_followers(twitter_api, screen_name, limit=1000000, depth=10, **mongo_conn_kw):
    
    # Resolve the ID for screen_name and start working with IDs for consistency 
    # in storage
    G = nx.Graph()
    seed_id = str(twitter_api.users.show(screen_name=screen_name)['id'])
    
    _, next_queue = get_friends_followers_ids(twitter_api, user_id=seed_id, 
                                              friends_limit=5000, followers_limit=5000)
    G.add_node(seed_id)
    print(G)
    # Store a seed_id => _follower_ids mapping in MongoDB
    
    #save_to_mongo({'followers' : [ _id for _id in next_queue ]}, 'followers_crawl', 
                 # '{0}-follower_ids'.format(seed_id), **mongo_conn_kw)
    while G.number_of_nodes()<=100:
        (queue, next_queue) = (next_queue, [])
        for fid in queue:
            myFriendsIDs = get_friends_followers_ids(twitter_api, str(fid), 
                                                     friends_limit=5000, 
                                                     followers_limit=5000)
            recipFriendsQ = reciprocalFreinds(myFriendsIDs)
            newAdditions = getFollowerCountFromList(recipFriendsQ)
            print(newAdditions)
            if len(recipFriendsQ) == 0:
                pass
            for i in newAdditions:
                G.add_node(str(i))
                G.add_edge(str(fid),str(i))
                print(G)
                next_queue += str(i)
            # Store a fid => follower_ids mapping in MongoDB
            #save_to_mongo({'followers' : [ _id for _id in follower_ids ]}, 
              #            'followers_crawl', '{0}-follower_ids'.format(fid))
    return G
def getDiameter(graphInput):
    return(nx.diameter(graphInput))
def getAvergeDistance(graphInput):
    centralNode = [node for node, in_degree  in graphInput.in_degree if in_degree==0]
    totalDistance = 0
    for node in graphInput:
        shortestDistance = nx.shortest_path_length(graphInput, source = centralNode, target = node )
        totalDistance += shortestDistance
    return(totalDistance/(graphInput.number_of_nodes()-1))
def main():
    input1 = input("What is the twitter Name?")
    graphMade = crawl_followers(twitter_api, str(input1))
    print("The diameter of My Network is:" + getDiameter(graphMade))
    print("The average distance of My Network is"+ getAvergeDistance(graphMade))
main()