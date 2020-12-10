import urllib
import random
import requests

from hashlib import sha1
from django.utils.translation import ugettext_lazy as _


from .settings import *
from .utils import parse_xml


class BigBlueButton:
    secret_key = settings.BBB_SECRET_KEY
    api_url = settings.BBB_API_URL
    attendee_password = 'ap'
    moderator_password = 'mp'

    def api_call(self, query, call):
        """ Method to create valid API query
        to call on BigBlueButton. Because each query
        should have a encrypted checksum based on request Data.
        """
        prepared = '{}{}{}'.format(call, query, self.secret_key)
        checksum = sha1(str(prepared).encode('utf-8')).hexdigest()
        result = "%s&checksum=%s" % (query, checksum)
        return result

    def is_running(self, meeting_id):
        """ Return whether meeting_id is running or not! """
        call = 'isMeetingRunning'
        query = urllib.parse.urlencode((
            ('meetingID', meeting_id),
        ))
        hashed = self.api_call(query, call)
        url = self.api_url + call + '?' + hashed
        result = parse_xml(requests.get(url).content)
        if result:
            return result.find('running').text
        return 'error'

    def end_meeting(self, meeting_id, password):
        """ End meeting,
        Should provide Moderator password as input to make it work!
        """
        call = 'end'
        query = urllib.parse.urlencode((
            ('meetingID', meeting_id),
            ('password', password),
        ))
        hashed = self.api_call(query, call)
        url = self.api_url + call + '?' + hashed
        req = requests.get(url)
        result = parse_xml(req.content)
        if result:
            return True
        return False

    def meeting_info(self, meeting_id, password):
        """ Get information about meeting.
        result includes below data:
            start_time
            end_time
            participant_count
            moderator_count
            attendee_pw
            moderator_pw
        """
        call = 'getMeetingInfo'
        query = urllib.parse.urlencode((
            ('meetingID', meeting_id),
            ('password', password),
        ))
        hashed = self.api_call(query, call)
        url = self.api_url + call + '?' + hashed
        r = parse_xml(requests.get(url).content)
        if r:
            attendee_list = []
            try:
                for a in r.findall('attendees'):
                    try:
                        x = a.find('attendee')
                        user_id = x.find('userID').text
                        if not user_id:
                            continue
                        fullname = x.find('fullName').text
                        role = x.find('role')
                        attendee_list.append({
                            'id': user_id,
                            'fullname': fullname,
                            'role': role
                        })
                    except:
                        continue
            except Exception as e:
                pass

            # Create dict of values for easy use in template
            d = {
                'start_time': r.find('startTime').text,
                'end_time': r.find('endTime').text,
                'participant_count': r.find('participantCount').text,
                'moderator_count': r.find('moderatorCount').text,
                'moderator_pw': r.find('moderatorPW').text,
                'attendee_pw': r.find('attendeePW').text,
                'attendee_list': attendee_list,
                # 'invite_url': reverse('join', args=[meeting_id]),
            }
            return d
        return None

    def get_meetings(self):
        """ Will return list of running meetings. """
        call = 'getMeetings'
        query = urllib.parse.urlencode((
            ('random', 'random'),
        ))
        hashed = self.api_call(query, call)
        url = self.api_url + call + '?' + hashed
        result = parse_xml(requests.get(url).content)
        # Create dict of values for easy use in template
        d = []
        if result:
            r = result[1].findall('meeting')
            for m in r:
                meeting_id = m.find('meetingID').text
                password = m.find('moderatorPW').text
                d.append({
                    'meeting_id': meeting_id,
                    'running': m.find('running').text,
                    'moderator_pw': password,
                    'attendee_pw': m.find('attendeePW').text,
                    'info': self.meeting_info(
                        meeting_id,
                        password
                    )
                })
        return d

    def join_url(self, meeting_id, name, password, **kwargs):
        """ Join existing meeting_id.

        can send userID also as **kwargs so it will be set on
        meeting join, and can track useful info about users later.
        """
        call = 'join'
        data = (
            ('fullName', name),
            ('meetingID', meeting_id),
            ('password', password),
        )
        for key, value in kwargs.items():
            # Iterate on kwargs keys, and set their key=value in request.
            data = data + ((key, value), )

        query = urllib.parse.urlencode(data)
        hashed = self.api_call(query, call)
        url = self.api_url + call + '?' + hashed
        return url

    def start(self, name, meeting_id, **kwargs):
        """ Start meeting with provided info.

        Most of BigBlueButton info is provided now.
        TODO: will add more configs for bigbluebutton later!
        """
        call = 'create'
        attendee_password = kwargs.get("attendee_password", self.attendee_password)
        moderator_password = kwargs.get("moderator_password", self.moderator_password)

        # Get extra configs or set default values
        welcome = kwargs.get('welcome_text', _('Welcome!'))
        record = kwargs.get('record', BBB_RECORD)
        auto_start_recording = kwargs.get('auto_start_recording', BBB_AUTO_RECORDING)
        allow_start_stop_recording = kwargs.get('allow_start_stop_recording', BBB_ALLOW_START_STOP_RECORDING)
        logout_url = kwargs.get('logout_url', BBB_LOGOUT_URL)
        webcam_only_for_moderators = kwargs.get('webcam_only_for_moderators', BBB_WEBCAM_ONLY_FOR_MODS)
        voice_bridge = 70000 + random.randint(0, 9999)

        # Making the query string
        query = urllib.parse.urlencode((
            ('name', name),
            ('meetingID', meeting_id),
            ('attendeePW', attendee_password),
            ('moderatorPW', moderator_password),
            ('record', record),
            ('welcome', welcome),
            ('bannerText', welcome),
            ('copyright', 'شرکت پیشرو اندیشه پرداز سی‌پل'),
            ('logoutURL', logout_url),
            ('voiceBridge', voice_bridge),
            ('autoStartRecording', auto_start_recording),
            ('allowStartStopRecording', allow_start_stop_recording),
            ('webcamsOnlyForModerator', webcam_only_for_moderators),
        ))
        hashed = self.api_call(query, call)
        url = self.api_url + call + '?' + hashed
        result = parse_xml(requests.get(url).content.decode('utf-8'))
        if result:
            return result
        else:
            raise
