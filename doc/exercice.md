module creation
===============

odoo.py scaffold epc

Models
======

- create a new rep with an __init__.py
- create a new activity class in this rep

```
# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Activity(models.Model):
    _name = 'epc.activity'
    _description = "activity"
    
    name = fields.Char()
    ens_start = fields.Integer()
    ens_end = fields.Integer()
    description = fields.Text()
```

- Install/Update the module in odoo
- Check if the model exist in the database

Demo datas
----------

```
<openerp>
    <data>
        <record model="epc.activity" id="Activity0">
            <field name="name">Activity 0</field>
            <field name="description">Activity 0's description

Can have multiple lines
            </field>
        </record>
        <record model="epc.activity" id="Activity1">
            <field name="name">Activity 1</field>
            <!-- no description for this one -->
        </record>
        <record model="epc.activity" id="Activity2">
            <field name="name">Activity 2</field>
            <field name="description">Activity 2's description</field>
        </record>
    </data>
</openerp>
```

Menu items
----------

- create a menu to access the activities

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <!-- window action -->
        <!--
            The following tag is an action definition for a "window action",
            that is an action opening a view or a set of views
        -->
        <record model="ir.actions.act_window" id="activity_list_action">
            <field name="name">Activities</field>
            <field name="res_model">epc.activity</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="oe_view_nocontent_create">Create the first Activity
                </p>
            </field>
        </record>

        <!-- top level menu: no parent -->
        <menuitem id="main_epc_menu" name="Open Academy"/>
        <!-- A first level in the left side menu is needed
             before using action= attribute -->
        <menuitem id="epc_menu" name="Open Academy"
                  parent="main_epc_menu"/>
        <!-- the following menuitem should appear *after*
             its parent epc_menu and *after* its
             action activity_list_action -->
        <menuitem id="activitys_menu" name="Activities" parent="epc_menu"
                  action="activity_list_action"/>
        <!-- Full id location:
             action="epc.activity_list_action"
             It is not required when it is the same module -->
    </data>
</openerp>
```

Form view
=========

- Customise form view using XML

Create your own form view for the activity object. Data displayed should be: the name and the description of the activity.

```
<record model="ir.ui.view" id="activity_form_view">
    <field name="name">activity.form</field>
    <field name="model">epc.activity</field>
    <field name="arch" type="xml">
        <form string="Activity Form">
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="description"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

- Notebooks

In the activity form view, put the description field under a tab, such that it will be easier to add other tabs later, containing additional information.

```
<record model="ir.ui.view" id="activity_form_view">
    <field name="name">activity.form</field>
    <field name="model">epc.activity</field>
    <field name="arch" type="xml">
        <form string="Activity Form">
            <sheet>
                <group>
                    <field name="name"/>
                </group>
                <notebook>
                    <page string="Schedule">
                        <group col="4">
                            <field name="ens_start"/>
                            <field name="ens_end"/>
                        </group>
                    </page>
                    <page string="Description">
                        <field name="description"/>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```

Search view
===========

- Search Activities

Allow searching for Activities based on their title or their description.

```
<record model="ir.ui.view" id="activity_search_view">
    <field name="name">activity.search</field>
    <field name="model">epc.activity</field>
    <field name="arch" type="xml">
        <search>
            <field name="name"/>
            <field name="description"/>
            <field name="ens_start"/>
            <field name="ens_end"/>
        </search>
    </field>
</record>
```

- Add "group by" on ens_start and ens_end

```
<record model="ir.ui.view" id="activity_search_view">
    <field name="name">activity.search</field>
    <field name="model">epc.activity</field>
    <field name="arch" type="xml">
        <search>
            <field name="name"/>
            <field name="description"/>
            <field name="ens_start"/>
            <field name="ens_end"/>
            <group string="Group By">
                <filter name="group_by_start" string="Start" context="{'group_by': 'ens_start'}"/>
                <filter name="group_by_end" string="End" context="{'group_by': 'ens_end'}"/>
            </group>
        </search>
    </field>
</record>
```

- Add filter for ens_start="2015" and ens_end="2015"

```
<record model="ir.ui.view" id="activity_search_view">
    <field name="name">activity.search</field>
    <field name="model">epc.activity</field>
    <field name="arch" type="xml">
        <search>
            <field name="name"/>
            <field name="description"/>
            <field name="ens_start"/>
            <field name="ens_end"/>
            <group string="Group By">
                <filter name="group_by_start" string="Start" context="{'group_by': 'ens_start'}"/>
                <filter name="group_by_end" string="End" context="{'group_by': 'ens_end'}"/>
            </group>
            <filter name="2015 activities" domain="[('ens_start', '=', 2015), ('ens_end', '=', 2015)]"
				string="2015 activities"/>
			<field name="name"/>
        </search>
    </field>
</record>
```

Relation between models
=======================

Create a CahierCharge model

```
# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SpecSet(models.Model):
    _name = 'epc.specset'
    _description = "Cahier de charge"
    _rec_name = 'validity'
    
    validity = fields.Integer('Validity')
    language = fields.Char()
    skills = fields.Html("Skills to aquire")
    prerequisite = fields.Html(string="Prerequisite")
    
```

Many2one relations
------------------

Using a many2one, modify the activity and SpecSet models to reflect their relation with other models:

- A SpecSet is related to a activity; the value of that field is a record of the model epc.activity and is required.
- Adapt the views.
- Add the relevant Many2one fields to the models, and
- add them in the views.

One2many relations
------------------

- add the reflecting One2many in activity corresponding to the many2one in specset

```
# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Activity(models.Model):
    _name = 'epc.activity'
    _description = "activity"
    _rec_name = 'name'
    
    name = fields.Char()
    ens_start = fields.Integer()
    ens_end = fields.Integer()
    description = fields.Text()
    specset_ids = fields.One2many('epc.specset', 'activity_id', string="Cahiers de charge")
```

```
# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SpecSet(models.Model):
    _name = 'epc.specset'
    _description = "Cahier de charge"
    _rec_name = 'validity'
    
    validity = fields.Integer('Validity')
    activity_id = fields.Many2one('epc.activity', string="Activity")
    language = fields.Char()
    skills = fields.Html("Skills to aquire")
    prerequisite = fields.Html(string="Prerequisite")
```

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <!-- Search -->
        <record model="ir.ui.view" id="activity_search_view">
            <field name="name">activity.search</field>
            <field name="model">epc.activity</field>
            <field name="arch" type="xml">
                <search>
                    <field name="name"/>
                    <field name="description"/>
                    <field name="ens_start"/>
                    <field name="ens_end"/>
                </search>
            </field>
        </record>
        
        <!-- Form -->
        <record model="ir.ui.view" id="activity_form_view">
            <field name="name">activity.form</field>
            <field name="model">epc.activity</field>
            <field name="arch" type="xml">
                <form string="Activity Form">
                    <sheet>
                        <group>
                            <field name="name"/>
                        </group>
                        <notebook>
                            <page string="Schedule">
                                <group col="4">
                                    <field name="ens_start"/>
                                    <field name="ens_end"/>
                                </group>
                            </page>
                            <page string="Description">
                                <field name="description"/>
                            </page>
                            <page string="Specset">
                                <field name="specset_ids">
                                    <tree>
                                        <field name="validity"/>
                                        <field name="language"/>
                                    </tree>
                                </field>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>
    </data>
</openerp>
```

```
<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data>
        <!-- List -->
        <record model="ir.ui.view" id="epc_view_specset_tree">
            <field name="name">epc.view.specset_tree</field>
            <field name="model">epc.specset</field>
            <field name="priority" eval="16"/>
            <field name="arch" type="xml">
                <tree string="Specset">
                    <field name="validity"/>
                    <field name="activity_id"/>
                    <field name="language"/>
                    <field name="skills"/>
                    <field name="prerequisite"/>
                </tree>
            </field>
        </record>
        
        <!-- Form -->
        <record model="ir.ui.view" id="epc_specset_form">
            <field name="name">epc.view.specsetform</field>
            <field name="model">epc.specset</field>
            <field name="priority" eval="16"/>
            <field name="arch" type="xml">
                <form string="Specset">
                    <sheet>
                        <group col="2">
                            <field name="validity"/>
                            <field name="activity_id"/>
                            <field name="language"/>
                            <field name="skills"/>
                            <field name="prerequisite"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>
            
    </data>
</openerp>
```

- Edit searchview to add custom domain

```
<record model="ir.ui.view" id="activity_search_view">
    <field name="name">activity.search</field>
    <field name="model">epc.activity</field>
    <field name="arch" type="xml">
        <search>
            <field name="name"/>
            <field name="description"/>
            <field name="ens_start"/>
            <field name="ens_end"/>
            <field name="specset_ids" filter_domain="['|', '|', ('specset_ids.language','ilike',self), ('specset_ids.skills','ilike',self), ('specset_ids.prerequisite','ilike',self)]"/>
            <group string="Group By">
                <filter name="group_by_start" string="Start" context="{'group_by': 'ens_start'}"/>
                <filter name="group_by_end" string="End" context="{'group_by': 'ens_end'}"/>
            </group>
            <filter name="2015 activities" domain="[('ens_start', '=', 2015), ('ens_end', '=', 2015)]"
				string="2015 activities"/>
			<field name="name"/>
        </search>
    </field>
</record>
```

Many2many
---------

We'll do many2many after the inheritance

Inheritance
===========

Traditional (_name == _inherit)
-------------------------------

Using model inheritance, modify the existing Partner model to add an instructor boolean field, and a many2many field that corresponds to the session-partner relation

```
# -*- coding: utf-8 -*-
from openerp import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    student = fields.Boolean("Student", default=False)
```

Using view inheritance, display this fields in the partner form view

```
<?xml version="1.0" encoding="UTF-8"?>
 <openerp>
    <data>
        <!-- Add instructor field to existing view -->
        <record model="ir.ui.view" id="partner_instructor_form_view">
            <field name="name">partner.instructor</field>
            <field name="model">res.partner</field>
            <field name="inherit_id" ref="base.view_partner_form"/>
            <field name="arch" type="xml">
                <notebook position="inside">
                    <page string="Sessions">
                        <group>
                            <field name="instructor"/>
                            <field name="student"/>
                        </group>
                    </page>
                </notebook>
            </field>
        </record>

    </data>
</openerp>
```

```
<record model="ir.actions.act_window" id="contact_list_action">
    <field name="name">Contacts</field>
    <field name="res_model">res.partner</field>
    <field name="view_mode">tree,form</field>
</record>
<menuitem id="configuration_menu" name="Configuration"
          parent="main_epc_menu"/>
<menuitem id="contact_menu" name="Contacts"
          parent="configuration_menu"
          action="contact_list_action"/>
```

Traditional (_name != _inherit)
-------------------------------

Add a depency with mail

_inherit activity and specset from mail.thread

Adapt form views

Track changes on ens_start and ens_end

```
# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Activity(models.Model):
    _name = 'epc.activity'
    _inherit = 'mail.thread'
    _description = "activity"
    
    name = fields.Char()
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    ens_start = fields.Integer(track_visibility=True)
    ens_end = fields.Integer(track_visibility=True)
    description = fields.Text()
    specset_ids = fields.One2many('epc.specset', 'activity_id', string="Cahiers de charge")
    activityinfo_ids = fields.One2many('epc.activityinfo', 'activity_id', string="Infos")
```

Delegation inheritance
----------------------

Create an ActivityInfo whinch _inherits from Activity and _inherit from mail.thread

add complete_name, validity, sigle, cnum and subdivision fields
add a selection field activity_type

```
from openerp import models, fields, api

class ActivityInfo(models.Model):
    _name = 'epc.activityinfo'
    _inherit = 'mail.thread'
    _inherits = [['epc.activity','activity_id'],]
    _description = "Activity Info"
    
    complete_name = fields.Char('Complete name')
    validity = fields.Integer('Validity')
    sigle = fields.Char('Sigle', required=True)
    cnum = fields.Integer('CNum', required=True)
    subdivision = fields.Char('Subdivision')
    activity_type = fields.Selection([('COURS', 'Cours'), ('PARTIM', 'Partim'), ('THESE', 'Thèse'), ('CLASSE', 'Classe')])
```

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <!-- Search -->
        <record model="ir.ui.view" id="activity_search_view">
            <field name="name">activity.search</field>
            <field name="model">epc.activity</field>
            <field name="arch" type="xml">
                <search>
                    <field name="name"/>
                    <field name="description"/>
                    <field name="ens_start"/>
                    <field name="ens_end"/>
                </search>
            </field>
        </record>
        
        <!-- Form -->
        <record model="ir.ui.view" id="activity_form_view">
            <field name="name">activity.form</field>
            <field name="model">epc.activity</field>
            <field eval="16" name="priority"/>
            <field name="arch" type="xml">
                <form string="Activity Form">
                    <sheet>
                        <group>
                            <field name="name"/>
                        </group>
                        <notebook>
                            <page string="Schedule">
                                <group col="4">
                                    <field name="ens_start"/>
                                    <field name="ens_end"/>
                                    <field name="responsible_id"/>
                                </group>
                            </page>
                            <page string="Description">
                                <field name="description"/>
                            </page>
                            <page string="Specset" name="specset">
                                <field name="specset_ids">
                                    <tree>
                                        <field name="validity"/>
                                        <field name="language"/>
                                    </tree>
                                </field>
                            </page>
                            
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids" widget="mail_followers"/>
                        <field name="message_ids" widget="mail_thread"/>
                    </div>
                </form>
            </field>
        </record>
        
        <record model="ir.ui.view" id="activity_form_view_inherit">
            <field name="name">activity.form.infos</field>
            <field name="model">epc.activity</field>
            <field eval="8" name="priority"/>
            <field name="mode">primary</field>
            <field name="inherit_id" ref="epc.activity_form_view"/>
            <field name="arch" type="xml">
                <xpath expr="//page[@name='specset']" position="after">
                    <page string="Infos">
                        <field name="activityinfo_ids"/>
                    </page>
                </xpath>
            </field>
        </record>
        
    </data>
</openerp>
```

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <!-- Form -->
        <record model="ir.ui.view" id="activityinfo_form_primherit_view">
            <field name="name">activityinfo.form</field>
            <field name="model">epc.activityinfo</field>
            <field name="mode">primary</field>
            <field eval="16" name="priority"/>
            <field name="inherit_id" ref="epc.activity_form_view"/>
            <field name="arch" type="xml">
                <form position="attributes">
                    <attribute name="string">Activity Info</attribute>
                </form>
                <xpath expr="//field[@name='name']" position="after">
                    <field name="complete_name"/>
                </xpath>
                <xpath expr="//field[@name='responsible_id']" position="after">
                    <field name="validity"/>
                    <field name="sigle"/>
                    <field name="cnum"/>
                    <field name="subdivision"/>
                    <field name="activity_type"/>
                </xpath>
            </field>
        </record>
        
        <record model="ir.ui.view" id="activityinfo_form_view">
            <field name="name">activityinfostandalone.form</field>
            <field name="model">epc.activityinfo</field>
            <field eval="8" name="priority"/>
            <field name="inherit_id" eval="False"/>
            <field name="arch" type="xml">
                <form string="Activity Form">
                    <sheet>
                        <group>
                            <field name="complete_name"/>
                        </group>
                        <notebook>
                            <page string="Details">
                                <group col="4">
                                    <field name="validity"/>
                                    <field name="sigle"/>
                                    <field name="cnum"/>
                                    <field name="subdivision"/>
                                    <field name="activity_type"/>
                                </group>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>
        
        <!-- Tree -->
        <record model="ir.ui.view" id="epc_view_activityinfo_tree">
            <field name="name">epc.view.activityinfo_tree</field>
            <field name="model">epc.activityinfo</field>
            <field name="priority" eval="16"/>
            <field name="arch" type="xml">
                <tree string="activityinfo">
                    <field name="name"/>
                    <field name="complete_name"/>
                    <field name="activity_id"/>
                    <field name="validity"/>
                    <field name="sigle"/>
                    <field name="cnum"/>
                    <field name="subdivision"/>
                    <field name="activity_type"/>
                </tree>
            </field>
        </record>
        
    </data>
</openerp>
```

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <!-- window action -->
        <record model="ir.actions.act_window" id="activity_list_action">
            <field name="name">Activities</field>
            <field name="res_model">epc.activity</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="oe_view_nocontent_create">Create the first course
                </p>
            </field>
        </record>
        <record model="ir.actions.act_window" id="activityinfo_list_action">
            <field name="name">Activity infos</field>
            <field name="res_model">epc.activityinfo</field>
            <field name="view_type">form</field>
            <field name="view_mode">tree,form</field>
            <field name="view_id" eval="False"/>
            <field name="help" type="html">
                <p class="oe_view_nocontent_create">Create the first info
                </p>
            </field>    
        </record>
        <record model="ir.actions.act_window.view" id="activityinfo_list_action_tree">
            <field name="view_mode">tree</field>
            <field name="view_id" ref="epc_view_activityinfo_tree"/>
            <field name="act_window_id" ref="activityinfo_list_action"/>
        </record>
        <record model="ir.actions.act_window.view" id="activityinfo_list_action_form">
            <field name="view_mode">form</field>
            <field name="view_id" ref="activityinfo_form_primherit_view"/>
            <field name="act_window_id" ref="activityinfo_list_action"/>
        </record>
        
      <record model="ir.actions.act_window" id="contact_list_action">
          <field name="name">Contacts</field>
          <field name="res_model">res.partner</field>
          <field name="view_mode">tree,form</field>
      </record>

        <menuitem id="main_epc_menu" name="EPC"/>
        <menuitem id="epc_menu" name="Activities"
                  parent="main_epc_menu"/>
        <menuitem id="activitys_menu" name="Activities" parent="epc_menu"
                  action="activity_list_action" sequence="1"/>
        <menuitem id="activityinfos_menu" name="Infos" parent="epc_menu"
                  action="activityinfo_list_action" sequence="2"/>
                  
      <menuitem id="configuration_menu" name="Configuration"
                parent="main_epc_menu"/>
      <menuitem id="contact_menu" name="Contacts"
                parent="configuration_menu"
                action="contact_list_action"/>
    </data>
</openerp>
```

Domain in menus
===============

- Only display students and instructors in the contact menu

```
<record model="ir.actions.act_window" id="contact_list_action">
    <field name="name">Contacts</field>
    <field name="res_model">res.partner</field>
    <field name="view_mode">tree,form</field>
    <field name="domain">['|', ('instructor', '=', True), ('student', '=', True)]</field>
    <field name="context" eval="{ 'default_instructor': 1, 
                                   'default_student': 1 }" />
</record>
```

Many2many
=========

- add a many2many student_ids from activityinfo to res.partner 
- ensure to be able to list activityinfos from student

```
from openerp import models, fields, api

class ActivityInfo(models.Model):
    _name = 'epc.activityinfo'
    _inherit = 'mail.thread'
    _inherits = [['epc.activity','activity_id'],]
    _description = "Activity Info"
    
    complete_name = fields.Char('Complete name')
    validity = fields.Integer('Validity')
    sigle = fields.Char('Sigle', required=True)
    cnum = fields.Integer('CNum', required=True)
    subdivision = fields.Char('Subdivision')
    activity_type = fields.Selection([('COURS', 'Cours'), ('PARTIM', 'Partim'), ('THESE', 'Thèse'), ('CLASSE', 'Classe')])
    student_ids = fields.Many2many('res.partner', domain="[('student', '=', 1)]", relation='epc_student_activityinfo', column1='activity_id', column2='student_id')
```

```
<!-- Form -->
<record model="ir.ui.view" id="activityinfo_form_primherit_view">
    <field name="name">activityinfo.form</field>
    <field name="model">epc.activityinfo</field>
    <field name="mode">primary</field>
    <field eval="16" name="priority"/>
    <field name="inherit_id" ref="epc.activity_form_view"/>
    <field name="arch" type="xml">
        <form position="attributes">
            <attribute name="string">Activity Info</attribute>
        </form>
        <xpath expr="//field[@name='name']" position="after">
            <field name="complete_name"/>
        </xpath>
        <xpath expr="//field[@name='responsible_id']" position="after">
            <field name="validity"/>
            <field name="sigle"/>
            <field name="cnum"/>
            <field name="subdivision"/>
            <field name="activity_type"/>
        </xpath>
        <xpath expr="//page[@name='specset']" position="after">
            <page string="Students">
                <group col="1">
                    <field name="student_ids" nolabel="1"/>
                </group>
            </page>
        </xpath>
    </field>
</record>

<record model="ir.ui.view" id="activityinfo_form_view">
    <field name="name">activityinfostandalone.form</field>
    <field name="model">epc.activityinfo</field>
    <field eval="8" name="priority"/>
    <field name="inherit_id" eval="False"/>
    <field name="arch" type="xml">
        <form string="Activity Form">
            <sheet>
                <group>
                    <field name="complete_name"/>
                </group>
                <group col="4">
                    <field name="code"/>
                    <field name="site"/>
                </group>
                <notebook>
                    <page string="Details">
                        <group col="4">
                            <field name="validity"/>
                            <field name="sigle"/>
                            <field name="cnum"/>
                            <field name="subdivision"/>
                            <field name="activity_type"/>
                        </group>
                    </page>
                    <page string="Students">
                        <group col="1">
                            <field name="student_ids" nolabel="1"/>
                        </group>
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
```


Computed fields
===============

Ajouter code et site sur base de sigle, cnum et subdivision

```
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
    
    @api.one
    @api.depends('sigle', 'cnum', 'subdivision')
    def _compute_code(self):
        self.code = "%s%s%s" % (self.sigle, self.cnum, self.subdivision if self.subdivision else "")
            
    @api.one
    @api.depends('sigle')
    def _compute_site(self):
        self.site = self.sigle[0] if self.sigle else ""
```

Default values
--------------

- Add an active field on Activity
- default value = True

```
# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Activity(models.Model):
    _name = 'epc.activity'
    _inherit = 'mail.thread'
    _description = "activity"
    
    name = fields.Char()
    responsible_id = fields.Many2one('res.partner', string='Responsible')
    ens_start = fields.Integer(track_visibility=True)
    ens_end = fields.Integer(track_visibility=True)
    description = fields.Text()
    specset_ids = fields.One2many('epc.specset', 'activity_id', string="Cahiers de charge")
    activityinfo_ids = fields.One2many('epc.activityinfo', 'activity_id', string="Infos")
    active = fields.Boolean(default=True)
```

- check impact of active False on activity on the related activityinfo

OnChange
========

- create class entity hierarchical
- add m2o entity and entity_attrib in activity
- add related o2m
- set entity_attrib=entity when entity is set, but user can change value of attributed

```
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
```

```
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
```

```
<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data>
        <!-- Form -->
        <record model="ir.ui.view" id="epc_entity_form">
            <field name="name">epc.view.entityform</field>
            <field name="model">epc.entity</field>
            <field name="priority" eval="16"/>
            <field name="arch" type="xml">
                <form string="UCL Entity form">
                    <sheet>
                        <group colspan="4">
                            <field name="name"/>
                            <field name="parent_id" attrs="{'required': [('name', '!=', 'UCL')], 'invisible': [('name', '=', 'UCL')]}"/>
                        </group>
                        <group col="4">
                            <field name="validity_start"/>
                            <field name="validity_end"/>
                        </group>
                        <notebook>
                            <page string="Activities">
                                <field name="activites_charge_ids"/>
                            </page>
                            <page string="Attributed activities">
                                <field name="activites_attrib_ids"/>
                            </page>
                            
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids" widget="mail_followers"/>
                        <field name="message_ids" widget="mail_thread"/>
                    </div>
                </form>
            </field>
        </record>
        
        <!-- List -->
        <record model="ir.ui.view" id="epc_view_entity_tree">
            <field name="name">epc.view.entity_tree</field>
            <field name="model">epc.entity</field>
            <field name="priority" eval="16"/>
            <field name="arch" type="xml">
                <tree string="Entities list">
                    <field name="name"/>
                    <field name="validity_start"/>
                    <field name="validity_end"/>
                </tree>
            </field>
        </record>
        
    </data>
</openerp>
```

```
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
    
    @api.onchange('entity_id')
    def _check_entity_attrib_id(self):
        if self.entity_id:
            self.entity_attrib_id=self.entity_id
```

Constraints
===========

- Add an sql contraint on specset to ensure the unicity of activity/lang combination
- Add for vol1 and vol2, a total, q1, q2 and coeff field in ActivityInfo (8 fields)
- add a python contraints to ensure that if q1 and q2 are set, they are equal to total
- restrict deletion of entities when attributed

```
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

```

```
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
    vol1_total = fields.Float(default=0)
    vol1_q1 = fields.Float(default=0)
    vol1_q2 = fields.Float(default=0)
    vol1_coeff = fields.Integer(default=0)
    vol2_total = fields.Float(default=0)
    vol2_q1 = fields.Float(default=0)
    vol2_q2 = fields.Float(default=0)
    vol2_coeff = fields.Integer(default=0)
    
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

```

Duplicate
---------
Since we added a constraint on the specset, it's not possible to use the duplicate anymore. Re-implement your own "copy" method which allows to duplicate the SpecSet object, changing the original lang into "[original name] (#)".

```
@api.multi
def copy(self, default=None):
    default = dict(default or {})

    copied_count = self.search_count(
        [('language', '=like', u"{}%".format(self.language))])
    if not copied_count:
        new_language = u"{} (1)".format(self.language)
    else:
        new_language = u"{} ({})".format(self.language, copied_count)

    default['language'] = new_language
    return super(SpecSet, self).copy(default)
```

attrs
=====

It's possible to set fields as invisible, required, readonly, ... conditionnaly using attrs on fields.

- set fields activityinfo_ids invisible when partner is not a student:

```
<separator string="Activities" attrs="{'invisible': [('student', '=', False)]}"/>
<group col="1">
    <field name="activityinfo_ids" nolabel="1"  attrs="{'invisible': [('student', '=', False)]}"/>
</group>
```

Add a new tad in activityinfo only visible when it's a thesis, with a date_start and date_end, and allow 600 days to the student for his thesis

```
@api.onchange('date_start', 'date_end')
def _verify_dates(self):
    if self.date_start and not self.date_end:
        self.date_end = fields.Datetime.to_string(fields.Datetime.from_string(self.date_start) + datetime.timedelta(days=600))
    if self.date_start and self.date_end and self.date_end < self.date_start:
        return {
            'warning': {
                'title': "Incorrect dates",
                'message': "Finish date must be greater or equal to begin date",
            },
        }
```

- using options, disallow creation/open of form of entity from activityinfo

```
<field name="entity_id" options="{'no_create': True, 'no_open': True}"/>
```

Views
=====

Tree
----

- set color on infos, red for THESE and blue for COURS

```
<record model="ir.ui.view" id="epc_view_activityinfo_tree">
    <field name="name">epc.view.activityinfo_tree</field>
    <field name="model">epc.activityinfo</field>
    <field name="priority" eval="16"/>
    <field name="arch" type="xml">
        <tree string="activityinfo" colors="blue:activity_type=='COURS';red:activity_type=='THESE'">
            <field name="name"/>
            <field name="complete_name"/>
            <field name="activity_id"/>
            <field name="validity"/>
            <field name="sigle"/>
            <field name="cnum"/>
            <field name="subdivision"/>
            <field name="activity_type"/>
        </tree>
    </field>
</record>
```

Calendar
--------

- create a calendar view for infos based on thesis dates
```
<record model="ir.ui.view" id="epc_view_activityinfo_calendar">
    <field name="name">epc.activityinfo.calendar</field>
    <field name="model">epc.activityinfo</field>
    <field name="arch" type="xml">
        <calendar string="Activity infos Calendar" date_start="date_start"
                  date_stop="date_end"
                  color="site">
            <field name="name"/>
        </calendar>
    </field>
</record>
```

Gantt
-----

```
<record model="ir.ui.view" id="epc_view_activityinfo_gantt">
    <field name="name">epc.activityinfo.gantt</field>
    <field name="model">epc.activityinfo</field>
    <field name="arch" type="xml">
        <gantt string="Activities Gantt" color="subdivision"
               date_start="date_start" date_end="date_end"
               default_group_by='site'>
            <field name="complete_name"/>
        </gantt>
    </field>
</record>
```

Graph
-----

- Add the number of attendees as a stored computed field
- Then add the relevant view

```
students_count = fields.Integer(
    string="students count", compute='_get_students_count', store=True)
    
@api.depends('student_ids')
def _get_students_count(self):
    for r in self:
        r.students_count = len(r.student_ids)
```

```
<record model="ir.ui.view" id="epc_view_activityinfo_graph">
    <field name="name">epc.activityinfo.graph</field>
    <field name="model">epc.activityinfo</field>
    <field name="arch" type="xml">
        <graph string="Participations by Courses">
            <field name="activity_id"/>
            <field name="students_count" type="measure"/>
        </graph>

    </field>
</record>
```

Kanban
------

- Add an integer color field to the Activityinfo model
- Add the kanban view and update the action

```
<record model="ir.ui.view" id="epc_view_activityinfo_kanban">
    <field name="name">epc.activityinfo.kanban</field>
    <field name="model">epc.activityinfo</field>
    <field name="arch" type="xml">
        <kanban default_group_by="activity_id">
            <field name="color"/>
            <templates>
                <t t-name="kanban-box">
                    <div
                            t-attf-class="oe_kanban_color_{{kanban_getcolor(record.color.raw_value)}}
                                          oe_kanban_global_click_edit oe_semantic_html_override
                                          oe_kanban_card {{record.group_fancy==1 ? 'oe_kanban_card_fancy' : ''}}">
                        <div class="oe_dropdown_kanban">
                            <!-- dropdown menu -->
                            <div class="oe_dropdown_toggle">
                                <span class="oe_e">#</span>
                                <ul class="oe_dropdown_menu">
                                    <li>
                                        <a type="delete">Delete</a>
                                    </li>
                                    <li>
                                        <ul class="oe_kanban_colorpicker"
                                            data-field="color"/>
                                    </li>
                                </ul>
                            </div>
                            <div class="oe_clear"></div>
                        </div>
                        <div t-attf-class="oe_kanban_content">
                            <!-- title -->
                            Session name:
                            <field name="complete_name"/>
                            <br/>
                            Start date:
                            <field name="date_start"/>
                            <br/>
                            End date:
                            <field name="date_end"/>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

Workflows
=========

Define a state, of type selection, to define:
- ('draft', "Draft")
- ('in_progress', "In progress")
- ('give_result', "Give results")
- ('to_be_signed', "Results to be signed")
- ('done', "Done")

```
state = fields.Selection([
    ('draft', "Draft"),
    ('in_progress', "In progress"),
    ('give_result', "Give results"),
    ('to_be_signed', "Results to be signed"),
    ('done', "Done"),
], default='draft')
```

```
<record model="ir.ui.view" id="activityinfo_form_primherit_view">
    <field name="name">activityinfo.form</field>
    <field name="model">epc.activityinfo</field>
    <field name="mode">primary</field>
    <field eval="16" name="priority"/>
    <field name="inherit_id" ref="epc.activity_form_view"/>
    <field name="arch" type="xml">
        <form position="inside">
            <attribute name="string">Activity Info</attribute>
        </form>
        <xpath expr="//sheet" position="before">
            <header>
                <button name="action_draft" type="object"
                        string="Reset to draft"
                        states="in_progress,give_result"/>
                <button name="action_in_progress" type="object"
                        string="Confirm" states="draft"
                        class="oe_highlight"/>
                <button name="action_give_result" type="object"
                        string="Need results" states="in_progress"
                        class="oe_highlight"/>
                <button name="action_to_be_signed" type="object"
                        string="To be signed" states="give_result"
                        class="oe_highlight"/>
                <button name="action_done" type="object"
                        string="Mark as done" states="to_be_signed"
                        class="oe_highlight"/>
                <field name="state" widget="statusbar"/>
            </header>
        </xpath>
```

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <record model="workflow" id="wkf_activityinfo">
            <field name="name">EPC Activity info workflow</field>
            <field name="osv">epc.activityinfo</field>
            <field name="on_create">True</field>
        </record>

        <record model="workflow.activity" id="draft">
            <field name="name">Draft</field>
            <field name="wkf_id" ref="wkf_activityinfo"/>
            <field name="flow_start" eval="True"/>
            <field name="kind">function</field>
            <field name="action">action_draft()</field>
        </record>
        <record model="workflow.activity" id="in_progress">
            <field name="name">In progress</field>
            <field name="wkf_id" ref="wkf_activityinfo"/>
            <field name="kind">function</field>
            <field name="action">action_in_progress()</field>
        </record>
        <record model="workflow.activity" id="give_result">
            <field name="name">Give results</field>
            <field name="wkf_id" ref="wkf_activityinfo"/>
            <field name="kind">function</field>
            <field name="action">action_give_result()</field>
        </record>
        <record model="workflow.activity" id="to_be_signed">
            <field name="name">To be signed</field>
            <field name="wkf_id" ref="wkf_activityinfo"/>
            <field name="kind">function</field>
            <field name="action">action_to_be_signed()</field>
        </record>
        <record model="workflow.activity" id="done">
            <field name="name">Done</field>
            <field name="wkf_id" ref="wkf_activityinfo"/>
            <field name="kind">function</field>
            <field name="action">action_done()</field>
        </record>
        
        <record model="workflow.transition" id="activityinfo_draft_to_in_progress">
            <field name="act_from" ref="draft"/>
            <field name="act_to" ref="in_progress"/>
            <field name="signal">in_progress</field>
        </record>
        <record model="workflow.transition" id="activityinfo_in_progress_to_give_result">
            <field name="act_from" ref="in_progress"/>
            <field name="act_to" ref="give_result"/>
            <field name="signal">give_result</field>
        </record>
        <record model="workflow.transition" id="activityinfo_in_progress_to_draft">
            <field name="act_from" ref="in_progress"/>
            <field name="act_to" ref="draft"/>
            <field name="signal">draft</field>
        </record>
        <record model="workflow.transition" id="activityinfo_give_result_to_draft">
            <field name="act_from" ref="give_result"/>
            <field name="act_to" ref="draft"/>
            <field name="signal">draft</field>
        </record>
        <record model="workflow.transition" id="activityinfo_give_result_to_to_be_signed">
            <field name="act_from" ref="give_result"/>
            <field name="act_to" ref="to_be_signed"/>
            <field name="signal">to_be_signed</field>
        </record>
        <record model="workflow.transition" id="activityinfo_to_be_signed_to_give_result">
            <field name="act_from" ref="to_be_signed"/>
            <field name="act_to" ref="give_result"/>
            <field name="signal">give_result</field>
        </record>
        <record model="workflow.transition" id="activityinfo_to_be_signed_to_done">
            <field name="act_from" ref="to_be_signed"/>
            <field name="act_to" ref="done"/>
            <field name="signal">done</field>
        </record>
        
    </data>
</openerp>
```

Wizards
=======

- create a new wizard to add points to students
- save points in the activityinfo with a new model activityinforesults

```
result_ids = fields.One2many('epc.activityinfo.result', 'activityinfo_id', string="Results")

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
        
class ActivityInfoResults(models.Model):
    _name = 'epc.activityinfo.result'
    
    activityinfo_id = fields.Many2one('epc.activityinfo', string='Activity info')
    student_id = fields.Many2one('res.partner', string='Student', required=True)
    result = fields.Float('Result')
```

```
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
```

```
<?xml version="1.0" encoding="UTF-8"?>
<openerp>
    <data>
        <record model="ir.ui.view" id="resultswizard_form_view">
            <field name="name">epc.wizard.result.form</field>
            <field name="model">epc.wizard.result</field>
            <field name="arch" type="xml">
                <form string="New results">
                    <group col="1">
                        <field name="activityinfo_id" readonly="1" nolabel="1"/>
                        <field name="line_ids" nolabel="1">
                            <tree editable="bottom">
                                <field name="student_id" readonly="1"/>
                                <field name="result"/>
                            </tree>
                        </field>
                    </group>
                    <footer>
                        <button name="validate_results" type="object"
                                string="Validate" class="oe_highlight"/>
                        or
                        <button special="cancel" string="Cancel"/>
                    </footer>
                </form>
            </field>
        </record>
    </data>
</openerp>
```

```
<button name="wizard_encode_results" type="object"
    string="Encode results" states="give_result"/>
    
<page string="Results" states="to_be_signed,done">
    <group col="1">
        <field name="result_ids" nolabel="1">
            <tree>
                <field name="student_id"/>
                <field name="result"/>
            </tree>
        </field>
    </group>
</page>    
```

Smart buttons
=============

- use smart buttons to display various infos of a student to the user

```
<xpath expr="//div[@name='buttons']" position="inside">
    <button class="oe_inline oe_stat_button" type="object" name="courses_list" icon="fa-hospital-o">
        <field name="courses_count" string="Skills" widget="statinfo"/>
    </button>
    <button class="oe_stat_button oe_inline" type="object" name="courses_list">
        <field name="courses_prc" string="Skills" widget="percentpie"/>
    </button>
    <button class="oe_stat_button oe_inline" type="object" name="courses_list">
        <field name="courses_daily" string="Skills" widget="barchart"/>
    </button>
</xpath> 
```

```
courses_count = fields.Integer('N° of courses', compute='_get_nbr_courses')
courses_prc = fields.Integer('Percentage of courses', compute='_get_prc_courses')
courses_daily = fields.Char('Skills', compute='_get_courses_daily')

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
```
        
Models With init False
======================

```
# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _, tools

class SessionAnalysis(models.Model):
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
```

NEEDACTION
==========
- _inherit = ['ir.needaction_mixin']
- def _needaction_domain_get(self, cr, uid, context=None):
- you have the list of the courses where results needs to be signed, encoded, ...

```
class ActivityInfo(models.Model):
    _name = 'epc.activityinfo'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    
    [...]
    
    @api.model
    def _needaction_domain_get(self):
        return [('state', '=', 'give_result')]
```
