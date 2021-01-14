# -*- coding: utf-8 -*-
from flectra import http

# class FtoUser(http.Controller):
#     @http.route('/fto_user/fto_user/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fto_user/fto_user/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fto_user.listing', {
#             'root': '/fto_user/fto_user',
#             'objects': http.request.env['fto_user.fto_user'].search([]),
#         })

#     @http.route('/fto_user/fto_user/objects/<model("fto_user.fto_user"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fto_user.object', {
#             'object': obj
#         })