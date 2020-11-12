from sanic import Sanic
from sanic.response import json as JsonResponse
from sanicdb import SanicDB
from sanic_cors import CORS

from config import MYSQL_CONFIG
from views.table1 import table1_bp
from views.tables import table_bp

from error_response import ParamsNotFound

app = Sanic(__name__, strict_slashes = False)
app.blueprint(table1_bp)
app.blueprint(table_bp)

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



@app.exception(ParamsNotFound)
async def paramsNotFound(request, exception):
    return JsonResponse({
        "code":0,
        "msg":str(exception)
    }, status = 400)



@app.middleware('request')
async def verificationLogin(request):
    print("request Interceptor")




if __name__ == '__main__':
    app.run(host = "localhost", port = 80, debug = True)