import opengradient as og

client = og.Client(
    private_key="0xd024bdb371d0249f82cdac2e323616f6baedf3dd8b12767a7373d281255afee0"
)

# Approve OPG tokens for spending
print("Approving OPG tokens...")
client.llm.ensure_opg_approval(opg_amount=5.0)
print("Approved!\n")

# Ask for a coin
coin = input("Enter a coin name (e.g. Bitcoin, Solana, ETH): ")

print(f"\nAsking AI for its opinion on {coin}...\n")

messages = [
    {
        "role": "user",
        "content": f"You are a sharp crypto analyst. Give your honest opinion on {coin} — covering what it is, its strengths, weaknesses, and overall sentiment. Be direct and concise."
    }
]

result = client.llm.chat(
    model=og.TEE_LLM.CLAUDE_HAIKU_4_5,
    messages=messages,
    max_tokens=300,
    temperature=0.7
)

print("=" * 50)
print(f"AI OPINION ON {coin.upper()}")
print("=" * 50)
print(result.chat_output['content'])
print("=" * 50)
print(f"On-chain proof: {result.payment_hash}")