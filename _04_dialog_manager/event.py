subscribers = dict()

def subscribe(event, function):
    """
    subscribes function to event
    @param event: name of event
    @param function: function to subscribe
    """
    if not event in subscribers:
        subscribers[event] = []
    subscribers[event].append(function)

def post_event(event, data):
    """
    posts new event
    @param event: name of event
    @param data: data to pass to subscribed function"""
    if not event in subscribers:
        return
    for function in subscribers[event]:
        function(data)
