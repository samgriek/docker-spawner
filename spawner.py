from flask import Flask, request, jsonify
import docker
import requests
import time
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = docker.from_env()


@app.route('/spawn', methods=['POST'])
def spawn():
    try:
        dockerfile_path = request.json['dockerfile_path']
        
        with open(f"{dockerfile_path}/Dockerfile", "r") as f:
            dockerfile_contents = f.read()
            logger.info("Contents of Dockerfile:")
            logger.info(dockerfile_contents)
        
        image, build_log = client.images.build(path=dockerfile_path)

        logger.info(f"{build_log=}")
        logger.info(f"{image=}")

        container = client.containers.run(image, detach=True, network='docker-spawner-2_my_network', name='my_flask_container', ports={'5000/tcp': 5000})


        time.sleep(5)
        
        response = requests.get('http://my_flask_container:5000/')
        
        return jsonify({
            'message': 'Successfully spawned container and received API response.',
            'api_response': response.text,
            'container_id': container.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
