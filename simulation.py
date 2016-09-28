#!/usr/bin/env python
# -*- coding: utf-8
"""Simulation docstring."""

import sys

class Queue:

    def __init__(self):
        self.array = []

    def enqueue(self, item):
        self.array.insert(0, item)

    def dequeue(self):
        if not self.array:
            return None
        return self.array.pop()

    def allItems(self):
        return self.array

    def isEmpty(self):
        return len(self.array) == 0

class Server:

    def __init__(self):
        self.queue = Queue()
        self.currentRequest = None

    def addRequest(self, request):
        self.queue.enqueue(request)

    def incrementRequestTimers(self):
        for request in self.queue.allItems():
            request.incrementWaitTime()
        if self.currentRequest:
            self.currentRequest.incrementRunningTime()

    def processNextRequest(self):
        self.currentRequest = self.queue.dequeue()

        if self.currentRequest:
            return self.currentRequest.getWaitTime()

        return 0

    def isRequestDone(self):
        return self.currentRequest == None or self.currentRequest.isDone()

    def hasRequestsQueued(self):
        return not self.queue.isEmpty()

class Request:

    def __init__(self, second, request_url, duration):
        self.second = second
        self.request_url = request_url
        self.duration = duration
        self.runningTime = 0
        self.waitTime = 0

    def getSecond(self):
        return self.second

    def getRequestURL(self):
        return self.request_url

    def getDuration(self):
        return self.duration

    def incrementWaitTime(self):
        self.waitTime += 1

    def getWaitTime(self):
        return self.waitTime

    def incrementRunningTime(self):
        self.runningTime += 1

    def isDone(self):
        return self.runningTime >= self.duration

    def __str__(self):
        return "%s,%s,%s"%(self.second, self.request_url, self.duration)

    def __repr__(self):
        return str(self)

def simulateOneServer(requests):
    seconds = 1
    index = 0
    waitTime = 0.0
    server = Server()

    while index < len(requests):
        while index < len(requests) and requests[index].getSecond() == seconds:
            server.addRequest(requests[index])
            index += 1

        if server.isRequestDone():
            temp = server.processNextRequest()
            waitTime += temp

        server.incrementRequestTimers()
        seconds += 1

    while server.hasRequestsQueued():
        if server.isRequestDone():
            temp = server.processNextRequest()
            waitTime += temp

        server.incrementRequestTimers()

    return waitTime / len(requests)

def simulateManyServers(requests, server_count):
    seconds = 1
    index = 0
    waitTime = 0.0
    currentServerIndex = 0
    servers = []

    for i in range(server_count):
        servers.append(Server())

    while index < len(requests):
        while index < len(requests) and requests[index].getSecond() == seconds:
            servers[currentServerIndex].addRequest(requests[index])
            index += 1
            currentServerIndex = (currentServerIndex + 1) % server_count

        for server in servers:
            if server.isRequestDone():
                temp = server.processNextRequest()
                waitTime += temp
            server.incrementRequestTimers()

        seconds += 1

    for server in servers:
        while server.hasRequestsQueued():
            if server.isRequestDone():
                temp = server.processNextRequest()
                waitTime += temp

            server.incrementRequestTimers()

    return waitTime / len(requests)

def main():
    request_list = []

    input_file = ""
    server_count = 1

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--file":
            input_file = sys.argv[i+1]
        if sys.argv[i] == "--servers":
            server_count = int(sys.argv[i+1])
        i += 2

    with open(input_file) as f:
        for line in f:
            tokens = line.strip().split(",")
            request_list.append(Request(int(tokens[0]),
                                        tokens[1].strip(),
                                        int(tokens[2])))

    request_list.sort(key=lambda x: x.second)

    if server_count == 1:
        print("Servers: 1")
        print("Average wait time: "+str(simulateOneServer(request_list))+" seconds")
    else:
        print("Servers: "+str(server_count))
        print("Average wait time: "+str(simulateManyServers(request_list,server_count)) +" seconds")

if __name__ == '__main__':
    main()
