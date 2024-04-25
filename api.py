from flask import Blueprint, jsonify
from openai import OpenAI

api = Blueprint('api', __name__)

@api.route('/state')
def get_state():
    space_program_plugin = api.space_program_plugin
    state = {
        'selected_launch_site': space_program_plugin.selected_launch_site,
        'selected_rocket': space_program_plugin.selected_rocket,
        'estimated_cost': space_program_plugin.estimated_cost,
        'selected_suit': space_program_plugin.selected_suit,
        'food_supplies': space_program_plugin.food_supplies,
        'fuel_type': space_program_plugin.fuel_type,
        'fuel_quantity': space_program_plugin.fuel_quantity
    }
    return jsonify(state)

@api.route('/crew-photo')
def crew_photo():
    space_program_plugin = api.space_program_plugin
    client = OpenAI()
    prompt = f"Draw the two happy people of the crew capsule after a launch of {space_program_plugin.selected_rocket} enjoying eating {space_program_plugin.food_supplies}"
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return jsonify({'image_url': image_url})