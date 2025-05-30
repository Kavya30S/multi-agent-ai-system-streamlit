from agents.email_agent import EmailAgent

email_agent = EmailAgent()
sample_email = """
From: customer@example.com
Subject: Request for Quotation
Dear Team,
We need a quote for 100 units of Product X. Please respond urgently.
Best,
Customer
"""
result = email_agent.process_email("email-thread", sample_email)
print(result)