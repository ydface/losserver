#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Ydface'

from core.callback import Callback


class ServerHandler(Callback):
    @Callback.callback("save_exp")
    def save_exp(self, params):
        print params
        return None

    def run(self, event, params):
        self.dispatch(event)(params)
