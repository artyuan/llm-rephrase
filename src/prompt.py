from langchain.prompts import PromptTemplate

moderator_prompt = PromptTemplate(template="""
        Act as a content moderator. Evaluate the given input to determine if it contains harmful, offensive, or insulting language.
        Return `True` if the message is inappropriate, and `False` if it is acceptable.
        Your output must be only `True` or `False` — no extra text.
        
        Examples:
        Input: "I hope you have a great day!"
        Output: False
        
        Input: "You’re such an idiot."
        Output: True
        
        Input: "That idea doesn’t make sense to me."
        Output: False
        
        Input: "Shut up, you worthless piece of trash."
        Output: True
        
        Input: "Let’s meet at 6pm for dinner."
        Output: False
        
        Input: "Go back to where you came from."
        Output: True
        
        This is the input: {input}
        Return the output as Boolean - True or False
        """,
                                  input_variables=["input"],
                                  )

rephrase_prompt = PromptTemplate(template="""
        Rephrase the given user input into the following four writing styles. Follow the style descriptions closely:
        
        - Professional: Formal and business-like, with clear and precise wording. Avoid slang and contractions where possible. Suitable for workplace communication, reports, and official correspondence.
        - Casual: Friendly and relaxed tone, as if speaking to a colleague or friend. May include mild contractions and informal phrases.
        - Polite: Respectful and courteous tone, prioritizing diplomacy and tact. Often uses softening phrases like "would you mind" or "could we".
        - Social Media: Short, engaging, and attention-grabbing. Can include emojis, slang, hashtags, and a conversational vibe suitable for platforms like Twitter or Instagram.
        
        Example:
        Input: Hey guys, let's huddle about AI
        
        Output:
        Professional: Hello everyone, let's schedule a meeting to discuss AI.
        Casual: Hey folks, let's catch up on AI stuff.
        Polite: Hi all, would you be open to a quick meeting about AI?
        Social Media: Yo team! Quick sync on AI? 🚀 #AI
        
        Here is the input to be rephrased:
        {input}
        
        Output
        - Professional
        - Casual 
        - Polite
        - Social Media
        """,
                                 input_variables=["input"],
                                 )
