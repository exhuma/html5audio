from multiprocessing import Process, log_to_stderr
from Queue import Empty, Full
from itertools import cycle
import logging

LOG = logging.getLogger(__name__)

class Message(object):
    """
    Instances of this type can be sent to the provider's message queue.
    """

    ADD = 'add'
    REMOVE = 'remove'

    def __init__(self, op, uuid, payload):
        self.op = op
        self.payload = payload
        self.uuid = uuid

class Provider(object):
    """
    A class providing audio data in chunks to consumers.
    Each consumer has it's own queue. Chunks will be passed on through that
    queue.

    Additionally, the provider has a queue itself allowing us to attach/detach
    consumers.
    """

    def __init__(self, files):
        """
        Constructor

        :param files: A list of filenames
        """
        self.__files = files

    def process(self, message_queue):
        """
        Provide (stream) the audio data

        During the stream-loop, messages to add/remove consumers are handled.
        """
        log = log_to_stderr(level=logging.DEBUG)
        consumers = {}

        for fullpath in cycle(self.__files):
            log.debug('Streaming %s to %d consumers' % (fullpath, len(consumers)))

            fp = open(fullpath, 'rb')
            for chunk in fp:
                msg = None
                try:
                    msg = message_queue.get_nowait()
                except Empty:
                    # no message received. Continue normally
                    pass

                # Handle messages
                if msg:
                    if msg.op == Message.ADD:
                        consumers[msg.uuid] = msg.payload
                        log.info('Added %s to consumers' % msg.uuid)
                    else:
                        try:
                            result = consumers.pop(msg.uuid, None)
                            if result:
                                log.info('Removed %s from consumers' % msg.uuid)
                            else:
                                log.info('%s was not a registsred consumer' % msg.uuid)
                        except ValueError, exc:
                            log.debug(exc)

                # Send the data chunk to each consumer
                for consumer in consumers.values():
                    try:
                        consumer.put_nowait(chunk)
                    except Full:
                        # Queue is full! Silently ignore this event,
                        # effectively dropping the chunk.
                        pass

    def start(self, message_queue):
        LOG.info("starting, using the message queue: %s" % message_queue)
        p = Process(target=self.process, args=(message_queue,))
        p.start()
