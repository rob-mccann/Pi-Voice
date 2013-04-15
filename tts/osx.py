import os


class OSX:

    def say(self, text):
        print "Saying: " + text
        os.system('say "%s"' % text)
