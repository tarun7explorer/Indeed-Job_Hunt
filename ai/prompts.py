TEXT_PROMPT = """
Candidate Profile: {profile}
Question: {question}

Provide a concise, direct answer in 1-2 sentences max.
"""

CHOICE_PROMPT = """
Candidate Profile: {profile}
Question: {question}
Options: {choices}

Select the single best matching option. Return ONLY the exact option text.
"""