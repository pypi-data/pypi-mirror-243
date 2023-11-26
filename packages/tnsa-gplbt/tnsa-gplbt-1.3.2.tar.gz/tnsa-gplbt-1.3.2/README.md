TNSA GPLBT IS A AI MODEL DEVELOPED BY TNSA FOR TEXT GENERATION I IS A PRE-TRAINED MODEL TO GENERATE TEXT.



HOW TO USE TNSA Generative Pre-Trained Language Based Transformer(GPLBT)?


import numpy as np
import os
import json
import random

# Load the pre-trained model architecture
model_json_file = 'text_generation_model.json'

if not os.path.exists(model_json_file):
    print("Model architecture file not found.")
    exit()

with open(model_json_file, 'r') as json_file:
    model_architecture = json.load(json_file)

input_dim = model_architecture['input_dim']
output_dim = model_architecture['output_dim']
word_to_index = model_architecture['word_to_index']
index_to_word = model_architecture['index_to_word']

# Load weights and biases from provided CSV files
weights_hidden = np.loadtxt('weights_hidden.csv', delimiter=',')
biases_hidden = np.loadtxt('biases_hidden.csv', delimiter=',')
weights_output = np.loadtxt('weights_output.csv', delimiter=',')
biases_output = np.loadtxt('biases_output.csv', delimiter=',')

# Define a function to generate text
def generate_text(seed_text, next_words, model_architecture, temperature=1.0):
    generated_text = seed_text
    recent_words = seed_text.split()  # Store the most recent words

    for _ in range(next_words):
        # Calculate the output probabilities for the entire vocabulary
        token_list = generated_text.split()
        token_list = token_list[-(input_dim - 1):]

        token_indices = [word_to_index[word] for word in token_list]
        token_encoding = np.zeros(input_dim)

        for idx in token_indices:
            token_encoding[idx] = 1

        hidden_layer_input = np.dot(token_encoding, weights_hidden) + biases_hidden
        hidden_layer_output = 1 / (1 + np.exp(-hidden_layer_input))

        output_layer_input = np.dot(hidden_layer_output, weights_output) + biases_output
        output_layer_output = np.exp(output_layer_input) / np.sum(np.exp(output_layer_input))

        # Adjust the temperature to control randomness
        scaled_output = np.log(output_layer_output) / temperature
        scaled_output = np.exp(scaled_output - np.max(scaled_output))
        scaled_output = scaled_output / scaled_output.sum()

        # Sample from the modified probabilities using np.random.choice
        next_word_index = np.random.choice(range(output_dim), p=scaled_output)
        next_word = index_to_word[str(next_word_index)]

        if next_word not in recent_words:
            recent_words.append(next_word)
            if len(recent_words) > input_dim - 1:
                recent_words.pop(0)

            generated_text += " " + next_word

    return generated_text

# Example usage
seed_text = "your seed text"
generated_text = generate_text(seed_text, next_words=50, model_architecture=model_architecture, temperature=0.7)
print(generated_text)
