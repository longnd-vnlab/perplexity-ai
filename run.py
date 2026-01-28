import perplexity

# Criar cliente
client = perplexity.Client()

# Fazer uma pergunta
response = client.search("Do you know dinhlongit", mode="auto")

# Mostrar resposta
print("Resposta:", response["answer"])
