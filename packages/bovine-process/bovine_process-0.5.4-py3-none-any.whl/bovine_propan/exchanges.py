from faststream.rabbit import RabbitExchange, ExchangeType

processing = RabbitExchange("processing", auto_delete=False, type=ExchangeType.TOPIC)
"""Exchange used for messages being processed.

Relevant routing_key are:

* `inbox`
* `outbox`
"""

processed = RabbitExchange("processed", auto_delete=False, type=ExchangeType.TOPIC)
"""Exchange used for messages having been processed, currently used to feed the EventSources"""
