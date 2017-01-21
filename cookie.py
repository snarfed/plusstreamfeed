"""Fetch plus.google.com with a cookie and convert it to Atom.
"""

import datetime
import logging
import re
import urllib2

import appengine_config
from granary import atom, googleplus
from oauth_dropins.webutil import handlers
import webapp2

CACHE_EXPIRATION = datetime.timedelta(minutes=5)


class CookieHandler(handlers.ModernHandler):
  handle_exception = handlers.handle_exception

  @handlers.memcache_response(CACHE_EXPIRATION)
  def get(self):
    try:
      cookie = 'SID=%(SID)s; SSID=%(SSID)s; HSID=%(HSID)s' % self.request.params
    except KeyError:
      return self.abort(400, 'Query parameters SID, SSID, and HSID are required')

    logging.info('Fetching with Cookie: %s', cookie)
    resp = urllib2.urlopen(urllib2.Request(
      'https://plus.google.com/',
      headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Cookie': cookie,
      }),
      timeout=60)
    body = resp.read().decode('utf-8')
    logging.info('Response: %s', resp.getcode())

    if resp.getcode() != 200 or 'href="https://accounts.google.com/Logout' not in body:
      return self.abort(401, "Couldn't log into Google+ with cookie %s" % cookie)

    actor = {}
    name_email = re.compile(r'title="Google Account: ([^"]+)"').search(body)
    if name_email:
      logging.info('Logged in for user %s', name_email.group(1))
      actor = {'displayName': name_email.group(1)}
    else:
      logging.warning("Couldn't determine Google user!")

    activities = [
      a for a in googleplus.GooglePlus(None, None).html_to_activities(body)
      if a.get('verb') != 'like'
    ]

    self.response.headers['Content-Type'] = 'application/atom+xml'
    self.response.out.write(atom.activities_to_atom(
      activities, actor, title='plusstreamfeed (Google+ Atom feed)',
      host_url=self.request.host_url + '/', request_url=self.request.path_url,
      xml_base='https://plus.google.com/'))


application = webapp2.WSGIApplication(
  [('/cookie', CookieHandler),
   ], debug=False)

