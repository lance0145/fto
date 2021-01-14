# -*- coding: utf-8 -*-
from flectra import http

# class FtoShiftManagement(http.Controller):
#     @http.route('/fto_shift_management/fto_shift_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fto_shift_management/fto_shift_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fto_shift_management.listing', {
#             'root': '/fto_shift_management/fto_shift_management',
#             'objects': http.request.env['fto_shift_management.fto_shift_management'].search([]),
#         })

#     @http.route('/fto_shift_management/fto_shift_management/objects/<model("fto_shift_management.fto_shift_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fto_shift_management.object', {
#             'object': obj
#         })