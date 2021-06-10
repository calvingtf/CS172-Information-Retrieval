import re
from urllib.request import Request
from urllib.request import urlopen

user = 'CS172_blakhdari' # Write your username here

url = 'https://www.reddit.com/user/{0}/'.format(user)
headers = {
    'Host': 'www.reddit.com',
    'User-Agent': '/r/learnpython example from {0}'.format(user),
    'Accept': '*/*',
    'Accept-Language': 'en-US',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Save-Data': 'on',
}
subreddits = ['askReddit', 'apple']

while url:
    print('Data collected: ', len(subreddits))
    conn = Request(url=url, headers=headers)
    resp = urlopen(conn)
    url = ''
    if resp.code == 200:
        code = resp.read().decode('utf-8')
        new_subreddits = re.findall('class="subreddit hover"[^>]+>([^<]+)', code)
        subreddits += new_subreddits
        url = re.findall('href="([^"]+)"[^=]+rel="nofollow next"', code)
        url = url[0] if url else ''


result = {s: subreddits.count(s) for s in set(subreddits)}
for k,v in result.items(): print('{0}: {1}'.format(k,v))