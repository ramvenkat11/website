# Getting Started

Search2o is currently in open beta. Anyone interested is welcome to try it.

## Register

<Registration form>. See ./register/

## Download the agent server


pip install search2o


## Running the server

If you are an AI hobbyist or just checking out the product for yourself, just run it from your laptop.

If you expect to invite others to check it out, start it from a common place in your organization - or, you can share your license key with them and they can all start it on their laptops. Since the agent server is stateless, you can do many different things with it. 

One key is that the APIs and/or databases you wish to call from your agents should be accessible from where you start the agent server.

### Setting up the license key

    License key

A Search2o license key is required to run the server.

Provide the key with ONE of these environment variables:

- SEARCH2O_LICENSE_KEY
  The license key itself.
  Example:
  SEARCH2O_LICENSE_KEY=your-license-key

- SEARCH2O_LICENSE_KEY_FILE
  The path to a file containing the license key.
  Example:
  SEARCH2O_LICENSE_KEY_FILE=/path/to/license.txt

Setting both is an error. If neither is set, or the key is empty, the server will exit.


### Set up at least one LLM key

To make LLM calls, you need an API key from one of the three vendors: Google, Openai, Anthropic

Set up at least one of GEMINI_API_KEY, OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables.

Search2o is not limited to these vendors. See docs for more details. 


### Start the server

SEARCH2O_LICENSE_KEY=... ANTHROPIC_API_KEY=... search2o 

### GUI

if you started it on your laptop:
Go to http://127.0.0.1:9020 for the GUI
Login with the same credentials you registered with above in the registration form. 

Other URLs:
Openapi: http://127.0.0.1:9020/openapi.json
Docs: http://127.0.0.1:9020/docs
Redoc: http://127.0.0.1:9020/redoc

You can customize all these from the GUI. See the docs. 


## Inline docs


