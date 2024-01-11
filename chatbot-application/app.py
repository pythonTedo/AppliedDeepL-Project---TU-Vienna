from flask import Flask, render_template, request, jsonify, redirect, flash, url_for, session
import sys
import time
import os
import gc
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoConfig,
    pipeline,
)
from peft import LoraConfig, PeftModel
import threading

app = Flask(__name__)
#app.secret_key = "DemoLab Solution"

app_dir = os.path.dirname(__file__) 
#base_model = "./model/base_model"
#bulgarian_model = "./model/new_model"
base_model = "NousResearch/Llama-2-7b-chat-hf"
bulgarian_model = "teodor98/LORA_Config_BG_Recepies"

# Activate 8-bit precision base model loading
use_8bit = True
# Compute dtype for 4-bit base models
bnb_4bit_compute_dtype = "float16"
# Quantization type (fp4 or nf4)
bnb_4bit_quant_type = "nf4"
# Load tokenizer and model with QLoRA configuration
compute_dtype = getattr(torch, bnb_4bit_compute_dtype)
# Load the entire model on the GPU 0
device_map = {"": 0}
# Set Temperature of the model
def_temp = 0.4
# Set Generated text length
def_len_text = 3000
# Chat hitory
def_conversation = 1

# Reload tokenizer to save it
tokenizer = AutoTokenizer.from_pretrained(bulgarian_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

def load_init_model():
    global model, base_model, bulgarian_model
    print(f"Loading the LLama model", file=sys.stderr)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model,
        low_cpu_mem_usage=True,
        return_dict=True,
        torch_dtype=torch.float16,
        device_map=device_map,
    )
    model = PeftModel.from_pretrained(base_model, bulgarian_model)
    model = model.merge_and_unload()
    print("Model loaded successfuly", file=sys.stderr)

def generate_response(instruction, temperature, text_len, conversations):
    def_prompt = "<s>[INST] <<SYS>> You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, dont use emoji and answer in the language you are being asked. <</SYS>>  "

    if 'conversation_history' not in session:
        session['conversation_history'] = []
    
    new_instruction = f"[INST] {instruction} [/INST]"
    
    if conversations == 0:
        session.pop('conversation_history', None)
        session.modified = True
        session['conversation_history'] = []
    
    if len(session['conversation_history']) > conversations:
    # Remove the oldest items so that our list will have space for the new item
        session['conversation_history'] = session['conversation_history'][-conversations:]
        session.modified = True

    # Concatenate the new instruction with the past conversation history
    conversation_input = " ".join(session['conversation_history']) + " " + new_instruction
    final_string = conversation_input.replace("[INST]", def_prompt, 1)

    print("-------------------------------------------------------------------------------", file=sys.stderr)
    print(final_string, file=sys.stderr)
   
    # Generate the response using your model (replace with actual model call)
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=text_len, temperature=temperature)
    gen = pipe(final_string)
    generated = gen[0]['generated_text']

    # Extract and process the response
    if '[/INST]' in generated:
        # If an [/INST] tag is found, we take the content after the last [/INST] as the response
        response = generated.rsplit('[/INST]', 1)[-1].strip()
    else:
        response = generated.strip()

    new_pair = new_instruction + " " + response

    if conversations != 0:
        session['conversation_history'].append(new_pair)
        session.modified = True

    return response  # Return the generated response


@app.route("/")
def index():
    temperature = session.get('temperature', def_temp)
    length = session.get('length', def_len_text)
    conversations = session.get('conversations', def_conversation)
    #model_choice = session.get('model_choice', def_model_choice)

    print(f"The set paramethers are:\n temperature - {temperature}\n length - {length}\n conversations - {conversations}\n", file=sys.stderr)
    return render_template("index.html", temperature=temperature, length=length, conversations=conversations)


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg")

    # Retrieve session parameters
    temperature = float(session.get('temperature', def_temp))
    text_len = int(session.get('length', def_len_text))
    conversations = int(session.get('conversations', def_conversation))

    # Generate the response
    response = generate_response(msg, temperature, text_len, conversations)
    return response

    
@app.route('/set_params', methods=['POST'])
def set_params():
    temperature = request.form['temperature']
    length = request.form['textLength']
    conversations = request.form['conversations']
    
    session['temperature'] = temperature
    session['length'] = length
    session['conversations'] = conversations

    flash("Parameters set successfully!", 'success')
    return redirect(url_for("index"))

@app.route("/reset_session", methods=['POST'])
def reset_session():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.secret_key = os.urandom(24)

    load_init_model()
    app.run(debug=False, port=8081, host='0.0.0.0')