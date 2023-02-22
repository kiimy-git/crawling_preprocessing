import os
import openai
import ssl
import certifi
import requests
import urllib3

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

client = urllib3.PoolManager(ca_certs=certifi.where())

openai.api_key = client.request("GET", "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")

def chat(prompt):
    
    ## 모델 엔진 선택
    model_engine = "text-davinci-003"

    ## 맥스 토큰(=문장 길이)
    max_tokens = 2048

    completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0.3,      # creativity
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return completion

models = openai.Model.list()

# if __name__ == '__main__':
#     prompt = ""
#     response = chat(prompt=prompt)

#     print(response)