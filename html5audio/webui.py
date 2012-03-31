from flask import Flask, render_template, abort, Response
from uuid import uuid1
from multiprocessing import Queue, Manager
from Queue import Empty


PROVIDER_MQ = Queue()
MANAGER = Manager()

# A list of file to be played. As the files are not in question right now,
# this simplifiaction will do.
FILES = []

app = Flask(__name__)


@app.before_first_request
def bootstrap_server(*args, **kwargs):
    """
    When the application receives the first request, we'll start up our audio
    data provider
    """
    from audio_provider import Provider
    provider = Provider(FILES)
    provider.start(PROVIDER_MQ)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def stream():

    from audio_provider import Message

    app.logger.info("Starting stream")

    queue = MANAGER.Queue(100000)
    queue.uuid = uuid1()
    def data_generator():
        """
        Creates a new generator for this HTTP request
        """
        msg = Message(Message.ADD, queue.uuid, queue)
        PROVIDER_MQ.put(msg)
        keep_running = True
        while keep_running:
            try:
                chunk = queue.get()
                yield chunk
            except Empty:
                app.logger.info('Queue empty. Ending stream')
                keep_running = False

    response = Response(
            data_generator(),
            mimetype='audio/x-mpeg')
    return response


def main():
    """
    Debug server startup.

    SYNOPSIS
        <webui> FILE1 [FILE2 [... [FILE n]]]

        FILE = mp3 file (for this sandbox I'll only accept MP3)
    """
    import sys
    FILES.extend(sys.argv[1:])
    app.debug = True
    app.run(port=5001, threaded=False)
