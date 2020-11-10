from utils.table_utils import FormatColumns, ForeignKey





class Table(FormatColumns):
    table_name = "table"
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
