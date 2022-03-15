from flask import Flask, request, jsonify
from sqlalchemy.engine import result
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os


# Initialize app
app = Flask(__name__)

CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))


# Database Configurations + Path
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'anzscoDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# attaching SqlAlchemy and Marshmallow with this App
db = SQLAlchemy(app)
ma = Marshmallow(app)


# creatiing Model class for DB table structure

# First page table
class anzsco(db.Model):
    __tablename__ = 'anzsco'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anzsco_url = db.Column(db.Text)
    authority = db.Column(db.Text)
    employer_sponsership = db.Column(db.Text)
    indep_and_family_sponsered = db.Column(db.Text)
    state_nomination = db.Column(db.Text)
    mltssl_stsol = db.Column(db.Text)
    caveat = db.Column(db.Text)


# Second page table
class anzsco_sec(db.Model):
    __tablename__ = 'anzsco_sec'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    head1 = db.Column(db.Text)
    description = db.Column(db.Text)
    skill_level = db.Column(db.Integer)
    alternative_titles = db.Column(db.Text)
    specialisations = db.Column(db.Text)
    skills_assess_authority = db.Column(db.Text)
    caveats = db.Column(db.Text)
    asco_occupations = db.Column(db.Text)
    head2 = db.Column(db.Text)
    more_description = db.Column(db.Text)
    tasks = db.Column(db.Text)
    skill_level_desc = db.Column(db.Text)
    occupations_in_this_group = db.Column(db.Text)


# creating schema class for ORM Mapping
class anzscoSchema(ma.Schema):

    class Meta:
        fields = ('id', 'anzsco_url', 'authority', 'employer_sponsership', 'indep_and_family_sponsered', 'state_nomination',
                  'mltssl_stsol', 'caveat')


class anzscoSecSchema(ma.Schema):
    class Meta:
        fields = ('id', 'head1', 'description', 'skill_level', 'alternative_titles', 'specialisations', 'skills_assess_authority',
                  'caveats', 'asco_occupations', 'head2', 'more_description', 'tasks', 'skill_level_desc', 'occupations_in_this_group')


# Delete database file if it exists currently
# if os.path.exists('anzscoDB'):
#     os.remove('anzscoDB')

anzsco_schema = anzscoSchema(many=True)
anzsco_sec_schema = anzscoSecSchema(many=True)

# for i in anzsco.select().execute():
#     print(i)

# db.create_all()

# API for fetching all data from First page
@app.route('/anzsco', methods=['GET'])
def getAllFirstData():
    all_tb1_data = anzsco.query.order_by(anzsco.id).all()
    result = anzsco_schema.dump(all_tb1_data)
    return jsonify(result)


# API for fetching all + single data from second page
@app.route('/anzsco_sec', methods=['GET'])
def getAllSecData():
    all_tb2_data = 0
    heading = request.args.get("heading")
    if heading:
        all_tb2_data = anzsco_sec.query.filter(
            anzsco_sec.head1.like(f'%{heading}%'))
    else:

        all_tb2_data = anzsco_sec.query.order_by(anzsco_sec.id).all()

    result = anzsco_sec_schema.dump(all_tb2_data)
    return jsonify(result)


# API for default request
@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'hello World'})


# Run server
if __name__ == '__main__':
    app.run(debug=True)


os.close()
