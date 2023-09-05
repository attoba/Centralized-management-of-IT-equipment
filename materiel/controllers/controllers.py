# -*- coding: utf-8 -*-
# from odoo import http


# class Materiel(http.Controller):
#     @http.route('/materiel/materiel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/materiel/materiel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('materiel.listing', {
#             'root': '/materiel/materiel',
#             'objects': http.request.env['materiel.materiel'].search([]),
#         })

#     @http.route('/materiel/materiel/objects/<model("materiel.materiel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('materiel.object', {
#             'object': obj
#         })
