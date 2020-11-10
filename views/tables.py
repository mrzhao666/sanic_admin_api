from sanic import Blueprint
from sanic.response import json as JsonResponse
from table_field import Table, Table2



tables_bp = Blueprint('tables', url_prefix = "/tables")


@tables_bp.route("/")
async def playerTable(request):
    return JsonResponse({
        "table1":"table1",
        "table2":"table2",
    })


@tables_bp.route("/table1")
async def playerTable(request):
    table_obj = Table()
    return JsonResponse({
        "table_name":table_obj.verbose_name,
        "columns":table_obj.getList
    })
@tables_bp.route("/table2")
async def playerTransferTable(request):
    table_obj = Table2()
    return JsonResponse({
        "table_name":table_obj.verbose_name,
        "columns":table_obj.getList
    })

