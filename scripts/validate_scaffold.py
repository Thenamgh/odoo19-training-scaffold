"""Kiểm tra tĩnh bộ khung; không thay thế việc cài/test trên Odoo 19."""

import ast
import configparser
import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "custom_addons" / "odoo_training"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def validate():
    counts = {}
    python_files = list(MODULE.rglob("*.py")) + [Path(__file__)]
    models = {}
    for path in python_files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        if path.parent.name == "models" and path.name != "__init__.py":
            for node in tree.body:
                if not isinstance(node, ast.ClassDef):
                    continue
                model_name = None
                field_names = set()
                for stmt in node.body:
                    if not isinstance(stmt, ast.Assign):
                        continue
                    names = [target.id for target in stmt.targets if isinstance(target, ast.Name)]
                    if "_name" in names:
                        model_name = ast.literal_eval(stmt.value)
                    if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Attribute):
                        if isinstance(stmt.value.func.value, ast.Name) and stmt.value.func.value.id == "fields":
                            field_names.update(names)
                if model_name:
                    models[model_name] = field_names
    check(set(models) == {"training.item", "training.category"}, "Thiếu model")
    counts["python_parsed"] = len(python_files)

    manifest = ast.literal_eval((MODULE / "__manifest__.py").read_text(encoding="utf-8"))
    check(manifest["version"].startswith("19.0."), "Version không đúng 19.0")
    check(manifest["depends"] == ["base"], "Phụ thuộc ngoài phạm vi khung")
    check(manifest["installable"] is True, "Module chưa cho phép cài")
    for relative in manifest["data"] + manifest["demo"]:
        check((MODULE / relative).is_file(), f"Manifest trỏ file không tồn tại: {relative}")
    check(manifest["data"].index("security/training_security.xml") <
          manifest["data"].index("security/ir.model.access.csv"), "Sai thứ tự nhóm/ACL")
    check(manifest["data"][-1] == "views/training_menus.xml", "Menu phải nạp sau action")

    ids = set()
    references = []
    xml_paths = list(MODULE.rglob("*.xml"))
    for path in xml_paths:
        tree = ET.parse(path)
        check(tree.getroot().tag == "odoo", f"Sai root XML: {path}")
        for element in tree.iter():
            external_id = element.get("id")
            if external_id:
                check(external_id not in ids, f"XML ID bị trùng: {external_id}")
                ids.add(external_id)
            for attr in ("ref", "parent", "action"):
                if element.get(attr):
                    references.append(element.get(attr))
            check(element.tag != "tree", "Dùng list thay cho tree trong Odoo 19")
            check(not ({"attrs", "states"} & set(element.attrib)), "Có cú pháp view cũ")
        for record in tree.findall(".//record[@model='ir.ui.view']"):
            model = record.find("field[@name='model']").text
            arch = record.find("field[@name='arch']")
            check(model in models, f"View tham chiếu model lạ: {model}")
            # Với One2many lồng list, field name/active có ở cả hai model.
            for field in arch.findall(".//field"):
                check(field.get("name") in models[model],
                      f"Field view không khai báo: {model}.{field.get('name')}")
    for ref in references:
        if "." not in ref:
            check(ref in ids, f"XML ID nội bộ không tồn tại: {ref}")
        elif ref.startswith("odoo_training."):
            check(ref.split(".", 1)[1] in ids, f"XML ID không tồn tại: {ref}")
    counts["xml_parsed"] = len(xml_paths)
    counts["xml_ids_unique"] = len(ids)

    with (MODULE / "security/ir.model.access.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    check(len(rows) == 2, "Cần ACL cho hai model")
    expected = {"model_" + name.replace(".", "_") for name in models}
    check({r["model_id:id"] for r in rows} == expected, "ACL sai model")
    for row in rows:
        check(row["group_id:id"] == "odoo_training.group_training_user", "ACL thiếu nhóm riêng")
        check(row["group_id:id"].split(".", 1)[1] in ids, "Nhóm quyền không tồn tại")
        check(all(row[key] == "1" for key in ("perm_read", "perm_write", "perm_create", "perm_unlink")),
              "ACL không đúng CRUD dự kiến")
    counts["acl_rows"] = len(rows)

    for path in (ROOT / ".vscode").glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    counts["vscode_json"] = len(list((ROOT / ".vscode").glob("*.json")))
    config = configparser.ConfigParser(interpolation=None)
    config.read(ROOT / "config/odoo.conf.example", encoding="utf-8")
    check(config["options"]["db_password"].startswith("CHANGE_ME"), "Không được ghi mật khẩu thật")
    check(config["options"]["http_interface"] == "127.0.0.1", "Chỉ mở cổng local")
    check("custom_addons" in config["options"]["addons_path"], "Thiếu custom_addons")
    for name in ("odoo", "custom_addons", "config", "logs", ".odoo_data"):
        # Các thư mục bị Git bỏ qua có thể chưa tồn tại sau clone; ZIP giữ thư mục trống.
        if name in ("custom_addons", "config"):
            check((ROOT / name).is_dir(), f"Thiếu thư mục {name}")
    for name in ("__init__.py", "models/__init__.py", "tests/__init__.py"):
        check((MODULE / name).is_file(), f"Thiếu {name}")
    for key, value in counts.items():
        print(f"PASS {key}: {value}")
    print("PASS manifest, XML references, ACL, config and folder structure")
    print("NOT RUN: Odoo install/upgrade, ORM tests and web UI")


if __name__ == "__main__":
    validate()
