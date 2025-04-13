




import streamlit as st
import pandas as pd
import base64
import time
import datetime
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io
from streamlit_tags import st_tags
from PIL import Image
from Courses import ds_course, web_course, android_course, ios_course, uiux_course
import os
import random
import nltk
import spacy
from pyresparser.resume_parser import ResumeParser


nltk.download('stopwords')
os.environ["PAFY_BACKEND"] = "internal"


def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    rec_course = []
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for c, (c_name, c_link) in enumerate(course_list[:no_of_reco], start=1):
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
    return rec_course


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon='./Logo/logo2.png',
)


def run():
    img = Image.open('./Logo/logo2.png')
    st.image(img)
    st.title("AI Resume Analyser")
    st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume, and get smart recommendations</h5>''',
                unsafe_allow_html=True)

    pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
    if pdf_file is not None:
        with st.spinner('Uploading your Resume...'):
            time.sleep(4)
        save_image_path = './Uploaded_Resumes/' + pdf_file.name
        with open(save_image_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        show_pdf(save_image_path)
        ResumeParser.nlp = spacy.load("en_core_web_sm")

        resume_data = ResumeParser(save_image_path).get_extracted_data()
        if resume_data:
            resume_text = pdf_reader(save_image_path)

            st.header("**Resume Analysis**")
            st.success("Hello " + resume_data['name'])
            st.subheader("**Your Basic info**")
            try:
                st.text('Name: ' + resume_data['name'])
                st.text('Email: ' + resume_data['email'])
                st.text('Contact: ' + resume_data['mobile_number'])
                st.text('Resume pages: ' + str(resume_data['no_of_pages']))
            except:
                pass

            cand_level = ''
            if resume_data['no_of_pages'] == 1:
                cand_level = "Fresher"
                st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''', unsafe_allow_html=True)
            elif resume_data['no_of_pages'] == 2:
                cand_level = "Intermediate"
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''', unsafe_allow_html=True)
            elif resume_data['no_of_pages'] >= 3:
                cand_level = "Experienced"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''', unsafe_allow_html=True)

            keywords = st_tags(label='### Your Current Skills',
                               text='See our skills recommendation below',
                               value=resume_data['skills'], key='1')

            ds_keyword = ['tensorflow', 'keras', 'pytorch', 'machine learning', 'deep Learning', 'flask', 'streamlit']
            web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                           'javascript', 'angular js', 'c#', 'flask']
            android_keyword = ['android', 'android development', 'flutter', 'kotlin', 'xml', 'kivy']
            ios_keyword = ['ios', 'ios development', 'swift', 'cocoa', 'cocoa touch', 'xcode']
            uiux_keyword = ['ux', 'adobe xd', 'figma', 'zeplin', 'balsamiq', 'ui', 'prototyping', 'wireframes', 'storyframes',
                            'adobe photoshop', 'photoshop', 'editing', 'adobe illustrator', 'illustrator',
                            'adobe after effects', 'after effects', 'adobe premier pro', 'premier pro', 'adobe indesign',
                            'indesign', 'wireframe', 'solid', 'grasp', 'user research', 'user experience']

            recommended_skills = []
            reco_field = ''
            rec_course = ''

            for i in resume_data['skills']:
                if i.lower() in ds_keyword:
                    reco_field = 'Data Science'
                    st.success("** Our analysis says you are looking for Data Science Jobs.**")
                    recommended_skills = ['Data Visualization', 'Predictive Analysis', 'Statistical Modeling', 'Data Mining',
                                          'Clustering & Classification', 'Data Analytics', 'Quantitative Analysis',
                                          'Web Scraping', 'ML Algorithms', 'Keras', 'Pytorch', 'Probability',
                                          'Scikit-learn', 'Tensorflow', "Flask", 'Streamlit']
                    st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System', value=recommended_skills, key='2')
                    rec_course = course_recommender(ds_course)
                    break
                elif i.lower() in web_keyword:
                    reco_field = 'Web Development'
                    st.success("** Our analysis says you are looking for Web Development Jobs **")
                    recommended_skills = ['React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 'Magento',
                                          'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK']
                    st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System', value=recommended_skills, key='3')
                    rec_course = course_recommender(web_course)
                    break
                elif i.lower() in android_keyword:
                    reco_field = 'Android Development'
                    st.success("** Our analysis says you are looking for Android App Development Jobs **")
                    recommended_skills = ['Android', 'Android development', 'Flutter', 'Kotlin', 'XML', 'Java', 'Kivy',
                                          'GIT', 'SDK', 'SQLite']
                    st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System', value=recommended_skills, key='4')
                    rec_course = course_recommender(android_course)
                    break
                elif i.lower() in ios_keyword:
                    reco_field = 'IOS Development'
                    st.success("** Our analysis says you are looking for IOS App Development Jobs **")
                    recommended_skills = ['IOS', 'IOS Development', 'Swift', 'Cocoa', 'Cocoa Touch', 'Xcode',
                                          'Objective-C', 'SQLite', 'Plist', 'StoreKit', "UI-Kit", 'AV Foundation',
                                          'Auto-Layout']
                    st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System', value=recommended_skills, key='5')
                    rec_course = course_recommender(ios_course)
                    break
                elif i.lower() in uiux_keyword:
                    reco_field = 'UI-UX Development'
                    st.success("** Our analysis says you are looking for UI-UX Development Jobs **")
                    recommended_skills = ['UI', 'User Experience', 'Adobe XD', 'Figma', 'Zeplin', 'Balsamiq',
                                          'Prototyping', 'Wireframes', 'Storyframes', 'Adobe Photoshop', 'Editing',
                                          'Illustrator', 'After Effects', 'Premier Pro', 'Indesign', 'Wireframe', 'Solid',
                                          'Grasp', 'User Research']
                    st_tags(label='### Recommended skills for you.',
                            text='Recommended skills generated from System', value=recommended_skills, key='6')
                    rec_course = course_recommender(uiux_course)
                    break

            st.subheader("**Resume Tips & Ideas💡**")
            resume_score = 0
            if 'Objective' in resume_text:
                resume_score += 20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h4>''',
                            unsafe_allow_html=True)
            if 'Declaration' in resume_text:
                resume_score += 20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Declaration</h4>''',
                            unsafe_allow_html=True)
            if 'Hobbies' in resume_text or 'Interests' in resume_text:
                resume_score += 20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies</h4>''',
                            unsafe_allow_html=True)
            if 'Achievements' in resume_text:
                resume_score += 20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',
                            unsafe_allow_html=True)
            if 'Projects' in resume_text:
                resume_score += 20
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',
                            unsafe_allow_html=True)

            st.subheader("**Resume Score📝**")
            my_bar = st.progress(0)
            for percent_complete in range(resume_score):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1)
            st.success('** Your Resume Writing Score: ' + str(resume_score) + '**')
            st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
        else:
            st.error('Something went wrong..')


run()
