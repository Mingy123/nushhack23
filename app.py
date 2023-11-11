from flask import Flask, request, send_file, abort, jsonify
import random, string, rendertext, parsevideo

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

def refresh_tags(packageID):
  if packageID not in packages: return
  diffs, tags = [], set()
  for key, val in lessons:
    if val['package'] != packageID: continue
    lec = val['lecture']
    diffs.append(lec['difficulty'])
    tags.add(lec['tags'])
  packages[packageID]['difficulty'] = sum(diffs)//len(diffs)
  packages[packageID]['tags'] = list(tags)

packages = {
  'testing': {
    'title': 'doing math with friends',
    'lessons': ['someID', 'someOtherID'],
    'tags': ['math', 'calculus'],
    'difficulty': 50
  }
}

lessons = {
  'someID': {
    'title': 'math 1',
    'package': 'testing',
    'lecture': {
      'difficulty': 50,
      'tags': ['math', 'calculus'],
      'url': '/static/lectures/division.mp4'
    },
    'quiz': [{'question': 'What  is 1 + 1?', 'options': ['1', '2', '3', '4'], 'answer': 1}]
  },
  'someOtherID': {
    'title': 'math 2',
    'package': 'testing',
    'lecture': {
      'difficulty': 50,
      'tags': ['math', 'calculus'],
      'url': '/static/lectures/division.mp4'
    },
    'quiz': [{'question': 'What  is 2 + 1?', 'options': ['1', '2', '3', '4'], 'answer': 2}]
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
  packages[packID] = {
    'title': request.get_json().get('title'),
    'lessons': [],
    'tags': [],
    'difficulty': 50
  }
  return packID

@app.route('/create-lesson', methods=['POST'])
def create_lesson():
  data = request.get_json()
  packID = data.get('id')
  if packID not in packages:
    abort(404)
  lessonID = random_string(16)
  lessons[lessonID] = {
    'title': data.get('title'),
    'package': packID,
    'lecture': {
      'difficulty': 50,
      'tags': [],
      'url': ''
    },
    'quiz': []
  }
  return lessonID


@app.route('/get-packages')
def get_packages():
  return packages

@app.route('/get-lessons')
def get_lessons():
  return lessons


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
  if not lsn: abort(404)
  if 'file' not in request.files: abort(400)
  file = request.files['file']
  if file.filename == '': abort(400)
  name, ext = split_filename(file.filename)
  filename = random_string(16) + '.' + ext
  if ext == '': filename = filename[:-1]
  path = './static/lectures/'+filename
  file.save(path)
  diff, tags = parsevideo.render(path)
  lec = lsn['lecture']
  lec['difficulty'] = diff
  lec['url'] = path
  lec['tags'] = tags
  refresh_tags(lsn['package'])
  return 'success'

@app.route('/set-info')
def set_lecture_info():
  data = request.get_json()
  lessonID = data.get('id')
  lsn = lessons.get(lessonID)
  if not lsn: abort(404)
  lec = lsn['lecture']
  lec['difficulty'] = data.get('difficulty')
  lec['tags'] = data.get('tags')
  refresh_tags(lsn['package'])
  return 'success'


@app.route('/nicetify', methods=['POST'])
def nicetify():
  if 'file' not in request.files: abort(400)
  file = request.files['file']
  if file.filename == '': abort(400)
  name, ext = split_filename(file.filename)
  fileID = random_string(16)
  path = './static/nicetify/' + fileID + '.' + ext
  if ext == '': path = path[:-1]
  file.save(path)
  image = rendertext.read(path)
  path = './static/nicetify/' + fileID + '_out.' + ext
  if ext == '': path = path[:-1]
  image.save(path)
  return path[1:]



app.run(host='0.0.0.0')