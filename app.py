from flask import Flask, redirect, render_template, request, url_for
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        message = request.form.get('message')
        
        if message and message.strip():  # check for empty input
            data_to_insert = {"message": message.strip()}
            supabase.table('confessions').insert(data_to_insert).execute()
        
        return redirect(url_for('show_all_confessions'))

    return render_template('index.html')

@app.route('/confessions')
def show_all_confessions():
    response = supabase.table('confessions').select('*').order('created_at', desc=True).execute()
    all_confessions = response.data
    return render_template('confessions.html', confessions=all_confessions)

if __name__ == '__main__':
    app.run(debug=True)
