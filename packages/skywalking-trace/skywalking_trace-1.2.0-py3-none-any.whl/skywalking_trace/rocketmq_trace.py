from skywalking import Layer, Component
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import TagMqTopic
from rocketmq.client import Message
#发送消息    
def send_sync(producer,topic,keys,tags,body):
    message = Message(topic)
    message.set_keys(keys)
    message.set_tags(tags)
    message.set_body(body)

    with get_context().new_exit_span(op=f'Rocketmq/{topic}/Producer' or '/',peer=None,component=Component.General) as span:
        carrier = span.inject()
        carrier.client_address='xxx'
        span.layer = Layer.MQ
        for item in carrier:  
            if item.val is not None :
                message.set_property(item.key,item.val.encode('utf8'))
        res = producer.send_sync(message)
        span.tag(TagMqTopic(topic))
        return res

#订阅消息
def subscribe(pushConsumer, topic, callback):
    #回调
    def _callback(msg):
        carrier = Carrier()
        for item in carrier:
            value = bytes.decode(msg.get_property(item.key))
            item.val = value
        with get_context().new_entry_span(op=f'Rocketmq/{topic}/Consumer' or '/', carrier=carrier) as span:
            span.layer = Layer.MQ
            span.component = Component.General
            span.tag(TagMqTopic(topic))
            return callback(msg)        
    return pushConsumer.subscribe(topic=topic,callback=_callback)

            

     

