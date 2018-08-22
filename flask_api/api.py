from flask import Flask
from utils import scrape_functions as sf

from flask import render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField,  SubmitField
import gensim

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    train_label = 'No text here'
    train = TextField(train_label, validators=[validators.required()])
class SearchForm(Form):    
    search_label = 'No text here'
    search = TextField(search_label, validators=[validators.required()])
class Five_w2v_words(Form):
    
    words=[]
    label = 'No word here.\n'
    for i in range(0,5,1):
        words.append(label)
    # def assign(self,v_words):
    #     for i in range(0,len(result),1):
    #         result[i] = v_words[i]

 
@app.route("/", methods=['POST','GET'])
def hello():
    # Init
    form = ReusableForm(request.form)
    form.train_label = 'Word to train with: '
    print form.errors
    search = SearchForm(request.form)
    search.search_label = 'Word to search: '
    w2v = Five_w2v_words(request.form)
    
    print "Request method:",request.method

    if request.method == 'POST':
        if request.form['submit'] == 'Train':
            train_word=request.form['train']
            print "train with", train_word,
        
            if form.validate():
                # Save the comment here.

                documents, words = sf.train(train_word.lower(),sf.stopwords_sv)
                # build vocabulary and train model
                model = gensim.models.Word2Vec(
                    documents,
                    size=150,
                    window=20,
                    min_count=2,
                    workers=4,
                    sg=0)

                model.train(documents, total_examples=len(documents), epochs=10)
                model.save('train.model')

                flash('Trained a model with the word: ' + train_word.lower())
            else:
                flash('All the form fields are required. ')
            

        if request.form['submit'] == 'Search':
            
            search_word=request.form['search']
            print "Search with", search_word,
        
            if search.validate():
                # Save the comment here.
                model = gensim.models.word2vec.Word2Vec.load('train.model')
                #flash('Word2Vec with the word: ' + sf.get_similar(search_word, model))
                result = sf.get_similar(search_word, model)
                for i in range(0,len(result),1):
                    w2v.words[i] = result[i]


            else:
                flash('All the form fields are required. ')


    return render_template('test.html', form=form, search=search, w2v=w2v)


# Run the app add port=# if you want to run on a different port than 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0')
