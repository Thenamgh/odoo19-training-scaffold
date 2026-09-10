from odoo import fields, models


class TrainingItem(models.Model):
    """Model nghiệp vụ tối thiểu; phát triển dần trong các bài học sau."""

    _name = "training.item"
    _description = "Hồ sơ thực hành"
    _order = "id desc"

    name = fields.Char(string="Tên hồ sơ", required=True)
    description = fields.Text(string="Mô tả")
    active = fields.Boolean(string="Đang sử dụng", default=True)
    category_id = fields.Many2one(
        comodel_name="training.category",
        string="Danh mục",
        required=True,
        ondelete="restrict",
        index=True,
    )
