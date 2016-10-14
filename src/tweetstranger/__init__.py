import re


class TweetStranger(object):
    def __init__(self, board, twitter, tag="#StrangerHacks"):
        self.tag = tag
        self.queue = []
        self.searches = 0
        self.twitter = twitter
        self.board = board
        board.begin()

    def cycle(self, count=10, splain=False):
        if not self.searches:
            results = self.twitter.search(query=self.tag, count=count)
        else:
            results = self.twitter.repeat_search()

        if type(results) is list:
            self.searches += 1
            for tweet in results:
                text = re.sub('#\w+', '', tweet['text'])
                text = re.sub('[^A-Za-z ]', '', text)
                self.queue.append(text)
                if splain:
                    print("added '{}' to queue".format(text))

        if len(self.queue):
            msg = self.queue.pop()
            if splain:
                print("Writing '{}' to device queue".format(msg))
            self.board.write(msg)

        if type(results) is list:
            return len(results)
        return 0
