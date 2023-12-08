
# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# # Load pre-trained GPT-2 model and tokenizer
# model_name = "gpt2"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# # Set the model to evaluation mode
# model.eval()

# # Function to generate a response given user input
# def generate_response(user_input, max_length=100):
#     input_ids = tokenizer.encode(user_input, return_tensors="pt")

#     # Generate response
#     output = model.generate(input_ids, max_length=max_length, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)

#     # Decode the generated response
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     return response

# # Chatbot loop
# print("Chatbot: Hello! I'm your camping assistant. Type 'exit' to end the conversation.")
# while True:
#     user_input = input("You: ")
    
#     if user_input.lower() == 'exit':
#         print("Chatbot: Goodbye! Have a great day.")
#         break

#     # Generate and print the chatbot's response
#     response = generate_response(user_input)
#     print(f"Chatbot: {response}")

# -------------------------------------------------------------------------------------------------------------------------------
import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            knowledge_base: dict = json.load(file)
        return knowledge_base
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {"questions": []}

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base.get("questions", []):
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    new_answer: str = ""

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        # Use user_input directly in find_best_match instead of [q["question"] for q in knowledge_base.get("questions", [])]
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base.get("questions", [])])

        if best_match:
            answer: str | None = get_answer_for_question(best_match, knowledge_base)
            if answer is not None:
                print(f'Bot: {answer}')
            else:
                print('Bot: I don\'t know the answer. Can you teach me?')
                new_answer = input('Type the answer or "skip" to skip: ')

                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print('Bot: Thank you! I learned a new response!')

        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == "__main__":
    chat_bot()


