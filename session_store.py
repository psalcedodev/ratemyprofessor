import os
import base64


class SessionStore:

    def __init__(self):
        self.sessions = {}

    def createSession(self):
        newSessionID = self.generateSessionId()
        self.sessions[newSessionID] = {}
        return newSessionID

    def getSession(self, sessionId):
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr
