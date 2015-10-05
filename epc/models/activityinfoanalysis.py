# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _, tools

class ActivityInfoAnalysis(models.Model):
    _name = "epc.activityinfo.analysis"
    _description = "Course and session analysis"
    _order='name'
    _auto = False

    name = fields.Char(string="Title")
    code = fields.Char()
    validity = fields.Integer('Validity')
    sigle = fields.Char('Sigle')
    cnum = fields.Integer('CNum')
    subdivision = fields.Char('Subdivision')
    responsible_id = fields.Many2one('res.users', string="responsible")
    country_id = fields.Many2one('res.country')
    students_count = fields.Integer()
    
    def init(self, cr):
        #tools.sql.drop_view_if_exists(cr, 'academy_session_analysis')
        cr.execute('''CREATE OR REPLACE VIEW epc_activityinfo_analysis AS (
            select info.id, act.responsible_id, prtn.country_id, 
            info.code, act.name, info.validity, info.sigle,
            info.cnum, info.subdivision, info.students_count
            from epc_activity as act
            inner join epc_activityinfo as info on act.id=info.activity_id
            left join res_partner as prtn on prtn.id=act.responsible_id)''')
