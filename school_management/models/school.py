# -*- coding: utf-8 -*-

from odoo import models, fields

class SchoolDetails(models.Model):

    _name = "school.details"
    _description = "School Management"

    name = fields.Char(String="name")

