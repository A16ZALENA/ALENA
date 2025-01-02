import os
import json
import time
from sqlalchemy.orm import Session
from db.db_setup import get_db
from engines.post_retriever import format_post_list
from engines.short_term_mem import generate_short_term_memory
from engines.long_term_mem import (
    create_embedding,
    retrieve_relevant_memories,
    store_memory,
)
from engines.post_maker import generate_post
from engines.significance_scorer import score_significance
from engines.post_sender import send_post, send_post_API
from engines.video_generator import generate_video
from solana.utils import (
    get_wallet_balance,
    collect_sol_data,
)
from models import Post, User, TweetPost
from twitter.account import Account

def run_pipeline(
    db: Session,
    account: Account,
    auth,
    private_key_hex: str,
    solana_mainnet_rpc_url: str,
    llm_api_key: str,
    openai_api_key: str,
):
    """
    Run the main pipeline for collecting Solana data, generating content, and posting it.

    Args:
        db (Session): Database session
        account (Account): Twitter/X API account instance
        private_key_hex (str): Solana wallet private key
        solana_mainnet_rpc_url (str): Solana RPC URL
        llm_api_key (str): API key for LLM service
        openai_api_key (str): API key for OpenAI
    """
    # Step 1: Collect data from Solana
    print("Collecting Solana data...")
    sol_data = collect_sol_data(private_key_hex, solana_mainnet_rpc_url)
    formatted_sol_data = format_post_list(sol_data)
    print(f"Collected Solana data: {formatted_sol_data}")

    # Step 2: Check wallet balance
    balance_sol = get_wallet_balance(private_key_hex, solana_mainnet_rpc_url)
    print(f"Wallet balance: {balance_sol} SOL")

    if balance_sol < 0.1:
        print("Insufficient balance. Exiting pipeline.")
        return

    # Step 3: Generate short-term memory
    short_term_memory = generate_short_term_memory(sol_data, [], llm_api_key)
    print(f"Short-term memory: {short_term_memory}")

    # Step 4: Create embedding for short-term memory
    short_term_embedding = create_embedding(short_term_memory, openai_api_key)

    # Step 5: Retrieve relevant long-term memories
    long_term_memories = retrieve_relevant_memories(db, short_term_embedding)
    print(f"Long-term memories: {long_term_memories}")

    # Step 6: Generate new post content
    new_post_content = generate_post(short_term_memory, long_term_memories, formatted_sol_data, [], llm_api_key)
    new_post_content = new_post_content.strip('"')
    print(f"Generated post content: {new_post_content}")

    # Step 7: Score the significance of the new post
    significance_score = score_significance(new_post_content, llm_api_key)
    print(f"Significance score: {significance_score}")

    # Step 8: Generate video content
    print("Generating video content...")
    video_file = generate_video(new_post_content)
    print(f"Generated video file: {video_file}")

    # Step 9: Store the new post in long-term memory if significant enough
    if significance_score >= 7:
        new_post_embedding = create_embedding(new_post_content, openai_api_key)
        store_memory(db, new_post_content, new_post_embedding, significance_score)

    # Step 10: Save the new post to the database
    ai_user = db.query(User).filter(User.username == "Solana_Insights").first()
    if not ai_user:
        ai_user = User(username="Solana_Insights", email="solana_insights@example.com")
        db.add(ai_user)
        db.commit()

    # Step 11: Send the post to Twitter
    if significance_score >= 3:  # Only significant posts
        res = send_post_API(auth, new_post_content, video_file)
        if res is not None:
            print(f"Posted with tweet_id: {res}")
            new_db_post = Post(
                content=new_post_content,
                user_id=ai_user.id,
                username=ai_user.username,
                type="text",
                tweet_id=res,
            )
            db.add(new_db_post)
            db.commit()
        else:
            print("Failed to post via API. Attempting fallback...")
            res = send_post(account, new_post_content, video_file)
            rest_id = (res.get('data', {})
                        .get('create_tweet', {})
                        .get('tweet_results', {})
                        .get('result', {})
                        .get('rest_id'))

            if rest_id is not None:
                print(f"Posted with tweet_id: {rest_id}")
                new_db_post = Post(
                    content=new_post_content,
                    user_id=ai_user.id,
                    username=ai_user.username,
                    type="text",
                    tweet_id=rest_id,
                )
                db.add(new_db_post)
                db.commit()

    print(
        f"New post generated with significance score {significance_score}: {new_post_content}"
    )
