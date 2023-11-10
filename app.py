from flask import Flask, request, send_file, abort, jsonify
import random, string, rendertext

app = Flask(__name__)

RNG_CHARS = string.ascii_letters + string.digits
def random_string(length):
  ans = ''
  for i in range(length):
    ans += random.choice(RNG_CHARS)
  return ans

def split_filename(filename):
  spl = filename.split('.')
  if len(spl) == 1: return filename, ''
  return spl[0], '.'.join(spl[1:])

packages = {
  'testing': {
    'title': 'doing math with friends',
    'lessons': ['someID', 'someOtherID'],
    'tags': ['math', 'calculus'],
    'difficulty': 8
  }
}

lessons = {
  'someID': {
    'title': 'math 1',
    'package': 'testing',
    'lecture': 'videoID',
    'quiz': [{'question': 'What  is 1 + 1?', 'options': ['1', '2', '3', '4'], 'answer': '2'}]
  },
  'someOtherID': {
    'title': 'math 2',
    'package': 'testing',
    'lecture': 'videoID',
    'quiz': [{'question': 'What  is 2 + 1?', 'options': ['1', '2', '3', '4'], 'answer': '3'}]
  }
}


@app.route('/package')
def get_package():
  item = packages.get(request.args.get('id'))
  if not item: abort(404)
  return item

@app.route('/lesson')
def get_lesson():
  item = lessons.get(request.args.get('id'))
  if not item: abort(404)
  return item



@app.route('/create-package', methods=['POST'])
def create_package():
  packID = random_string(16)
  packages[packID] = []
  return packID

@app.route('/create-lesson', methods=['POST'])
def create_lesson():
  data = request.get_json()
  packID = data.get('id')
  if packID not in packages:
    abort(404)
  lessonID = random_string(16)
  lessons[lessonID] = {
    'package': packID,
    'lecture': '',
    'quiz': []
  }
  return lessonID



@app.route('/add-quiz', methods=['POST'])
def add_quiz():
  data = request.get_json()
  lessonID = data.get('id')
  lsn = lessons.get(lessonID)
  qn = data.get('question')
  opt = data.get('options')
  ans = data.get('answer')
  if not lsn: abort(404)
  if not (qn and opt and ans): abort(400) # missing data
  lsn['quiz'].append({
    'question': qn,
    'options': opt,
    'answer': ans
  })
  return 'success'

@app.route('/add-lecture', methods=['POST'])
def add_lecture():
  lessonID = request.form.get('id')
  lsn = lessons.get(lessonID)
  if 'file' not in request.files: abort(400)
  file = request.files['file']
  if file.filename == '': abort(400)
  name, ext = split_filename(file.filename)
  filename = random_string(16) + '.' + ext
  file.save('./static/lectures/'+filename)
  return 'success'



@app.route('/nicetify', methods=['POST'])
def nicetify():
  if 'file' not in request.files: abort(400)
  file = request.files['file']
  if file.filename == '': abort(400)
  name, ext = split_filename(file.filename)
  fileID = random_string(16)
  path = './static/nicetify/' + fileID + '.' + ext
  file.save(path)
  image = rendertext.read(path)
  path = './static/nicetify/' + fileID + '_out.' + ext
  image.save(path)
  return path[1:]



app.run(host='0.0.0.0')