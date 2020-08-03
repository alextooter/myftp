from asynchat import async_chat
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

encoding="GB18030"

class EncodedProducer:
    def __init__(self, producer):
        self.producer = producer
    def more(self):
        return self.producer.more().decode("utf8").encode(encoding)

class EncodedHandler(FTPHandler):

    def push(self, s):
        async_chat.push(self, s.encode(encoding))

    def push_dtp_data(self, data, isproducer=False, file=None, cmd=None):
        if file==None:
            if isproducer:
                data=EncodedProducer(data)
            else:
                data=data.decode("utf8").encode(encoding)

        FTPHandler.push_dtp_data(self, data, isproducer, file, cmd)

    def decode(self, bytes):
        return bytes.decode(encoding, self.unicode_errors)






def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('1', '1', '/')
    handler = EncodedHandler

    handler.authorizer = authorizer
    server = ThreadedFTPServer(('', 21), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
