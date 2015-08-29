"""Fetch plus.facebook.com with a cookie and convert it to Atom.
"""

import logging
import re
import urllib2

import appengine_config
from granary import atom, googleplus
import webapp2


class CookieHandler(webapp2.RequestHandler):

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
    assert resp.getcode() == 200

    # TODO: check we logged in ok
    # if not soup.find('a', href=re.compile('^/logout.php')):
    #   return self.abort(401, "Couldn't log into Facebook with cookie %s" % cookie)

    # home_link = soup.find('a', href=re.compile(
    #   r'/[^?]+\?ref_component=mbasic_home_bookmark.*'))
    # if home_link:
    #   href = home_link['href']
    #   logging.info('Logged in for user %s', href[1:href.find('?')])
    # else:
    #   logging.warning("Couldn't determine username or id!")

    activities = googleplus.GooglePlus(None, None).html_to_activities(body)

    self.response.headers['Content-Type'] = 'application/atom+xml'
    self.response.out.write(atom.activities_to_atom(
        activities, {}, title='title', host_url=self.request.host_url + '/',
        request_url=self.request.path_url))


application = webapp2.WSGIApplication(
  [('/cookie', CookieHandler),
   ], debug=False)
