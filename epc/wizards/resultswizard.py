# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ResultsWizard(models.TransientModel):
    _name = 'epc.wizard.result'
    
    activityinfo_id = fields.Many2one('epc.activityinfo', string='Activity info')
    line_ids = fields.One2many('epc.wizard.result.line', 'result_id')
    
    @api.one
    def validate_results(self):
        res_model = self.env['epc.activityinfo.result']
        for result in self.line_ids:
            res_ids = res_model.search([('activityinfo_id', '=', self.activityinfo_id.id), ('student_id', '=', result.student_id.id)])
            if res_ids:
                res_ids.write({'result': result.result})
            else:
                res_model.create({'activityinfo_id': self.activityinfo_id.id, 'student_id': result.student_id.id,'result': result.result})
        self.activityinfo_id.signal_workflow('to_be_signed')
        return True
    
class ResultsWizardLine(models.TransientModel):
    _name = 'epc.wizard.result.line'

    result_id = fields.Many2one('epc.wizard.result')
    student_id = fields.Many2one('res.partner', string='Student', required=True)
    result = fields.Float('Result')
