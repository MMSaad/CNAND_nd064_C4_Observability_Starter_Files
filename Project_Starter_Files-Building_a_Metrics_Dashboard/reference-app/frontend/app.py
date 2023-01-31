from flask import Flask, render_template, request
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

metrics.info('app_info', 'frontend service', version='1.0.15')


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
        return render_template("main.html")


tracer = init_tracer('frontend-service')
tracing = FlaskTracing(tracer, True, app)

if __name__ == "__main__":
    app.run()
