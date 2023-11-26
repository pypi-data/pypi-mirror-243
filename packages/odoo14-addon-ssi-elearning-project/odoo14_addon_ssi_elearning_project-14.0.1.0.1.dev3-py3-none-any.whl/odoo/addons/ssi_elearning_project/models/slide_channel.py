# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class SlideChannel(models.Model):
    _name = "slide.channel"
    _inherit = [
        "slide.channel",
        "mixin.task",
    ]
    _task_create_page = True
    _task_page_xpath = "//page[1]"
    _task_template_position = "after"

    task_ids = fields.Many2many(
        comodel_name="project.task",
        relation="rel_slide_channel_2_task",
        column1="channel_id",
        column2="task_id",
    )
