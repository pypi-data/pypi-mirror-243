from skywalking import Layer, Component
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import TagMqBroker, TagMqTopic
from rocketmq.client import PushConsumer
link_vector = ['https://github.com/apache/rocketmq-client-python']

support_matrix = {
    'rocketmq-client-python': {
        '>=3.7': ['2.0.0']
    }
}
note = """"""
def install():
    from rocketmq.client import Producer,PushConsumer

    _send_sync = Producer.send_sync
    
    Producer.send_sync = _sw_send_sync_func(_send_sync)
    PushConsumer.subscribe = _sw_subscribe

#发送消息    
def _sw_send_sync_func(_send_sync):
    def wrap(this, message):
        peer = ';'.join(this.config['bootstrap_servers'])
        context = get_context()
        topic = message._as_parameter_
        with context.new_exit_span(op=f'Rocketmq/{topic}/Producer' or '/', peer=peer,
                                   component=Component.General) as span:
            carrier = span.inject()
            span.layer = Layer.MQ

            for item in carrier:
                message.set_property(item.key,item.val.encode('utf-8'))
            res = _send_sync(this, message)
            span.tag(TagMqBroker(peer))
            span.tag(TagMqTopic(topic))
            return res
    return wrap

#订阅消息
def _sw_subscribe(self, topic, callback):
    #回调
    def _callback(msg):
        peer = getattr(self.connection, 'host', '<unavailable>')
        carrier = Carrier()
        for item in carrier:
            val = msg.get_property(item.key)
            if val is not None:
                item.val = val
        with get_context().new_entry_span(op=f'Rocketmq/{topic}/Consumer' or '/', carrier=carrier) as span:
            span.layer = Layer.MQ
            span.component = Component.General
            span.tag(TagMqBroker(peer))
            span.tag(TagMqTopic(topic))
            return callback(msg)
        
    return _subscribe(self, topic=topic,callback=_callback)
_subscribe = PushConsumer.subscribe
            

     

