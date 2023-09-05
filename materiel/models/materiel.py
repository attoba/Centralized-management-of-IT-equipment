from odoo import models, fields, api
from odoo.exceptions import ValidationError



class Materiel(models.Model):
    _name = "materiel.materiel"
    _inherit = {"mail.thread"}
    _rec_name = 'n_inventaire'
    _description = "Materiel Records"

    n_inventaire = fields.Char(string='Numéro d\'inventaire ', tracking=True)

    designation = fields.Char(string='Désignation', required=True, tracking=True)
    marque = fields.Char(string='Marque', required=True, tracking=True)
    etat = fields.Selection([('En bon etat', 'En bon état'), ('En panne', 'En panne')],
                            string='Etat', required=True, tracking=True, default='En bon etat')
    date_achat = fields.Date(string="Date d'achat", required=True, tracking=True)
    serie = fields.Char(string='Série', required=True, tracking=True)
    cause = fields.Text(string='Cause', tracking=True)
    solution = fields.Text(string='Solution', tracking=True)
    configuration = fields.Text(string='Configuration', tracking=True)
    photo = fields.Binary(string='Photo', tracking=True)
    lieu_id = fields.Many2one('materiel.lieu', string='Lieu', store=True)


    def _onchange_lieu_id(self):
        for material in self:
            if material.lieu_id:
                # Remove the material from the old 'materiel.lieu' record
                old_lieu = material._origin.lieu_id
                old_lieu.mat_ids -= material

                # Add the material to the new 'materiel.lieu' record
                new_lieu = material.lieu_id
                new_lieu.mat_ids += material

            else:
                # If no 'lieu_id' is selected, just remove it from the old 'materiel.lieu' record
                old_lieu = material._origin.lieu_id
                old_lieu.mat_ids -= material


    @api.constrains('n_inventaire')
    def _check_unique_inventory_number(self):
        for material in self:
            if material.n_inventaire:
                # Recherche de matériel avec le même numéro d'inventaire
                duplicate_material = self.search([('n_inventaire', '=', material.n_inventaire), ('id', '!=', material.id)],
                                                 limit=1)
                if duplicate_material:
                    raise ValidationError("Un matériel avec le même numéro d'inventaire existe déjà !")
