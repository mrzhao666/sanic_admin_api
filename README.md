```python
#table_field.py
from sanic_admin_api.utils.table_utils import FormatColumns,ForeignKey,CharField
class Player(FormatColumns):
    table_name = "player"
    verbose_name = "web端表名（table）"
    foreign_key_name = "Name_J"
    primary_key= "PlayerID"
    def __init__(self):
        Kind_Choice = {1:"孩子", 2:"青年"}
        self.PlayerID = CharField(is_edit=False, verbose_name = "Id")
        self.Kind = CharField(verbose_name = "类型", choice_field = Kind_Choice)
        self.Name_J = CharField(verbose_name = "中文名")
        self.Name_E = CharField(verbose_name = "英文名")


class Table2(FormatColumns):
    verbose_name = "web端表名（table2）"
    table_name = "table2"
    primary_key = "id"
    def __init__(self):
        self.id = CharField(is_edit=False, verbose_name = "Id")
        self.fromTableId = ForeignKey(self, Table, key_name = "fromTableName", verbose_name = "PlayerID", key_verbose = "1姓名", as_table_name = "fromTable")
        self.toTableId = ForeignKey(self, Table, key_name="toTableName", verbose_name="Id", key_verbose="2姓名", as_table_name = "toTable")



```



```python
#create views player
#views/player.py

from sanic import Blueprint
from sanic_admin_api.views.public_view import PublicList,ObjView
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



