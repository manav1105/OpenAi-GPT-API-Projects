import os
import requests
import shutil

from openai import OpenAI

client = OpenAI()

def system_prompt():
    return "You are a helpful assistant to write blogposts."


def create_prompt(title):
    prompt = """Manav's Website
 
 Biography
 I am a AI student learning about the power of LLM!


 Blog

 june 05, 2024
 Title: Power of LLM in Drug discovery and Healthcare
 tags: tech, LLM, Drug discover, 
 Summary:  I talk about LLMs and How Healthcare and Biotech industry can benefit from LLMs. I explain why I think that LLMs are game changer in Biotech.
 Full text:""".format(title)
    return prompt

def get_blog_from_openai(blog_title):
    response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": system_prompt()},
                                {"role": "user", "content": create_prompt(blog_title)},
                            ],
                                temperature=0.7
)

    return response.choices[0].message.content

def dalle3_prompt(title):
    prompt = f"Pixel art showing '{title}'."
    return prompt


def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream = True)
    
    if image_res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")
    return image_res.status_code, file_name


def get_cover_image(title, save_path):
    response = client.images.generate(
                    model="dall-e-3",
                    prompt=dalle3_prompt(title),
                    size="1024x1024",
                    quality="standard",
                    n=1,
                    )
    image_url = response.data[0].url
    status_code, file_name = save_image(image_url, save_path)
    return status_code, file_name


