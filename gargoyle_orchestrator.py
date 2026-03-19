"""
Gargoyle Orchestrator Demo

This script provides a minimal demonstration of the Gargoyle multi-agent system. It
uses a simple message bus to coordinate tasks between the Jurist, Cartographer and
Strategist agents. In production, replace the dummy functions with actual
implementations that call LLMs, perform graph searches or run simulations.

Run: python3 gargoyle_orchestrator.py
"""

from typing import Dict, Any, List

# Simple message bus for demo purposes
class MessageBus:
    def __init__(self):
        self.subscribers = []
        self.queue: List[Dict[str, Any]] = []

    def publish(self, message: Dict[str, Any]):
        self.queue.append(message)

    def subscribe(self, agent):
        self.subscribers.append(agent)

    def consume(self, filter: Dict[str, Any]):
        # Poll messages until one matches the filter
        while True:
            for i, msg in enumerate(self.queue):
                if all(msg.get(k) == v for k, v in filter.items()):
                    return self.queue.pop(i)

class Agent:
    def __init__(self, bus: MessageBus):
        self.bus = bus

    def handle(self, message: Dict[str, Any]):
        pass

class Coordinator(Agent):
    def handle(self, message):
        goal = message.get('goal', '')
        # Break the goal into sub‑tasks
        sub_tasks = [
            {'role': 'jurist_task', 'query': goal},
            {'role': 'cartographer_task', 'query': goal},
            {'role': 'strategist_task', 'query': goal},
        ]
        for task in sub_tasks:
            self.bus.publish(task)
        results = []
        for _ in range(len(sub_tasks)):
            results.append(self.bus.consume({'role': 'result'}))
        summary = self.summarize(results)
        return summary

    def summarize(self, results: List[Dict[str, Any]]):
        # Summarize the results into a coherent strategy
        lines = [f"- {res['source']}: {res['data']}" for res in results]
        return "\n".join(lines)

class Jurist(Agent):
    def handle(self, message):
        if message['role'] != 'jurist_task':
            return
        query = message['query']
        # TODO: call legal LLM and RAG here
        analysis = f"Legal analysis for '{query}'..."  # placeholder
        self.bus.publish({'role': 'result', 'source': 'Jurist', 'data': analysis})

class Cartographer(Agent):
    def handle(self, message):
        if message['role'] != 'cartographer_task':
            return
        query = message['query']
        # TODO: search patents and update knowledge graph
        mapping = f"Patent mapping for '{query}' produced 3 related patents."  # placeholder
        self.bus.publish({'role': 'result', 'source': 'Cartographer', 'data': mapping})

class Strategist(Agent):
    def handle(self, message):
        if message['role'] != 'strategist_task':
            return
        query = message['query']
        # TODO: run simulation
        simulation = f"Simulation for '{query}' suggests favourable outcome."  # placeholder
        self.bus.publish({'role': 'result', 'source': 'Strategist', 'data': simulation})


def run_demo(goal: str):
    bus = MessageBus()
    coordinator = Coordinator(bus)
    agents = [coordinator, Jurist(bus), Cartographer(bus), Strategist(bus)]
    for ag in agents:
        bus.subscribe(ag)

    # Start the workflow
    result = coordinator.handle({'goal': goal})
    return result

if __name__ == '__main__':
    print("Gargoyle Orchestrator Demo")
    goal = input("Enter your strategic query: ")
    print("Running...\n")
    summary = run_demo(goal)
    print("-- Summary --")
    print(summary)
