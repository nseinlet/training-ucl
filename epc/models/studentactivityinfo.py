# -*- coding: utf-8 -*-
from openerp import models, fields, api, tools, exceptions, _
import datetime

class StudentActivityInfo(models.Model):
    _name="epc.student.activityinfo"

    student_id = fields.Many2one('res.partner', domain="[('student', '=', True)]", string="Student")
    activity_id = fields.Many2one('epc.activityinfo', string='Info')
    registration_date = fields.Date(string = 'Registration date')
