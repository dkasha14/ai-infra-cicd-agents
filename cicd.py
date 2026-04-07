from llm import IaCAgent

agent = IaCAgent()

def generate_jenkins_pipeline(user_input):
    return agent.generate_pipeline(user_input)
