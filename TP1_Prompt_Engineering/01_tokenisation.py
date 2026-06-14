import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4o")
print(f"Encoding name: {encoding.name}")

system_message = """
Perform Sentiment analysis of the review presented in the user
message. The result should be positive or negative. Do not justify
your response """

tokens = encoding.encode(system_message)
print(f"Number of tokens: {len(tokens)}")
print(f"Tokens: {tokens}")

print("\nDecoded tokens:")
for token in tokens:
    print(encoding.decode_single_token_bytes(token).decode('utf-8', errors='ignore'), end="|")

def num_tokens_from_string(string: str, encoding_name: str = "o200k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

print(f"\n\nTokens in 'tiktoken is great!': {num_tokens_from_string('tiktoken is great!')}")
