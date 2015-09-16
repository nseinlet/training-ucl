# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ActivityInfo(models.Model):
    _name = 'epc.activityinfo'
    _inherit = 'mail.thread'
    _inherits = [['epc.activity','activity_id'],]
    _description = "Activity Info"
    
    complete_name = fields.Char('Complete name')
    code = fields.Char(compute='_compute_code',store=True,select=1)
    site = fields.Char(compute='_compute_site')
    validity = fields.Integer('Validity')
    sigle = fields.Char('Sigle', required=True)
    cnum = fields.Integer('CNum', required=True)
    subdivision = fields.Char('Subdivision')
    activity_type = fields.Selection([('COURS', 'Cours'), ('PARTIM', 'Partim'), ('THESE', 'Thèse'), ('CLASSE', 'Classe')])
    student_ids = fields.Many2many('res.partner')
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
                raise ValidationError("Your total is not equal to the sum of the 2 quarters : %s + %s != %s" % (record.vol1_q1, record.vol1_q2,  record.vol1_total))
                
    @api.constrains('vol2_total')
    def _check_total_vol2(self):
        for record in self:
            if round(record.vol2_q1 + record.vol2_q2 - record.vol2_total,2)!=0 and (record.vol2_q1!=0 or record.vol2_q2!=0):
                raise ValidationError("Your total is not equal to the sum of the 2 quarters : %s + %s != %s" % (record.vol2_q1, record.vol2_q2,  record.vol2_total))
