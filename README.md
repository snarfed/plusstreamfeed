plusstreamfeed
==============

A webapp that generates and serves an Atom feed of your Google+, ie posts from
people in your circles.

Deployed on App Engine at https://plusstreamfeed.appspot.com/

License: This project is placed in the public domain.


Development
---
You'll need the
[App Engine Python SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
version 1.9.15 or later (for
[`vendor`](https://cloud.google.com/appengine/docs/python/tools/libraries27#vendoring)
support). Add it to your `$PYTHONPATH`, e.g.
`export PYTHONPATH=$PYTHONPATH:/usr/local/google_appengine`, and then run:

```
virtualenv local
source local/bin/activate
pip install -r requirements.txt
```

Now run `/usr/local/google_appengine/dev_appserver.py .` and open
[localhost:8080](http://localhost:8080/) in your browser!

There's a good chance you'll need to make changes to
[granary](https://github.com/snarfed/granary) at the same time as plusstreamfeed. To
do that, clone the granary repo elsewhere, then install it in "source" mode
with:

```
pip uninstall oauth-dropins
pip install -e <path to oauth-dropins>
ln -s <path to oauth-dropins>/oauth_dropins \
  local/lib/python2.7/site-packages/oauth_dropins
```

The symlink is necessary because App Engine's `vendor` module doesn't follow
`.egg-link` files. :/
