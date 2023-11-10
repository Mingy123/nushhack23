from PIL import Image
from openai import OpenAI
import cv2, easyocr, random, string

RNG_CHARS = string.ascii_letters + string.digits
def random_string(length):
  ans = ''
  for i in range(length):
    ans += random.choice(RNG_CHARS)
  return ans

def render(video_path):
    cap = cv2.VideoCapture('test.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = frames // 20

    selected = []
    num = 0
    while True:
        num += interval
        if num > frames: break
        cap.set(1, num)
        ret, frame = cap.read()
        if not ret: break # video end
        selected.append(frame)

    cap.release()
    reader = easyocr.Reader(['en'])
    path = random_string(16) + '.jpg'
    texts = []
    for i, frame in enumerate(selected):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        width, height = image.size
        if width > 400:
            height = int(height / (width / 400))
            width = 400
            image = image.resize((width, height))
        image.save(path)
        result = reader.readtext(path)
        for i in result:
            if i[2] < 0.05: continue
            texts.append(i[1])

    dump = ' '.join(texts)
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you will be given a list of words, some of which are gibberish. output the scientific technical complexity of the image as a number from 0 to 100, from 1st grade to 12th grade. Respond with strictly only the number, no matter what."},
            {'role': 'user', 'content': dump}
        ]
    )
    ans = completion.choices[0].message.content
    try:
        return int(ans)
    except:
        return 50
