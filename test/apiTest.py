from llm.llmApi import LlmApi

llm = LlmApi()
res1, res2, res3, res4 = llm.getSuggestions("hello")

print(res1)
print(res2)
print(res3)
print(res4)