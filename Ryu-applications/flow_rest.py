
import logging

from time import sleep
import json
from webob import Response
import os
import mimetypes

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller import dpset
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_3
from ryu.lib import ofctl_v1_0
from ryu.lib import ofctl_v1_3
from ryu.app.wsgi import ControllerBase, WSGIApplication
from flow_core import FlowCore
from ryu.ofproto import inet
from pprint import pprint
import networkx as nx
LOG = logging.getLogger('ryu.app.flow_rest')


class FlowController(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(FlowController, self).__init__(req, link, data, **config)
        self.flow = data['flow']
        self.flow.dpset = data['dpset']

    def filter(self, body):
        return True
        #Todo:
        #Verify if body have the source and destination information;
        #Verify if source != dest, because host-to-host flow to same switch is non sense!
        #Verify if source ip is valid; Verify if dest ip is valid;
        #return true.

    def create_intent(self, req, **_kwargs):
        try:
            rest = req.json if req.body else {}
        except SyntaxError:
            response = Response(status=400, headerlist=[('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Headers', 'Content-Type, Cache-Control')])
            return response
        try:
            if self.flow.create_intent_internal(rest):
                body = json.dumps({'result': 'success'})
                response = Response(content_type='application/json', status=200, body=body)
                response.headers.update({
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type, Cache-Control"
                })
                return response
        except (RuntimeError, TypeError, NameError, KeyError, nx.NetworkXNoPath) as message:
                body = json.dumps({'result': 'failure', 'message': str(message)})
                response = Response(content_type='application/json', body=body)
                response.headers.update({
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type, Cache-Control"
                })
                return response

    def delete_intent(self, req, **_kwargs):
        pass

class FlowApi(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {
        'dpset': dpset.DPSet,
        'wsgi': WSGIApplication,
        'flow': FlowCore
    }

    def __init__(self, *args, **kwargs):
        super(FlowApi, self).__init__(*args, **kwargs)
        self.dpset = kwargs['dpset']
        flow = kwargs['flow']
        wsgi = kwargs['wsgi']
        self.waiters = {}
        self.data = {}
        self.data['dpset'] = self.dpset
        self.data['waiters'] = self.waiters
        self.data['flow'] = flow
        wsgi.registory['FlowController'] = self.data
        mapper = wsgi.mapper

        mapper.connect('flow', '/intent/add',
                       controller=FlowController, action='create_intent',
                       conditions=dict(method=['POST']))

        mapper.connect('flow', '/intent/del',
                       controller=FlowController, action='delete_intent',
                       conditions=dict(method=['POST']))

