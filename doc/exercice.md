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

Using view inheritance, display this fields in the partner form view

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

Many2many
=========

- add a many2many student_ids from activityinfo to res.partner 

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
