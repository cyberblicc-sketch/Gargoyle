from flask import Flask, jsonify, render_template, request, send_from_directory
from pathlib import Path

app = Flask(__name__)


class MessageBus:
    def __init__(self):
        self.queue = []

    def publish(self, message):
        self.queue.append(message)

    def consume_all(self):
        items = self.queue[:]
        self.queue.clear()
        return items


class Coordinator:
    def __init__(self, bus):
        self.bus = bus

    def handle(self, goal):
        tasks = [
            {'role': 'jurist_task', 'query': goal},
            {'role': 'cartographer_task', 'query': goal},
            {'role': 'strategist_task', 'query': goal},
        ]
        for task in tasks:
            self.bus.publish(task)
        results = []
        for task in tasks:
            if task['role'] == 'jurist_task':
                results.append(jurist(task['query']))
            elif task['role'] == 'cartographer_task':
                results.append(cartographer(task['query']))
            elif task['role'] == 'strategist_task':
                results.append(strategist(task['query']))
        return results


def jurist(query: str):
    return {
        'source': 'Jurist',
        'data': f"Legal analysis for '{query}'... identify the relevant rules, constraints, and filing risks."
    }


def cartographer(query: str):
    return {
        'source': 'Cartographer',
        'data': f"Patent and market map for '{query}'... identify 3 adjacent opportunities and likely overlap areas."
    }


def strategist(query: str):
    return {
        'source': 'Strategist',
        'data': f"Scenario simulation for '{query}'... compare conservative, balanced, and aggressive paths."
    }


def run_demo(goal: str):
    bus = MessageBus()
    coordinator = Coordinator(bus)
    return coordinator.handle(goal)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/demo', methods=['POST'])
def demo():
    payload = request.get_json(silent=True) or {}
    query = (payload.get('query') or '').strip()
    if not query:
        return jsonify({'error': 'query is required'}), 400
    return jsonify({'query': query, 'results': run_demo(query)})


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'})


@app.route('/docs/<path:filename>')
def docs_file(filename):
    return send_from_directory(Path(app.root_path) / 'docs', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
