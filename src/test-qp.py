from quality_prompts.prompt import QualityPrompt

directive = "You are given a text and your task is to classify its sentiment as positive or negative"

prompt = QualityPrompt(directive)

input_text = "Today I've been searching for you. A feeling that does not go away. I just can't help myself."
prompt.few_shot(input_text=input_text, n_shots=3)

print(prompt.compile())



