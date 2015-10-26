# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Activity(models.Model):
    _name = 'epc.activity'
    _inherit = 'mail.thread'
    _description = "activity"
    _order = "sequence,name"
    
    name = fields.Char(track_visibility="always")
    sequence = fields.Integer()
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    ens_start = fields.Integer(track_visibility="always")
    ens_end = fields.Integer(track_visibility="always")
    description = fields.Text()
    specset_ids = fields.One2many('epc.specset', 'activity_id', string="Cahiers de charge")
    activityinfo_ids = fields.One2many('epc.activityinfo', 'activity_id', string="Infos")
    active = fields.Boolean(default=True)
    country_id = fields.Many2one('res.country', related="responsible_id.country_id")
