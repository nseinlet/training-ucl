# -*- coding: utf-8 -*-
from openerp import models, fields, api, tools, exceptions, _
import datetime

class ActivityInfo(models.Model):
    _name = 'epc.activityinfo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherits = [['epc.activity','activity_id'],]
    _description = "Activity Info"
    
    complete_name = fields.Char('Complete name')
    code = fields.Char(compute='_compute_code',store=True,select=1)
    site = fields.Char(compute='_compute_site')
    picture = fields.Binary()
    validity = fields.Integer('Validity')
    sigle = fields.Char('Sigle', required=True)
    cnum = fields.Integer('CNum', required=True)
    subdivision = fields.Char('Subdivision')
    activity_type = fields.Selection([('COURS', 'Cours'), ('PARTIM', 'Partim'), ('THESE', 'Thèse'), ('CLASSE', 'Classe')])
    student_ids = fields.Many2many('res.partner', domain="[('student', '=', 1)]", relation='epc_student_activityinfo', column1='activity_id', column2='student_id')
    stud_ids = fields.One2many('epc.student.activityinfo', 'activity_id', string="Students")
    entity_id = fields.Many2one('epc.entity', string='Entity', ondelete="restrict")
    entity_attrib_id = fields.Many2one('epc.entity', string="Entity attributed", ondelete="restrict")
    vol_total = fields.Float(default=0)
    vol1_total = fields.Float(default=0)
    vol1_q1 = fields.Float(default=0)
    vol1_q2 = fields.Float(default=0)
    vol1_coeff = fields.Integer(default=0)
    vol2_total = fields.Float(default=0)
    vol2_q1 = fields.Float(default=0)
    vol2_q2 = fields.Float(default=0)
    vol2_coeff = fields.Integer(default=0)
    date_start = fields.Date('Begin')
    date_end = fields.Date('End')
    students_count = fields.Integer(
        string="students count", compute='_get_students_count', store=True)
    color = fields.Integer()
    state = fields.Selection([
        ('draft', "Draft"),
        ('in_progress', "In progress"),
        ('give_result', "Give results"),
        ('to_be_signed', "Results to be signed"),
        ('done', "Done"),
    ], default='draft', track_visibility="always")
    result_ids = fields.One2many('epc.activityinfo.result', 'activityinfo_id', string="Results")
    
        
    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_in_progress(self):
        self.state = 'in_progress'

    @api.multi
    def action_give_result(self):
        self.state = 'give_result'

    @api.multi
    def action_to_be_signed(self):
        self.state = 'to_be_signed'

    @api.multi
    def action_done(self):
        self.state = 'done'
        
    @api.onchange('entity_id')
    def _check_entity_attrib_id(self):
        if self.entity_id:
            self.entity_attrib_id=self.entity_id
            
    @api.one
    @api.depends('sigle', 'cnum', 'subdivision')
    def _compute_code(self):
        self.code = "%s%s%s" % (self.sigle, self.cnum, self.subdivision if self.subdivision else "")
            
    @api.one
    @api.depends('sigle')
    def _compute_site(self):
        self.site = self.sigle[0] if self.sigle else ""

    @api.constrains('vol1_total')
    def _check_total_vol1(self):
        for record in self:
            if round(record.vol1_q1 + record.vol1_q2 - record.vol1_total,2)!=0 and (record.vol1_q1!=0 or record.vol1_q2!=0):
                raise ValidationError(_("Your total is not equal to the sum of the 2 quarters : %s + %s != %s") % (record.vol1_q1, record.vol1_q2,  record.vol1_total))
                
    @api.constrains('vol2_total')
    def _check_total_vol2(self):
        for record in self:
            if round(record.vol2_q1 + record.vol2_q2 - record.vol2_total,2)!=0 and (record.vol2_q1!=0 or record.vol2_q2!=0):
                raise ValidationError(_("Your total is not equal to the sum of the 2 quarters : %s + %s != %s") % (record.vol2_q1, record.vol2_q2,  record.vol2_total))

    @api.onchange('date_start', 'date_end')
    def _verify_dates(self):
        if self.date_start and not self.date_end:
            self.date_end = fields.Datetime.to_string(fields.Datetime.from_string(self.date_start) + datetime.timedelta(days=600))
        if self.date_start and self.date_end and self.date_end < self.date_start:
            return {
                'warning': {
                    'title': _("Incorrect dates"),
                    'message': _("Finish date must be greater or equal to begin date"),
                },
            }

    @api.depends('student_ids')
    def _get_students_count(self):
        for r in self:
            r.students_count = len(r.student_ids)
            
    @api.multi
    def wizard_encode_results(self):
        wiz_id = self.env['epc.wizard.result'].create({
            'activityinfo_id': self.id,
            'line_ids':[(0,0,{'student_id': student.id}) for student in self.student_ids],
        })
            
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'epc.wizard.result',
            'res_id': wiz_id.id,
            'target': 'new',
        }
        
    @api.model
    def _needaction_domain_get(self):
        return [('state', '=', 'give_result')]
    
    @api.multi
    def mamethode(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'epc.wizard.result',
            'res_id': wiz_id.id,
            'target': 'new',
        }    
        
class ActivityInfoResults(models.Model):
    _name = 'epc.activityinfo.result'
    
    activityinfo_id = fields.Many2one('epc.activityinfo', string='Activity info')
    student_id = fields.Many2one('res.partner', string='Student', required=True)
    result = fields.Float('Result')
    
