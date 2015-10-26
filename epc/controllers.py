# -*- coding: utf-8 -*-
from openerp import http

class epc(http.Controller):
    @http.route('/epc/', auth='public', website=True)
    def index(self, **kw):
        act = http.request.env['epc.activity'].sudo()
        return http.request.render('epc.listing', {
            'objects': act.search([]),
        })
        
    @http.route('/epc/<model("epc.activity"):acti>', auth='public', website=True)
    def activity(self, acti):
        return http.request.render('epc.activity_page', {
            'activite': acti,
        })

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
