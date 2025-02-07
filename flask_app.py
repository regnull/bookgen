from flask import Flask, render_template, request, g, send_from_directory, flash, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

app = Flask(__name__)

def get_mongo_client():
    if 'mongo_client' not in g:
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI environment variable must be set")
        g.mongo_client = MongoClient(uri)
    return g.mongo_client

@app.route('/')
def display_index():
    return send_from_directory('static', 'index.html')

@app.route('/submit-book-description', methods=['POST'])
def submit_book_description():
    book_description = request.form.get('bookDescription')
    if not book_description:
        flash('Book description is required!')
        return redirect(url_for('display_index'))
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=1000)
    sys_prompt = '''
You are a masterful book writer.
'''
    user_prompt = '''
Create a book outline for the following book description:
{book_description}

The outline must be in markdown format, providing the list of chapters.
    '''

    prompt_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(sys_prompt),
        HumanMessagePromptTemplate.from_template(user_prompt)
    ])
    
    res = llm.invoke(prompt_template.format_messages(book_description=book_description))


    return res.content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    app.run(debug=True)