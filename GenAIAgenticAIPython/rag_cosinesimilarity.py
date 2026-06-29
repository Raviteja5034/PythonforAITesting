import os
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.environ["OPENAI_API_KEY"]
)


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    """

    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    similarity = np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

    return similarity


def answer_correctness(generated_answer, expected_answer):

    gen_embedding = embeddings.embed_query(generated_answer)
    exp_embedding = embeddings.embed_query(expected_answer)

    score = cosine_similarity(gen_embedding, exp_embedding)

    return round(score, 4)


if __name__ == "__main__":

    generated = """
    PM of India is Modi

    """

    expected = """
    AI is next generation IT 

    """

    score = answer_correctness(generated, expected)

    print(f"Answer Correctness Score : {score}")

    if score > 0.85:
        print("PASS")
    else:
        print("FAIL")