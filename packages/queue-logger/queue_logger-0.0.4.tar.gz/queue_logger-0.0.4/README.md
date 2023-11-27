Set following Environment variables: \
`QUEUE_HOST=QUEUE_BROKER_HOST` \
`QUEUE_PORT=QUEUE_BROKER_PORT` \
`QUEUE_USER=QUEUE_BROKER_USER` \
`QUEUE_PASS=QUEUE_BROKER_PASS`

```python
import logging
from QLGR import create_logger


logger = create_logger(__name__, logging.NOTSET)
logger.info('This is an informational message.')
logger.error('This is an error message.')
```

Check your message broker (rabbitmq in this case), there must be 2 messages on `logs` queue.
