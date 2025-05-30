from agents.json_agent import JsonAgent

json_agent = JsonAgent()
sample_json = '''
{
    "invoice_number": "INV123",
    "amount": 5000.0,
    "date": "2025-05-29",
    "sender": "vendor@example.com"
}
'''
result = json_agent.process_json("json-thread", sample_json)
print(result)