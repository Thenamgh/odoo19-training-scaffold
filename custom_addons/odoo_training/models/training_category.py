from odoo import fields, models


class TrainingCategory(models.Model):
    """Model danh mục để minh họa quan hệ One2many/Many2one."""

    _name = "training.category"
    _description = "Danh mục thực hành"
    _order = "name, id"

    name = fields.Char(string="Tên danh mục", required=True)
    active = fields.Boolean(string="Đang sử dụng", default=True)
    item_ids = fields.One2many(
        comodel_name="training.item",
        inverse_name="category_id",
        string="Hồ sơ thực hành",
    )
