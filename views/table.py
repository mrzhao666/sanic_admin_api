from sanic import Blueprint

from public_view import PublicList,ObjView
from table_field import Table
table_bp = Blueprint('table', url_prefix = "/table")


class TableList(PublicList):
    table = Table()
    serach_field = ("ID", "Name_J",)

class TableObj(ObjView):
    table = Table()

table_bp.add_route(TableList.as_view(), "")
table_bp.add_route(TableObj.as_view(), "/<obj_id>")