# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Entity(models.Model):
    _name = 'epc.entity'
    _inherit = 'mail.thread'
    
    name = fields.Char(required=True)
    validity_start = fields.Datetime()
    validity_end = fields.Datetime()
    parent_id = fields.Many2one('epc.entity', string='Parent entity', select=True, ondelete='restrict')
    child_ids = fields.One2many('epc.entity', 'parent_id', string='Child Entities')
    parent_left = fields.Integer('Left Parent', select=1)
    parent_right = fields.Integer('Right Parent', select=1)
    activites_charge_ids = fields.One2many('epc.activityinfo', 'entity_id', string='Activities')
    activites_attrib_ids = fields.One2many('epc.activityinfo', 'entity_attrib_id', string='Attributed activities')
    
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
