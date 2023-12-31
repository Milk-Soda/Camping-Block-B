
# import spacy
# from spacy.matcher import Matcher
# import json

# # Load spaCy model
# nlp = spacy.load("en_core_web_sm") 

# # ... (previous code remains unchanged)

# def process_user_input(user_input: str):
#     # Use spaCy for natural language processing
#     doc = nlp(user_input)

#     # Extract entities, keywords, or any relevant information from the user input
#     entities = [ent.text for ent in doc.ents]
#     keywords = [token.text for token in doc if token.is_alpha]

#     return entities, keywords

# def chat_bot():
#     knowledge_base: dict = load_knowledge_base('knowledge_base.json')
#     new_answer: str = ""

#     while True:
#         user_input: str = input('You: ')

#         if user_input.lower() == 'quit':
#             break

#         entities, keywords = process_user_input(user_input)

#         # Use entities and keywords for matching and handling user input

#         # ... (rest of the code)

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

def chat_bot(user_input):
    knowledge_base = load_knowledge_base('knowledge_base.json')
    new_answer = ""
    bot_response = ""

    # Use user_input directly in find_best_match instead of [q["question"] for q in knowledge_base.get("questions", [])]
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base.get("questions", [])])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        if answer is not None:
            bot_response = f'Bot: {answer}'
        else:
            bot_response = 'Bot: I don\'t know the answer. Can you teach me?'
            new_answer = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                bot_response = 'Bot: Thank you! I learned a new response!'

    else:
        bot_response = 'Bot: I don\'t know the answer. Can you teach me?'
        new_answer = input('Type the answer or "skip" to skip: ')

        if new_answer.lower() != 'skip':
            knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            bot_response = 'Bot: Thank you! I learned a new response!'

    return bot_response

user_input = input('You: ')
response = chat_bot(user_input)
print(response)


if __name__ == "__main__":
    chat_bot()


