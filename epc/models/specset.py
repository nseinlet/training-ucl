# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SpecSet(models.Model):
    _name = 'epc.specset'
    _inherit = 'mail.thread'
    _description = "Cahier de charge"
    _rec_name = 'validity'
    
    validity = fields.Integer('Validity')
    activity_id = fields.Many2one('epc.activity', string="Activity")
    language = fields.Char()
    skills = fields.Html("Skills to aquire")
    prerequisite = fields.Html(string="Prerequisite")

    _sql_constraints = [('activlang_uniq', 'unique(activity_id,language)', 'Specification set must be unique by language-activity!')]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        
        copied_count = self.search_count(
            [('language', '=like', u"{}%".format(self.language)), ('activity_id', "=", self.activity_id.id)])
        if not copied_count:
            new_language = u"{} (1)".format(self.language)
        else:
            new_language = u"{} ({})".format(self.language, copied_count+1)

        default['language'] = new_language
        return super(SpecSet, self).copy(default)
