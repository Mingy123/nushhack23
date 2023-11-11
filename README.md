# Nicetify

# Installation

`git submodule update --init --recursive`

## Inspiration
Students around the world face learning disabilities such as ADHD and dyslexia, without sufficient resources for their education, thus leaving them behind in our traditional education system. With Nicetify's service, students will be more connected with specialized mentors along with specialized learning materials and a tailored learning process.

## What it does
Nicetify mainly features a gamified Learning Management System where students can access a vast library of learning materials from a robust recommendation system which takes into account their recent activity and interests, so as to maintain their involvement in their education.  
Nicetify also provides several AI powered tools for the benefit of students and mentors alike, such as an OCR program which converts learning materials into a more dyslexia-friendly format by manipulating the font of text.

## How we built it
For the backend, we used a Flask server on Google Cloud, using many different computer vision libraries such as OpenCV and Pillow to run computations for the users. An optical character recognition model was also used to convert images into text for general use in later computations.

## Challenges we ran into
Of course, such an undertaking had many hurdles we had to overcome, both in the making of the LMS as well as the scanner. Communicating with the backend from the android app was a delicate process -- even getting the request to send was difficult in and of itself. Additionally, we had to account for the relatively long uploading, processing, and downloading times and factor it into the application so as to not interrupt the user experience. There were also a few issues in navigating some of the more obtuse parts of android's documentation; specifically in implementing the Picture-in-Picture (PIP) mode for the LMS and the live camera view for the scanner.

## What's next for Nicetify
We plan on further expanding the LMS to accommodate a sister application for teachers to submit their lessons through. Additionally, we could provide more customisability to the scanner functionality so as to better suit each and every user, perhaps through font selection (if they believe some other font is more legible for them)

## Work Distribution
Backend: Ming Hong

Frontend: CJT & Oon Han
