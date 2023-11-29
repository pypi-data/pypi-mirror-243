# GPTQAPI Server

an LLM API server for AutoGPTQ model. This server is designed to be compatible with the OpenAI API, allowing you to seamlessly use OpenAI clients with it.

## Installation

Before you can run the server, you need to install the necessary package. You can do this easily with `pip`:

```bash
pip install autogptq-api
```

## Usage

To run the GPTQAPI Server, use the following command:

```bash
python -m gptqapi.server [model-name] [port]
```

The `model-name` argument is mandatory while the `port` argument is optional, if not provided, it will default to a standard port for serving the API.

You can also configure the server using a `.env` file for convenience. Here's an example:

```dotenv
# .env file
MODEL_NAME=robinsyihab/Sidrap-7B-v2-GPTQ
PORT=8000
WORKERS=1
SYSTEM_PROMPT=
```

This `.env` file sets default values for the model name, the port the server will listen on, the number of worker processes, and the system prompt which can be used to customize behavior.

## API Schema

This server follows the OpenAI API schema, allowing for seamless integration with OpenAPI client libraries. You can utilize all typical endpoints as if you were using the actual OpenAI API, making it easier to integrate into your existing infrastructure if you're familiar with the OpenAI platform.

## Environment Variables

Here is a list of environment variables you can use to configure the server:

- `MODEL_NAME`: (required) Identifies which AutoGPTQ model to use.
- `PORT`: (optional) Specifies the port number on which to run the API server.
- `WORKERS`: (optional) Defines the number of worker processes for handling requests.
- `SYSTEM_PROMPT`: (optional) Sets the system prompt for the model if needed.

## Starting the Server

Once you have configured your environment variables or are ready to use the command line arguments, you can start the server by running the provided command. The server will serve your specified or default model and be ready to handle API requests.

## Contributing

If you're looking to contribute to the GPTQAPI Server project, please feel free to open an issue or create a pull request with your suggested changes or improvements.

Thank you for choosing GPTQAPI Server for running your local LLM API server. We hope you find it easy to set up and integrate into your development workflow.