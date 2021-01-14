# -*- coding: utf-8 -*-
from flectra import http

# class FtoAttendance(http.Controller):
#     @http.route('/fto_attendance/fto_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fto_attendance/fto_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fto_attendance.listing', {
#             'root': '/fto_attendance/fto_attendance',
#             'objects': http.request.env['fto_attendance.fto_attendance'].search([]),
#         })

#     @http.route('/fto_attendance/fto_attendance/objects/<model("fto_attendance.fto_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fto_attendance.object', {
#             'object': obj
#         })