from sanic import Blueprint
from sanic.response import json as JsonResponse
from sanic.exceptions import NotFound
from utils.public_utils import get_classes
import table_field

table_bp = Blueprint('table', url_prefix = "/table")


@table_bp.route("/")
async def tableList(request):
    class_dic = get_classes(table_field)
    return_list = []
    for key, value in class_dic.items():
        return_list.append({value.verbose_name: key})
    return JsonResponse(return_list)



@table_bp.route("/<func>")
async def objTable(request, func):
    class_dic = get_classes(table_field)
    try:
        table_obj = class_dic.get(func)()
    except TypeError:
        raise NotFound("Requested URL {} not found".format("/table/func"))
    return JsonResponse({
        "table_name":table_obj.verbose_name,
        "columns":table_obj.getList
    })



