Agent server is a FastAPI Uvicorn server. It is fully async. 

It passes most of the command line arguments through to Uvicorn. 

It does not allow the following command line params:

_DISALLOWED = {
"--reload",
"--reload-dir",
"--reload-include",
"--reload-exclude",
"--reload-delay",
"--factory",
"--workers"
}

It enforces a single worker. (Disallows workers)

By default, it exposes:

UI: http://127.0.0.1:9020

Openapi: http://127.0.0.1:9020/openapi.json
Swagger UI: http://127.0.0.1:9020/docs
Redoc: http://127.0.0.1:9020/redoc

All the above links can be configured from the GUI under operations/agent server. You can also create multiple configurations there and start multiple agent servers with different configurations. The configuration name has to be added to the end of the license as /<config_name>. Without this suffix, the agent server uses the "default" configuration. 

You are free to containarize the agent server and run it load balanced. It is stateless and so there is nothing else to do. See docs on configs on how they keep in sync. 

We do not have an explicit limit on the number of servers you run at this time. 

