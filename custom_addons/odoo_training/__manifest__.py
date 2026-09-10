{
    "name": "Odoo Training - Module khung",
    "version": "19.0.1.0.0",
    "summary": "Bộ khung thực hành dùng chung cho Short Course và HTTTQL",
    "category": "Tools",
    "author": "Nguyễn Thế Nam",
    "license": "LGPL-3",
    "depends": ["base"],
    # Nhóm quyền phải nạp trước ACL; action phải nạp trước menu.
    "data": [
        "security/training_security.xml",
        "security/ir.model.access.csv",
        "views/training_category_views.xml",
        "views/training_item_views.xml",
        "views/training_menus.xml",
    ],
    "demo": ["demo/training_demo.xml"],
    "application": True,
    "installable": True,
    "auto_install": False,
}
