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





#create views player
#views/player.py

from sanic import Blueprint
from public_view import PublicList,ObjView
from table_field import Player

player_bp = Blueprint('player', url_prefix = "/player")



class PlayerList(PublicList):
    table = Player()
    serach_field = ("PlayerID", "Name_J", "Name_E",)


class PlyerObj(ObjView):
    table = Player()


player_bp.add_route(PlayerList.as_view(), "")
player_bp.add_route(PlyerObj.as_view(), "/<obj_id>")
