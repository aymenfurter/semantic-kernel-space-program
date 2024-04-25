import asyncio
import os
from flask import Flask, jsonify, render_template
from space_program_plugin import SpaceProgramPlugin
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.core_plugins import MathPlugin, TimePlugin
from semantic_kernel.planners import FunctionCallingStepwisePlanner, FunctionCallingStepwisePlannerOptions
from semantic_kernel.utils.settings import openai_settings_from_dot_env
from api import api as api_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')

kernel = Kernel()
space_program_plugin = SpaceProgramPlugin()

api_blueprint.space_program_plugin = space_program_plugin

@app.route('/')
def index():
    return render_template('index.html')

async def run_planner():
    service_id = "planner"
    api_key, _ = openai_settings_from_dot_env()
    kernel.add_service(
        OpenAIChatCompletion(
            service_id=service_id,
            ai_model_id="gpt-4",
            api_key=api_key,
        ),
    )
    kernel.add_plugins({"SpaceProgramPlugin": space_program_plugin})
    options = FunctionCallingStepwisePlannerOptions(
        max_iterations=10,
        max_tokens=4000,
    )
    planner = FunctionCallingStepwisePlanner(service_id=service_id, options=options)
    await planner.invoke(kernel, "launch a rocket to the moon")

@app.route('/launch', methods=['POST'])
def launch_rocket():
    asyncio.run(run_planner())
    return jsonify({'message': 'Rocket launched successfully'})

if __name__ == "__main__":
    app.run(debug=True)

from openai import OpenAI
@app.route('/crew-photo')
def crew_photo():
    client = OpenAI()
    prompt = f"Draw the inside of the crew capsule after a launch of {space_program_plugin.selected_rocket} eating {space_program_plugin.food_supplies}"
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return jsonify({'image_url': image_url})