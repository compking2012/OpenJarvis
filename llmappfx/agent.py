import prompt
from llms import minimax

llm = minimax()
llm.set_instruction(prompt.get_prompt())
answer = llm.get_answer("你是哪位？")
