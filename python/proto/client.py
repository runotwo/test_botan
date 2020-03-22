import grpc

from . import insta_pb2 as proto
from . import insta_pb2_grpc


class Client:
    def __init__(self):
        self.channel = grpc.insecure_channel('0.0.0.0:3000')
        self.stub = insta_pb2_grpc.InstaServiceStub(self.channel)

    def get_data(self, usernames):
        resp = self.stub.GetProfiles(proto.ProfilesData(profiles=[proto.Profile(username=username) for username in usernames]))
        return resp
