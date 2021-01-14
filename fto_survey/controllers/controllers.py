# -*- coding: utf-8 -*-
from flectra import http

# class FtoSurvey(http.Controller):
#     @http.route('/fto_survey/fto_survey/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fto_survey/fto_survey/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fto_survey.listing', {
#             'root': '/fto_survey/fto_survey',
#             'objects': http.request.env['fto_survey.fto_survey'].search([]),
#         })

#     @http.route('/fto_survey/fto_survey/objects/<model("fto_survey.fto_survey"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fto_survey.object', {
#             'object': obj
#         })