from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestTraining(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.learner = new_test_user(
            cls.env,
            login="com04_learner",
            groups="base.group_user,odoo_training.group_training_user",
        )
        cls.outsider = new_test_user(
            cls.env, login="com04_outsider", groups="base.group_user",
        )
        cls.category = cls.env["training.category"].with_user(cls.learner).create(
            {"name": "Danh mục kiểm thử"}
        )

    def test_crud_and_relation(self):
        """Người có quyền tạo, đọc, sửa, xóa và truy cập quan hệ."""
        Item = self.env["training.item"].with_user(self.learner)
        item = Item.create({"name": "Hồ sơ A", "category_id": self.category.id})
        self.assertEqual(item.category_id, self.category)
        self.assertIn(item, self.category.item_ids)
        self.assertEqual(item.read(["name"])[0]["name"], "Hồ sơ A")
        item.write({"name": "Hồ sơ B"})
        self.assertEqual(item.name, "Hồ sơ B")
        item.unlink()
        self.assertFalse(item.exists())

    def test_archive(self):
        Item = self.env["training.item"].with_user(self.learner)
        item = Item.create({"name": "Lưu trữ", "category_id": self.category.id})
        item.write({"active": False})
        self.assertFalse(Item.search([("id", "=", item.id)]))
        self.assertTrue(Item.with_context(active_test=False).search([("id", "=", item.id)]))

    def test_internal_user_without_group_is_denied(self):
        """Ẩn menu chưa đủ: ORM cũng phải từ chối người thiếu nhóm."""
        item = self.env["training.item"].with_user(self.learner).create(
            {"name": "Không công khai", "category_id": self.category.id}
        )
        for model_name in ("training.category", "training.item"):
            Model = self.env[model_name].with_user(self.outsider)
            with self.assertRaises(AccessError):
                Model.search([])
            with self.assertRaises(AccessError):
                Model.create({"name": "Không có quyền", **(
                    {"category_id": self.category.id} if model_name == "training.item" else {}
                )})
        for record in (self.category, item):
            restricted = record.with_user(self.outsider)
            with self.assertRaises(AccessError):
                restricted.write({"name": "Không có quyền"})
            with self.assertRaises(AccessError):
                restricted.unlink()
