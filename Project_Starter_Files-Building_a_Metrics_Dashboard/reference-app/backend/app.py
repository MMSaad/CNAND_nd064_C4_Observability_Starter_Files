from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)
CORS(app)


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


@app.route("/")
def homepage():
    with tracer.start_span('home-span') as span:
        span.set_tag('home-tag', 'Sample from home')
        return "Hello World"


@app.route("/api")
def my_api():
    with tracer.start_span('api-span') as span:
        span.set_tag('api-tag', 'Sample from api')
        answer = "something"
        return jsonify(repsonse=answer)


tracer = init_tracer('backend-service')
tracing = FlaskTracing(tracer, True, app)

if __name__ == "__main__":
    app.run()
