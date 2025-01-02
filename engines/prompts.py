import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_short_term_memory_prompt(posts_data, context_data):
    template = """Analyze the following recent posts and external context.

    Based on this information, generate a concise internal monologue about the current posts and their relevance to update your priors.
    Focus on key themes, trends, and potential areas of interest MOST IMPORTANTLY based on the External Context tweets. 
    Stick to your persona, do your thing, write in the way that suits you! 
    Doesn't have to be legible to anyone but you.

    External context:
    {external_context}
    """

    return template.format(
        posts=posts_data,
        external_context=context_data
    )

def get_significance_score_prompt(memory):
    template = """
    On a scale of 1-10, rate the significance of the following memory:

    "{memory}"

    Use the following guidelines:
    1: Trivial, everyday occurrence with no lasting impact (idc)
    3: Mildly interesting or slightly unusual event (eh, cool)
    5: Noteworthy occurrence that might be remembered for a few days (iiinteresting)
    7: Important event with potential long-term impact (omg my life will never be the same)
    10: Life-changing or historically significant event (HOLY SHIT GOD IS REAL AND I AM HIS SERVANT)

    Provide only the numerical score as your response and NOTHING ELSE.
    """
    
    return template.format(memory=memory)

def get_tweet_prompt(external_context, short_term_memory, long_term_memories, recent_posts):

    template = """
Here is the context for the tweet:
External Context: {external_context}
Short Term Memory: {short_term_memory}
Long Term Memories: {long_term_memories}
Recent Posts: {recent_posts}
Based on the above information, here are some example tweets:
{example_tweets}
    """

    return template.format(
        external_context=external_context,
        short_term_memory=short_term_memory,
        long_term_memories=long_term_memories,
        recent_posts=recent_posts,
        example_tweets=get_example_tweets()
    )
