from rocketmq.client import PushConsumer,ConsumeStatus
from skywalking import agent,config 
from rocketmq_trace import subscribe
import time
from trace_log import TraceLog
config.init(agent_collector_backend_services='49.4.88.64:11800', agent_name='mq_consumer_trace')
agent.start()
log = TraceLog()

def callback(msg):
    log.info(msg.body)
    return ConsumeStatus.CONSUME_SUCCESS

consumer = PushConsumer('rocket-produce')
consumer.set_name_server_address('120.195.49.134:9876')
subscribe(consumer,'mq_trace', callback)
consumer.start()

while True:
    time.sleep(3600)
consumer.shutdown()