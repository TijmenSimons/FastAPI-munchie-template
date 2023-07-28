# Problem Tracing Protocols

Obscure problems we encountered and solved.

Usually these are stupid mistakes.

### Terminal not showing any updates

Check if there multiple terminals open, whoops.

Check if the server is not halted and/or crashed by the websocket. (Is there a message about websocket error or connection in the last few logs?)

### Websocket not responding

Check if you `returned` instead of `continued` in the loop.

### Websocket test giving unexpected error

This one is tricky, I think because things are happening at the same time, asynchronously, things are being sent wrong when the websockets are closing.

### Authorization not working

Check permission dependency.

If there was no permission dependency active on said endpoint when you loaded the docs, swagger does not send the authorization header with the request. If you then later do add the permission dependency, swagger does not update the docs live, meaning you just don't send the access_token, resulting in an authorization error. So a refresh of the page easily fixes this problem.

### SQLA `update()` not working

Did you `await session.commit()`?

### Pytest

`AssertionError: assert None` make sure you're not asserting the returns of a function that does not return anything.

### Unable to connect to websocket

Are you connecting to localhost or to the live version?
