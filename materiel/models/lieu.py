from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Lieu(models.Model):
    _name = 'materiel.lieu'
    _rec_name = 'lieu'
    _inherit = {"mail.thread"}
    _description = 'Materiel Lieu'

    lieu = fields.Char(string='Lieu', required=True, store=True)
    type = fields.Selection([('Salle', 'Salle'), ('Amphi', 'Amphi'), ('Bureau', 'Bureau'), ('Personnel', 'Personnel')],
                            string='Type')
    configuration = fields.Text(related='mat_ids.configuration', string='Configuration', store=True)
    mat_ids = fields.One2many('materiel.materiel', 'lieu_id', string='Matériel')
    photo = fields.Image(related='mat_ids.photo', string='Photo', store=True)
    designation = fields.Char(related='mat_ids.designation', string='Désignation', store=True)
    marque = fields.Char(related='mat_ids.marque', string='Marque', store=True)
    serie = fields.Char(related='mat_ids.serie', string='Série', store=True)
    quantite = fields.Integer(compute='_compute_quantite', string='Quantité', store=True)
    display_name = fields.Char(compute='_compute_display_name', store=True, string='Display Name')

    @api.depends('lieu')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.lieu

    @api.depends('mat_ids')
    def _compute_quantite(self):
        for classroom in self:
            classroom.quantite = len(classroom.mat_ids)

    @api.constrains('mat_ids')
    def _check_unique_material_recording(self):
        for lieu_record in self:
            for material in lieu_record.mat_ids:
                # Search for other records containing the same material
                domain = [('id', '!=', lieu_record.id), ('mat_ids', 'in', material.id)]
                duplicate_records = self.search(domain, limit=1)
                if duplicate_records:
                    raise ValidationError(
                        f"Vous avez sélectionné un matériel qui est déjà déplacé dans un lieu."
                    )
