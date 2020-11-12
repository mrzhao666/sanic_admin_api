class FormatColumns:
    table_name = ""
    @property
    def getList(self):
        return_list = []
        for key, value in self.__dict__.items():
            choice_field = None
            if isinstance(value, CharField):
                choice_field = value.choice_field
            return_list.append({"name_e": key, "name_j": value.verbose_name, "is_edit": value.is_edit, "choice_field":choice_field})
        return return_list

    @property
    def query_field(self):
        """
        :return: 返回默认的查询字段
        """
        return_list = []
        for key,value in self.__dict__.items():
            if isinstance(value, ForeignKey):
                return_list.append(value.value)
            return_list.append(self.table_name + "." + key + " AS " + key)

        return return_list

    @property
    def join_sql(self):
        """
        :return: 返回关联查询的sql
        """
        sql = ""
        for key,value in self.__dict__.items():
            if isinstance(value, ForeignKey):
                table = value.obj2.table_name
                where_obe = value.as_table_name + "." + value.obj2.primary_key
                where_two = value.obj1.table_name + "." + key
                sql += " LEFT JOIN {} AS {} ON {}={} ".format(table, value.as_table_name, where_obe, where_two)
        return sql

    def get_choice_and_foreignkey(self):
        choice_field = {}
        foreignkey_field = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ForeignKey):
                foreignkey_field[key] = value
            elif isinstance(value, CharField):
                if isinstance(value.choice_field, dict):
                    choice_field[key] = value
        return choice_field, foreignkey_field

class ForeignKey:
    def __init__(self, obj1, obj2, key_name, verbose_name, key_verbose, as_table_name = None, is_edit = True):
        """

        :param obj1: 主表对象
        :param obj2: 外键
        :param key_name:  返回的字段
        :param verbose_name:  后台中显示的字段
        """
        self.obj1 = obj1
        self.obj2 = obj2
        self.key_name = key_name
        self.verbose_name = verbose_name
        self.key_verbose = key_verbose
        self.as_table_name = self.obj2.table_name if as_table_name is None else as_table_name
        self.is_edit = is_edit
        self.value = "{}.{} AS {}".format(self.as_table_name, self.obj2.foreign_key_name, self.key_name)

class CharField:
    def __init__(self, is_edit = True, verbose_name = None, choice_field = None):
        self.is_edit = is_edit
        self.verbose_name = verbose_name
        self.choice_field = choice_field
