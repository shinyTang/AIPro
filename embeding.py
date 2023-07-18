import os
import openai
import numpy as np
import pandas
import time

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

model = "text-embedding-ada-002" 

MAX_LEN = 2048

prompt_prefix = """
你是一个客服，回答用户关于文档的问题。
仅使用以下资料提供的事实进行回答。 如果下面没有足够的信息，就说你不知道。不要生成不使用以下资料的答案。

资料：
{sources}
"""
summary_prompt_template =  """
以上是到目前为止的对话记录，下面我将提出一个新问题，需要通过在知识库中搜索相关的条目来回答问题。根据以上的对话记录和下面的新问题，生成一个英文的查询语句，用于在知识库中搜索相关的条目。你只需要回答查询的语句，不用加其他任何内容。

新问题：
{question}
"""

# def cosine_similarity(a, b):
#     return np.dot(a, b) 

# embedding1 = openai.Embedding.create(
#     input="苹果", engine="text-embedding-ada-002"
# )["data"][0]["embedding"]
# embedding2 = openai.Embedding.create(
#     input="apple", engine="text-embedding-ada-002"
# )["data"][0]["embedding"]
# embedding3 = openai.Embedding.create(
#     input="鞋子", engine="text-embedding-ada-002"
# )["data"][0]["embedding"]

# print(cosine_similarity(embedding1, embedding2))
# print(cosine_similarity(embedding1, embedding3))
# print(cosine_similarity(embedding2, embedding3))

def cos_sim(a, b):
    return np.dot(a, b)


def get_chat_answer(messages: dict, max_token=1024):
    return openai.ChatCompletion.create(
        engine="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=max_token,
    )["choices"][0]["message"]


# def get_embedding(text):
#     return openai.Embedding.create(
#         engine="text-embedding-ada-002",
#         input=text,
#     )["data"][
#         0
#     ]["embedding"]


def get_embedding(text):
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    embedding = response["data"][0]["embedding"]
    assert len(embedding) == 1536
    return embedding


def main():
    df = pandas.read_csv("output.csv")
    print(df["content"])
    for text in df["content"]:
        print(text)
    embeddings = [get_embedding(text) for text in df["content"]]
    df["embedding"] = embeddings
    df.to_csv("docs.csv", index=False)


if __name__ == "__main__":  
    star = time.time()
    main()
    print(f"Time taken: {time.time() - star}")

    history = []
    user_input = ""

    while(True):
        user_input = input()
        if len(history) == 0:
            query = user_input
        else:
            query = get_chat_answer(
                history
                + [
                    {
                        "role": "user",
                        "content": summary_prompt_template.format(question=user_input),
                    }
                ],
                max_token=32,
            )["content"]
       
        print(f"Searching: {query}")


        docs = pandas.read_csv("docs.csv", converters={"embedding": eval})
        pandas.set_option("display.max_colwidth", None)

        query_embedding = get_embedding(query)
        dot_products = np.dot(np.stack(docs["embedding"].values), query_embedding)
        top_index = np.argsort(dot_products)[-1:]
        top_content = (
            docs.iloc[top_index]["content"].to_string(index=False)
            if dot_products[top_index] > 0.8
            else "no information"
        )
        print("top_content: " + top_content)

        history.append({"role": "user", "content": user_input})

        massage = [
            {"role": "user", "content": prompt_prefix.format(sources=top_content)},
            {
                "role": "assistant",
                "content": "好的，我只会根据以上提供的资料提供的内容回答问题，我不会回答不使用资源的内容。",
            },
        ] + history

        res = get_chat_answer(massage)
        print(res["content"])



    # while(True):
    #     res = get_chat_answer(massage)
    #     print(res["content"])
    #     massage.append({"role": "assistant", "content": res['content']})
    #     history.append(res)
    #     print("-" * 50, end="\n\n")
    #     user_input = input()      
    #     massage.append({"role": "user", "content": user_input})

    #check the email
    


