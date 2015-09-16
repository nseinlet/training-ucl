# -*- coding: utf-8 -*-
from openerp import http

# class ../epc/(http.Controller):
#     @http.route('/../epc//../epc//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/../epc//../epc//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('../epc/.listing', {
#             'root': '/../epc//../epc/',
#             'objects': http.request.env['../epc/.../epc/'].search([]),
#         })

#     @http.route('/../epc//../epc//objects/<model("../epc/.../epc/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('../epc/.object', {
#             'object': obj
#         })