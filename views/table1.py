from sanic import Blueprint

from public_view import ObjList,ObjView
from table_field import Table
table1_bp = Blueprint('table1', url_prefix = "/table1")


class TableList(ObjList):
    table = Table()
    serach_field = ("ID", "Name_J",)

class TableObj(ObjView):
    table = Table()

table1_bp.add_route(TableList.as_view(), "")
table1_bp.add_route(TableObj.as_view(), "/<obj_id>")