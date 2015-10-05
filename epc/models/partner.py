# -*- coding: utf-8 -*-
from openerp import fields, models, api

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)
    student = fields.Boolean("Student", default=False)
    activityinfo_ids = fields.Many2many('epc.activityinfo', relation='epc_student_activityinfo', column1='student_id', column2='activity_id')
    entity_ids = fields.Many2many('epc.entity', relation='epc_partner_entity', column1='partner_id', column2='entity_id')
    entity_id = fields.Many2one('epc.entity')
    courses_count = fields.Integer('N° of courses', compute='_get_nbr_courses')
    courses_prc = fields.Integer('Percentage of courses', compute='_get_prc_courses')
    courses_daily = fields.Char('Skills', compute='_get_courses_daily')
    #registration_date = fields.Date(default=lambda self: fields.Date.today())
    registration_date = fields.Date(default=fields.Date.today)
    
    @api.one
    def _get_courses_daily(self):
        a = unicode([
            { "tooltip" : "Old", "value": 5},
            { "tooltip" : "New", "value": 7},
            { "tooltip" : "New 2", "value": 7},
            { "tooltip" : "New 3", "value": 7},
        ]).replace("'","\"")
        self.courses_daily = a
        
    @api.one
    def _get_nbr_courses(self):
        self.courses_count = len(self.activityinfo_ids)
        
    @api.one
    @api.depends('activityinfo_ids')
    def _get_prc_courses(self):
        nbr = self.env['epc.activityinfo'].sudo().search_count([])
        if not nbr:
            self.courses_prc = 0.0
        else:
            self.courses_prc = 100.0 * len(self.activityinfo_ids) / nbr
            
    @api.multi
    def courses_list(self):
        return {
            'name': 'Student courses',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'epc.activityinfo',
            'type': 'ir.actions.act_window',
            #'domain': [['id', 'in', self.activityinfo_ids.ids]],
            'domain': [['student_ids.id', "=", self.id]]
        }
    
