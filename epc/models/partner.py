# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)
    student = fields.Boolean("Student", default=False)
    activityinfo_ids = fields.Many2many('epc.activityinfo', relation='epc_student_activityinfo', column1='student_id', column2='activity_id')
    
