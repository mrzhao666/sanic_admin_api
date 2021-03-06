import json
import pymysql
from sanic.response import json as JsonResponse
from sanic.views import HTTPMethodView

from sanic_admin_api.utils.get_sql import querySql,inset_sql
from sanic_admin_api.utils.data_page import DataPage
from sanic_admin_api.utils.public_utils import JsonExtendEncoder
from sanic_admin_api.error_response import ParamsNotFound


class ObjList(HTTPMethodView, DataPage):
    table = object
    serach_field = ()
    max_page_size = 100
    page_size = 50
    page = 1
    def __init__(self):
        DataPage.__init__(self)

    def get_query_sql(self):
        sql = querySql(self.table.table_name, query_field=self.table.query_field, where_field=self.serach_field, operator_list="OR",
                       limit=" Limit {},{}".format((self.page - 1) * self.page_size, self.page_size), join_sql = self.table.join_sql)
        return sql

    def get_keyword(self, request):
        keyword = request.args.get("keyword", [])
        if not keyword:
            self.serach_field = None
        else:
            keyword = ["%" + keyword + "%"] * len(self.serach_field)
        return keyword


    async def get(self, request):
        self.set_page(request)
        keyword = self.get_keyword(request)
        sql = self.get_query_sql()

        db = request.app.db
        if not db.pool:
            await db.init_pool()
        async with db.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, keyword)
                    ret1 = await cur.fetchall()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(sql, keyword)
                    ret1 = await cur.fetchall()
                try:
                    await cur.execute("select found_rows() as count;")
                    ret2 = await cur.fetchone()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute("select found_rows() as count;")
                    ret2 = await cur.fetchone()
        data,count = ret1,ret2.get("count")
        # data,count = (await request.app.db.data_and_count(sql, *keyword))

        choice_field, foreignkey_field = self.table.get_choice_and_foreignkey()
        for obj in data:
            for choice,choice_obj in choice_field.items():
                obj[choice] = choice_obj.choice_field.get(obj[choice])
            for foreignkey,foreignkey_obj in foreignkey_field.items():
                obj[foreignkey] = "{}\n（{}）".format(obj[foreignkey], obj[foreignkey_obj.key_name])
                del obj[foreignkey_obj.key_name]
        data = json.dumps(data, cls = JsonExtendEncoder)

        int_count,float_count = divmod(count, self.page_size)
        if float_count:
            int_count += 1

        return JsonResponse({
            "data_count":count,
            "max_page": int_count,
            "page": self.page,
            "data" : json.loads(data),
        })

    async def post(self, request):
        if not request.form:
            raise ParamsNotFound("param not found")
        form_data = request.form
        sql = inset_sql(self.table.table_name, query_field = form_data.keys())
        await request.app.db.execute(sql, *list(form_data.values()))
        return JsonResponse({"code": 1,
                             "msg": "添加完成",
                             })


class ObjView(HTTPMethodView):
    table = object
    async def get(self, request, obj_id):
        sql = querySql(self.table.table_name, query_field = self.table.query_field,where_field = [self.table.primary_key], where_func = "=", count = "", join_sql = self.table.join_sql)
        result = await request.app.db.get(sql, obj_id)
        result = json.dumps(result, cls=JsonExtendEncoder)
        return JsonResponse(json.loads(result))

    async def put(self, request, obj_id):

        if not request.form:
            raise ParamsNotFound("param not found")
        await request.app.db.table_update(self.table.table_name, updates=request.form, field_where=self.table.primary_key,
                              value_where=obj_id)
        return JsonResponse({"code": 1,
            "msg": "更新成功",
        })

    async def delete(self, request, obj_id):
        sql = "DELETE FROM {} WHERE {}=%s;".format(self.table.table_name, self.table.primary_key)
        await request.app.db.execute( sql, obj_id, )
        return JsonResponse({"code": 1,
            "msg": "成功删除",
        })
