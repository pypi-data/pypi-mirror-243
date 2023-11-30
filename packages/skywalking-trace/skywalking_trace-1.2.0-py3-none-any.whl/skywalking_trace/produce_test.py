from rocketmq.client import Producer
from skywalking import agent,config
from rocketmq_trace import send_sync
from trace_log import TraceLog
from flask import Flask


config.init(agent_collector_backend_services='49.4.88.64:11800', agent_name='mq_produce_trace')
agent.start()
producer = Producer('rocket-produce')
producer.set_name_server_address('120.195.49.134:9876')
log = TraceLog()

app = Flask(__name__)
@app.route('/')
def index(): 
     producer.start()
     ret = send_sync(producer,'mq_trace','trace_keys','trace_tags','produce hello world')
     log = TraceLog()
     log.info(ret.status)
     producer.shutdown()
     log.info('Hello, Flask!') 
     return 'Hello, Flask!'

app.run()
