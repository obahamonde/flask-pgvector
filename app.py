from os import environ
from typing import List

import openai
import psycopg
from boto3 import Session
from dotenv import load_dotenv  # type: ignore
from flask import Flask, jsonify, make_response, render_template, request
from pgvector.psycopg import register_vector

load_dotenv()


openai.api_key = environ.get("OPENAI_API_KEY")

aws = Session(
	aws_access_key_id=environ.get("AWS_ACCESS_KEY_ID"),
	aws_secret_access_key=environ.get("AWS_SECRET_ACCESS_KEY"),
	region_name="us-east-1"
)


polly = aws.client("polly")


def text_to_speech(text: str) -> bytes:
	response = polly.synthesize_speech(
		Text=text,
		VoiceId="Mia",
		OutputFormat="mp3"
	)
	return response["AudioStream"].read()

conn = psycopg.connect('postgresql://postgres@db:5432/postgres', dbname='postgres', autocommit=True)

def on_start():
	conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
	register_vector(conn)
	conn.execute('CREATE TABLE IF NOT EXISTS text_embeddings (id bigserial PRIMARY KEY, content text, embedding vector(1536))')

def create_embedding(input: List[str],save:bool=True)->List[List[float]]:
	response = openai.Embedding.create(input=input,  model='text-embedding-ada-002')
	embeddings = [v['embedding'] for v in response['data']]
	if save:
		for content, embedding in zip(input, embeddings):
			conn.execute('INSERT INTO text_embeddings (content, embedding) VALUES (%s, %s)', (content, embedding)) # type: ignore
	return embeddings # type: ignore

def similarity_search(text:str, limit: int = 5):
	vector = create_embedding([text],save=False)[0]
	neighbors = conn.execute('SELECT content FROM text_embeddings ORDER BY embedding <=> cast(%(vector)s as vector(1536)) LIMIT %(limit)s', {'vector': vector, 'limit': limit}).fetchall()
	return [n[0] for n in neighbors]

def completion(text:str)->str:
	response = openai.ChatCompletion.create( # type: ignore
		model="gpt-4-0613",
		messages=[{
			"role":"user",
			"content":text
		},
		{
			"role":"system",
			"content":f"Respuestas similares en la historia del chat:\n" + "\n".join(similarity_search(text))
		}],
		max_tokens=1024,
		temperature=1
	)
	answer = response.choices[0].message.content # type: ignore
	create_embedding([answer])
	return answer # type: ignore


app = Flask(__name__)


@app.get("/")
def index():
	return render_template("index.html")

@app.get("/api/chat")
def chat():
	q = request.args.get("q")
	if not q:
		return jsonify({"message": "No question provided"}), 400
	response = make_response(text_to_speech(completion(q)))
	response.headers.set("Content-Type", "application/octet-stream")
	return response
