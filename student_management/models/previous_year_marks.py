from odoo import fields,models,api


class Previous_Year_Mark(models.Model):
    _name = 'previous.year.mark'
    _description = 'Marks Information'


    subject_id = fields.Many2one('subject.subject','Subject',required=True)
    course_id = fields.Many2one('res.student','Subject',required=True)
    total_marks = fields.Float(string='Total Marks',required=True)
    obtained_marks_exam = fields.Float(string='Exam Marks',required=True)
    obtained_marks_viva = fields.Float(string='Viva Marks',required=True)
    total_obtained_marks = fields.Float(string ='Total Marks',required=True,compute='on_compute_total_marks',store=True)

    @api.depends('obtained_marks_exam','obtained_marks_viva')
    def on_compute_total_marks(self):
        for rec in self:
            rec.total_obtained_marks = rec.obtained_marks_exam + rec.obtained_marks_viva
