from flask import Flask
from utils import scrape_functions as sf

from flask import render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField,  SubmitField
import gensim

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import numpy as np

from sklearn.decomposition import PCA

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

model = gensim.models.word2vec.Word2Vec.load('sv_blogposts_10M_minc10_win10_size300')
data = []


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

@app.route('/showMultiChart')
def multiLine():
    global data
    print 'Length', len(data)
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('test1.html',
                           graphJSON=graphJSON)

@app.route("/", methods=['POST','GET'])
def hello():
    global data, graphEnable
    # Init
    form = ReusableForm(request.form)
    form.train_label = 'Word to train with: '
    print form.errors
    search = SearchForm(request.form)
    search.search_label = 'Word to search: '
    w2v = Five_w2v_words(request.form)

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    print "Request method:",request.method

    if request.method == 'POST':
        # One of the buttons
        if request.form['submit'] == 'Train':
            train_word=request.form['train']
            print "train with", train_word,
        
            if form.validate():
                # Split between all the words we have to perform
                # twitter scrapying with.
                tweeter_words = train_word.split(',')

                # Just a vector that contains all the info
                class_search = []
                X = []
                data = []
                for word in tweeter_words:
                    # Harvest the tweets
                    sentences = sf.harvest_sentences(word)
                    # Get a sent2vect transformation
                    vectors = sf.sent2vect(sentences,model)
                    # Save the results
                    class_search.append([word,sentences,vectors])
                    X.extend(vectors)
                # Debug output, should remove
                print "Total fetched words : ", len(class_search)

                # Perform PCA
                pca = PCA(n_components=3)
                pca.fit(X)
                
                # For plotting the results
                data = []
                for index in range(0,len(class_search),1):
                    local_vectors = np.array(pca.transform(class_search[index][2]))
                    print 'local_vectors for ', class_search[index][0],
                    print ' is ', len(local_vectors[:,0]), ' shape is: ',
                    print local_vectors.shape
                    data.append(
                        go.Scatter(
                            x=local_vectors[:,0], # The vectors inside
                            y=local_vectors[:,1], # The second dim of the vector
                            # z=local_vectors[:,2], # The second dim of the vector
                            mode='markers',
                            text=class_search[index][0].encode('utf-8'),
                            name=class_search[index][0].encode('utf-8')
                        )
                        # go.Histogram(
                        #     x=local_vectors[:,0], # The vectors inside
                        #     text=class_search[index][0].encode('utf-8'),
                        #     name=class_search[index][0].encode('utf-8')
                        # )
                    )
                print "Total scatter plots : ", len(data)

                graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

                # flash('Trained a model with the word: ' + train_word.lower())

            else:
                flash('All the form fields are required. ')
        # The other button
        if request.form['submit'] == 'Search':
            
            search_word=request.form['search']
            print "Search with", search_word,
        
            if search.validate():
                #flash('Word2Vec with the word: ' + sf.get_similar(search_word, model))
                result = sf.get_similar(search_word, model)
                for i in range(0,len(result),1):
                    w2v.words[i] = result[i]


            else:
                flash('All the form fields are required. ')


    return render_template('test.html', form=form, search=search, w2v=w2v, graphJSON=graphJSON)


# Run the app add port=# if you want to run on a different port than 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0')
