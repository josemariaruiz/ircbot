import datetime

import helpers
import unittest

def format_time_left(now, deskbeer_time):
    tdiff = now - deskbeer_time
    diff_sec = int(round(abs(tdiff.days * 86400 + tdiff.seconds)))
    diff_min = int(round(diff_sec / 60))

    if diff_sec <= 1:
        if diff_sec == 0:
            return "less than a minute"
        return "1 minute"
    if diff_min < 45:
        return "{} minutes".format(diff_min)
    if diff_min < 90:
        return "about 1 hour"
    return "about {} hours".format(round(diff_min / 60.0))


MESSAGES = {
    'monday': ["Calm down drunkard, it is only Monday afterall!"],
    'tuesday': ["Tuesday isn't deskbeer day, " \
               "but definitely feel less bad going to the pub after work."],
    'wednesday': ["If you're a geek it's games night, " \
               "if you're not, have fun with the hangover tomorrow. " \
               "Deskbeer not required."],
    'thursday': [
        "Run, you fool! Grey is paying for the beers downstairs!",
        "Grey's FreeBEERs will be there in just {0}, don't despair yet!"],
    'friday': ["Deskbeer needs to be aquired in {}",
               "Deskbeer should be on it's way or in your belly!"],
    'weekend': ["Why are you here on the weekend?"]
}


def decide_deskbeer_message(now):
    """Returns the right message depending on the value of now."""

    msg = None

    if now.isoweekday() == 1:
        msg = MESSAGES['monday'][0]
    elif now.isoweekday() == 2:
        msg =  MESSAGES['tuesday'][0]
    elif now.isoweekday() == 3:
        msg =  MESSAGES['wednesday'][0]
    elif now.isoweekday() == 4:
        freebeer_time = datetime.datetime(now.year, now.month, now.day, 18)
        if now >= freebeer_time:
            msg = MESSAGES['thursday'][0]
        else:
            time_left = format_time_left(now, freebeer_time)
            msg = MESSAGES['thursday'][1]

    elif now.isoweekday() == 5:
        deskbeer_time = datetime.datetime(now.year, now.month, now.day, 17)
        if now >= deskbeer_time:
            msg = MESSAGES['friday'][1]
        else:
            time_left = format_time_left(now, deskbeer_time)
            msg = MESSAGES['friday'][0].format(time_left)

    else:
        msg = MESSAGES['weekend'][0]

    return msg


def deskbeer_message():
    "every friday, 5pm"
    now = datetime.datetime.now()
    return decide_deskbeer_message(now)

@helpers.commands('deskbeer')
@helpers.throttling(5, 2)
def deskbeer(bot, conn, event):
    conn.privmsg(event.target(), deskbeer_message())



class TestDeskbeer(unittest.TestCase):

    def test_monday(self):
        monday = datetime.datetime(2011, 9, 5, 10)
        self.assertEqual(decide_deskbeer_message(monday), MESSAGES['monday'][0])

    def test_tuesday(self):
        tuesday = datetime.datetime(2011, 9, 6, 10)
        self.assertEqual(decide_deskbeer_message(tuesday), MESSAGES['tuesday'][0])

    def test_wednesday(self):
        wednesday = datetime.datetime(2011, 9, 7, 10)
        self.assertEqual(decide_deskbeer_message(wednesday), MESSAGES['wednesday'][0])

    def test_thursday(self):
        thursday = datetime.datetime(2011, 9, 8, 10)
        self.assertEqual(decide_deskbeer_message(thursday), MESSAGES['thursday'][1])

        thursday = datetime.datetime(2011, 9, 8, 18)
        self.assertEqual(decide_deskbeer_message(thursday), MESSAGES['thursday'][0])

        thursday = datetime.datetime(2011, 9, 8, 18, 1)
        self.assertEqual(decide_deskbeer_message(thursday), MESSAGES['thursday'][0])






    def test_friday(self):
        friday = datetime.datetime(2011, 9, 9, 10)
        self.assertEqual(decide_deskbeer_message(friday), MESSAGES['friday'][0].format('about 7.0 hours'))

        friday = datetime.datetime(2011, 9, 9, 16, 59)
        self.assertEqual(decide_deskbeer_message(friday), MESSAGES['friday'][0].format('1 minutes'))

        friday = datetime.datetime(2011, 9, 9, 17, 00)
        self.assertEqual(decide_deskbeer_message(friday), MESSAGES['friday'][1])

        friday = datetime.datetime(2011, 9, 9, 17, 01)
        self.assertEqual(decide_deskbeer_message(friday), MESSAGES['friday'][1])




    def test_weekend(self):
        weekend = datetime.datetime(2011, 9, 10)
        self.assertEqual(decide_deskbeer_message(weekend), MESSAGES['weekend'][0])
        weekend = datetime.datetime(2011, 9, 11)
        self.assertEqual(decide_deskbeer_message(weekend), MESSAGES['weekend'][0])



if __name__ == "__main__":
    unittest.main()
