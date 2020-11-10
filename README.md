```python
#table_field.py
class Player(FormatColumns):
    table_name = "player"
    verbose_name = "web端表名（table）"
    foreign_key_name = "Name_J"
    primary_key= "ID"
    def __init__(self):
        self.ID = "ID"
        self.Name_J = "中文名"
        self.Name_E = "英文名"


class Table2(FormatColumns):
    verbose_name = "web端表名（table2）"
    table_name = "table2"
    primary_key = "id"
    def __init__(self):
        self.id = "id"
        self.fromTableId = ForeignKey(self, Table, key_name = "fromTableName", verbose_name = "Id", key_verbose = "1姓名", as_table_name = "fromTable")
        self.toTableId = ForeignKey(self, Table, key_name="toTableName", verbose_name="Id", key_verbose="2姓名", as_table_name = "toTable")



```



```python
#create views player
#views/player.py

from sanic import Blueprint
from public_view import PublicList,ObjView
from table_field import Player

player_bp = Blueprint('player', url_prefix = "/player")



class PlayerList(PublicList):
    #max_page_size = 50
    table = Player()
    serach_field = ("PlayerID", "Name_J", "Name_E",)


class PlyerObj(ObjView):
    table = Player()


player_bp.add_route(PlayerList.as_view(), "")
player_bp.add_route(PlyerObj.as_view(), "/<obj_id>")
```



```

http://127.0.0.1/player?keyword=Nicholas&page=10&page_size=100


http://127.0.0.1/player/888

GET：从服务器取出资源（一项或多项）。
POST：在服务器新建一个资源。
PUT：在服务器更新资源（客户端提供改变后的完整资源）。
DELETE：从服务器删除资源。

```



```python
#需要为sanicdb.py添加一个方法

    async def data_and_count(self, query, *parameters, **kwparameters):
        """获取查询的数据列表 和 数据表的总数量"""
        if not self.pool:
            await self.init_pool()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, kwparameters or parameters)
                    ret1 = await cur.fetchall()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute(query, kwparameters or parameters)
                    ret1 = await cur.fetchall()
                try:
                    await cur.execute("select found_rows() as count;")
                    ret2 = await cur.fetchone()
                except pymysql.err.InternalError:
                    await conn.ping()
                    await cur.execute("select found_rows() as count;")
                    ret2 = await cur.fetchone()
                return ret1,ret2.get("count")
```

