import getopt
import tornado.ioloop
import tornado.web
import sys
from sentiwordnet import Sentiwordnet

import time


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, sentiwordnet):
        self.sentiwordnet = sentiwordnet

    def get(self):
        start = time.time()
        # Check input text
        word = self.get_argument("word")
        pos = self.get_argument("pos")
        language = self.get_argument("language")

        score = sentiwordnet.get_sentiment(word, pos, language)

        # Create DS to save result
        response = {}
        response["score"] = score

        response["elipsed_time"] = time.time() - start
        # Return result
        self.write(response)

# Check if server por is valid
try:
    opts, args = getopt.getopt(sys.argv[1:], "p:", ["port="])
    assert (len(opts) == 1)
except:
    print 'sentiwordnet_service.py -p <port>'
    sys.exit()

for o, a in opts:
    if o == "-p":
        port = a
    else:
        pass

if __name__ == "__main__":
    # Init treetagger with a specific language
    sentiwordnet = Sentiwordnet()

    # Init Tornado web server
    application = tornado.web.Application([
        (r"/", MainHandler, dict(sentiwordnet=sentiwordnet)),
    ])

    # Listen on specific port and start server
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
