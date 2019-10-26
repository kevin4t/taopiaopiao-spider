from flask import Flask, Response
from flask_cors import cross_origin
from flask_apscheduler import APScheduler
import get_data

data = ""


class Config(object):  # 创建配置，用类
    # 任务列表
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:refresh_data',  # 方法名
            'trigger': 'interval',  # interval表示循环任务
            'days': 1,
        }
    ]


def refresh_data():
    global data
    data = get_data.refresh_data()


app = Flask(__name__)
app.config.from_object(Config())  # 为实例化的flask引入配置
refresh_data()

@app.route('/')
@cross_origin()
def hello():
    return Response(data, mimetype='application/json')


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)
