
def querySql(table_name, query_field = "*", where_field = None, operator_list = "OR", where_func = " LIKE ", limit = "", order_by = "", count = "SQL_CALC_FOUND_ROWS ", join_sql = ""):
    """
    :param table:
    :param query_field:   * or [field1, field2, field3]
    :param where_field:  None or [field1, field2, field3]
    :param operator_list:    where条件  OR\AND
    :return: 查询结果
    """
    query_field = ",".join(query_field)
    sql = "SELECT {}{} FROM {}".format(count, query_field, table_name)

    where_sql = ""
    if isinstance(where_field, (list, tuple, )):
        where_sql = " WHERE "
        if operator_list in ("OR", "AND", "or", "and"):
            operator_list = [operator_list] * (len(where_field) - 1)
        for index,value in enumerate(where_field):
            where_sql += (value + where_func + "%s")
            if len(where_field) - 1 == index:
                pass
            else:
                where_sql += " {} ".format(operator_list[index])
    return sql + join_sql + where_sql + order_by + limit + ";"


def updateSql(table_name, query_field, where_field):
    sql = "UPTATE {} SET ".format(table_name) + "=%s,".join(query_field) + "=%s"
    where_sql = ""
    if isinstance(where_field, (list, tuple,)):
        where_sql = " WHERE "
        for index,value in enumerate(where_field):
            where_sql += (value + "=%s")
            if len(where_field) - 1 == index:
                pass
                where_sql += ";"
            else:
                where_sql += " {} ".format("AND")
    return sql + where_sql


if __name__ == '__main__':
    sql = querySql("table", query_field=["field1", "field2", "field3"],where_field=("field1", "field2",), operator_list="OR", limit=" LIMIT 1,10", where_func = "=", count = "")
    print(sql)