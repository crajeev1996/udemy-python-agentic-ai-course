import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My name is Chaitanya Rajeev"

tokens = enc.encode(text)

# [25216, 3274, 0, 3673, 1308, 382, 1036, 1271, 7963, 40516, 2882, 85]
print("Tokens", tokens)

input_tokens = [25216, 3274, 0, 3673, 1308, 382, 1036, 1271, 7963, 40516, 2882, 85]

decode = enc.decode(input_tokens)

print(f"Decoded string = {decode}dea")