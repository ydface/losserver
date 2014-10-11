#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Ydface'

import sys
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor
import json
from handler import ServerHandler


class CmdProtocol(LineReceiver):

    delimiter = '\n'

    def __init__(self):
        self.client_ip = None
        self.handler = None

    def connectionMade(self):
        self.handler = ServerHandler()

        log.msg(self.transport)
        self.client_ip = self.transport.getPeer().host
        log.msg("Client connection from %s" % self.client_ip)
        if len(self.factory.clients) >= self.factory.clients_max:
            log.msg("Too many connections. bye !")
            self.client_ip = None
            self.transport.loseConnection()
        else:
            self.factory.clients.append(self.client_ip)
            self.transport.write("test")
            log.msg("Current client number is %d" % len(self.factory.clients))

    def connectionLost(self, reason):
        log.msg('Lost client connection.  Reason: %s' % reason)
        if self.client_ip:
            self.factory.clients.remove(self.client_ip)
            log.msg("Current client number is %d" % len(self.factory.clients))

    def lineReceived(self, line):
        msg = json.loads(line)
        method = msg["method"]
        params = msg["params"]

        self.handler.run(method, params)


class ServerPool(ServerFactory):

    protocol = CmdProtocol

    def __init__(self, clients_max=500):
        self.clients_max = clients_max
        self.clients = []


def start():
    log.startLogging(sys.stdout)
    reactor.listenTCP(6888, ServerPool())
    reactor.run()