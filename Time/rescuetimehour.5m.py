#!/usr/bin/env python2
# <bitbar.title>RescueTime Crono</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Queli Coto</bitbar.author>
# <bitbar.author.github>nothnk</bitbar.author.github>
# <bitbar.desc>Show your RescueTime Very productivity of the day in the status bar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# To install, you will want to generate an API key for rescue time and then store the
# key in ~/Library/RescueTime.com/api.key
# https://www.rescuetime.com/anapi/manage

import json
import os
import urllib
import urllib2

API_KEY = os.path.expanduser('~/Library/RescueTime.com/api.key')

MAPPING = {
    2: 'Very Productive',
    1: 'Productive',
    0: 'Neutral',
    -1: 'Distracting',
    -2: 'Very Distracting'
}

TIME_MIN = 198000
TIME_GOLD = 234000


def get(url, params):
    '''Simple function to mimic the signature of requests.get'''
    params = urllib.urlencode(params)
    result = urllib2.urlopen(url + '?' + params).read()
    return json.loads(result)


def statusTime(timeSeconds):
    color = 'RED'
    if timeSeconds > TIME_MIN:
        color = 'ORANGE'
    if timeSeconds > TIME_GOLD:
        color = '#27c940'
    return color


def smileStatusTime(timeSeconds):
    color = ':japanese_goblin:'
    if timeSeconds > TIME_MIN:
        color = ':sunglasses:'
    if timeSeconds > TIME_GOLD:
        color = ':fire:'
    return color


def getTime(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d" % (h, m)


if not os.path.exists(API_KEY):
    print('X')
    print('---')
    print('Missing API Key')
    exit()

with open(API_KEY) as fp:
    key = fp.read().strip()
    result = get('https://www.rescuetime.com/anapi/data', params={
        'format': 'json',
        'key': key,
        'restrict_kind': 'activity'
    })

    total_time_vp = 0
    total_time_p = 0
    total_time_n = 0
    total_time_d = 0
    total_time_vd = 0

for rank, seconds, people, activity, category, productivty in result['rows']:
    if productivty == 2:
        total_time_vp = total_time_vp + seconds
    if productivty == 1:
        total_time_p = total_time_p + seconds
    if productivty == 2:
        total_time_n = total_time_n + seconds
    if productivty == -1:
        total_time_d = total_time_d + seconds
    if productivty == -2:
        total_time_vd = total_time_vd + seconds


#time vp
total_time_vp_time = getTime(total_time_vp)
#time p
total_time_p_time = getTime(total_time_p)
#neutral time
total_time_n_time = getTime(total_time_n)
#time d
total_time_d_time = getTime(total_time_d)
#time md
total_time_vd_time = getTime(total_time_vd)

print(' %s%s | color=%s ' % (smileStatusTime(total_time_vp), total_time_vp_time, statusTime(total_time_vp)))
print('---')
print('Rescue Time | href=https://www.rescuetime.com/dashboard?src=bitbar')
print('Very Productive Time %s' % (total_time_vp_time))
print('Productive Time %s' % (total_time_p_time))
print('Neutral Time %s' % (total_time_n_time))
print('Distracting Time %s' % (total_time_d_time))
print('Very Distracting Time %s' % (total_time_vd_time))
