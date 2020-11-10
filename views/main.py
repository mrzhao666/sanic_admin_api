from sanic import Sanic
from sanic.response import json as JsonResponse
from sanicdb import SanicDB
from sanic_cors import CORS

from config import MYSQL_CONFIG
from views.table import table_bp
from views.tables import tables_bp

from sanic.exceptions import MethodNotSupported

app = Sanic(__name__, strict_slashes = False)
app.blueprint(table_bp)
app.blueprint(tables_bp)

CORS(app)

#服务启动运行
@app.listener('before_server_start')
async def setup_db(app, loop):
    app.db = SanicDB(host=MYSQL_CONFIG.host, port=MYSQL_CONFIG.port,
             user=MYSQL_CONFIG.user, password=MYSQL_CONFIG.password,database=MYSQL_CONFIG.db, loop = loop, pool_recycle = MYSQL_CONFIG.pool_recycle)
    print("datebase server has started")

#服务器关闭之前
@app.listener('before_server_stop')
async def close_db(app, loop):
    app.db.pool.close()
    await app.db.pool.wait_closed()



@app.exception(MethodNotSupported)
async def handleMethodNot(request, exception):
    return JsonResponse({
        "code":0,
        "msg":str(exception)
    }, status = 405)



@app.middleware('request')
async def verificationLogin(request):
    print("request Interceptor")



@app.route("/", methods = ["GET"])
async def index(request):
    return JsonResponse({
        "table资料" : "table",
        "table2资料": "table2",
    })


if __name__ == '__main__':
    app.run(host = "localhost", port = 80, debug = True)