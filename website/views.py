from sqlite3 import IntegrityError
from flask import Flask, render_template, request, redirect, url_for, make_response, Blueprint

from website.sbcCalculator import findRatingsAndPrice

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/', methods = ['POST'])
def output_ratings():
    data = request.form
    try:
        rating_list = data['ratingList'].split(",")
        new_rating_list = []
        for i in rating_list:
            curr_int = int(i.strip())
            if curr_int < 47 or curr_int > 99:
                return render_template('index.html')
            new_rating_list.append(curr_int)

        # rating_list = [int(i.strip()) for i in rating_list]
        
        target_rating = int(data['targetRating'])
        min_rating = int(data['minRating'])        
        max_rating = int(data['maxRating'])  
        df = findRatingsAndPrice(new_rating_list, target_rating, min_rating, max_rating)
        return render_template('output.html',  tables=[df.to_html(classes='table table-striped text-center', justify='center', index = False)])
    except:
        return render_template('index.html')
