# !/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

__author__ = 'wesc+api@google.com (Wesley Chun)'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi
from conference import MEMCACHE_FEATURED_SPEAKER_KEY
from models import Session
from google.appengine.api import memcache
from google.appengine.ext import ndb


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SetFeaturedSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """Set featured speaker in Memcache."""
        speaker = self.request.get('speaker')
        conference_key = ndb.Key(urlsafe=self.request.get('conference'))

        # if speaker has more than one session during that conference, make him featured speaker
        if Session.query(ancestor=conference_key).filter(Session.speaker == speaker).count() > 1:
            memcache.set(MEMCACHE_FEATURED_SPEAKER_KEY, speaker)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),  # from
            self.request.get('email'),  # to
            'You created a new Conference!',  # subj
            'Hi, you have created a following '  # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/set_featured_speaker', SetFeaturedSpeakerHandler),
], debug=True)
