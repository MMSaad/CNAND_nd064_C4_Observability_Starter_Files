from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing
import pymongo
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)
CORS(app)
app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

metrics.info('app_info', 'backend service', version='1.0.15')


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
    

@app.route("/star", methods=["POST"])
def add_star():
    star = mongo.db.stars
    name = request.json["name"]
    distance = request.json["distance"]
    star_id = star.insert({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})


tracer = init_tracer('backend-service')
tracing = FlaskTracing(tracer, True, app)

if __name__ == "__main__":
    app.run()
