# Import necessary modules
import os
import pandas as pd
import numpy as np
import streamlit as st

from transformers import pipeline
from fuzzywuzzy import process

from utils import open_webpage

# Get the directory where the current Python file resides, used for referencing relative paths
base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, 'data')

# Load the dataset
course_specs = pd.read_csv(os.path.join(data_path, 'course_specifications.csv'))
courses = pd.read_csv(os.path.join(data_path, 'courses.csv'))
entry_by_country = pd.read_csv(os.path.join(data_path, 'entry_requirements_country.csv'))
tariff = pd.read_csv(os.path.join(data_path, 'tariff_points.csv'))

# Load the model
model_name = "IProject-10/bert-base-uncased-finetuned-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)



full_names = pd.merge(courses[['url', 'full_title']], course_specs[['url', 'title']], on='url', how='outer')
full_names = full_names[full_names.url.notnull()][['url', 'title']].set_index('url').to_dict()['title']

courses['full_title'] = courses['url'].map(full_names)

#Page Setup
st.set_page_config(
   page_title="Admission Clearing",
   page_icon=":school:",
   layout="wide",
)



tool_tab, llm_tab = st.tabs(["⚙️ &nbsp; Admission Tool", "🤖 &nbsp; Chat with LLM"])


with tool_tab:
  st.markdown("<br>", unsafe_allow_html=True)
  
  # ---------------------------- Country Specific Entry Requirements ----------------------------
  st.subheader("Country Specific Entry Requirements", divider="red")
  col1, col2 = st.columns([4, 1])
  col2.markdown("<br>", unsafe_allow_html=True)
  col2.button("🌏 &nbsp; Access Full List", on_click=open_webpage, args=("https://www.londonmet.ac.uk/international/applying/entry-requirements-by-country/",), type="secondary")
  country_choice = col1.selectbox("Country of Origin", entry_by_country.country.unique(), index=None, placeholder="Select a country ...")



  if country_choice:
    with st.container():
      st.markdown("<br><br>", unsafe_allow_html=True)
      col1, col2 = st.columns([4, 1])
      col1.markdown( f"#### {country_choice}", unsafe_allow_html=True)
      filtered_country = entry_by_country[entry_by_country['country'] == country_choice]
      col2.button("🌐 &nbsp; Open London Met Website", on_click=open_webpage, args=(filtered_country['url'].values[0],), type="secondary")
      
      st.markdown("<h5>Academic entry requirements</h5>", unsafe_allow_html=True)
      st.markdown(filtered_country['academic'].values[0].replace('h3', 'h6'), unsafe_allow_html=True)
      
      st.markdown("<br>", unsafe_allow_html=True)
      st.markdown("<h5>Mathematics and English requirements</h5>", unsafe_allow_html=True)
      st.markdown(filtered_country['mathematics and english'].values[0].replace('h3', 'h6'), unsafe_allow_html=True)

  st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)






  # ---------------------------- UCAS Point Calculator ----------------------------

  st.subheader("UCAS Point Calculator", divider="red")
  col1, col2, col3 = st.columns([3, 1, 1])


  qualification = col1.selectbox("Qualification Title", tariff['Qualification Title'].unique(), index=None, placeholder="Select a qualification ...")
  row_count = col2.number_input("Number of Qualifications", min_value=1, max_value=10, value=3, step=1)

  col3.markdown("<br>", unsafe_allow_html=True)
  col3.button("🧮 &nbsp; Access Full UCAS Calculator", on_click=open_webpage, args=("https://www.ucas.com/undergraduate/applying-university/entry-requirements/calculate-your-ucas-tariff-points",), type="secondary")
  st.markdown("<br>", unsafe_allow_html=True)

  if qualification:
    filtered_tariff = tariff[tariff['Qualification Title'] == qualification]
    tariff_points_dict = dict(zip(filtered_tariff['Grade'], filtered_tariff['TARIFF POINTS']))
    
    total_points = 0
    for row in range(row_count):
      col1, col2, col3 = st.columns([2, 4, 1])
      col1.text_input("Subject (Optional)", key=f"subject_{row}", placeholder="Type a subject ...")
      value = col2.radio(f"Qualification {row+1}", tariff_points_dict.keys(), key=row, horizontal=True, index=None)
      if value:
        col3.markdown("<br>", unsafe_allow_html=True)
        value = tariff_points_dict[value]
        col3.markdown(f"Points obtained : <strong>{value}</strong>", unsafe_allow_html=True)
        total_points += value
      
      st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    col1.markdown("<br>", unsafe_allow_html=True)
    col1.markdown("<strong>Total points</strong>", unsafe_allow_html=True)
    col2.markdown(f"<h3><strong>{total_points}</strong></h3>", unsafe_allow_html=True)

  st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)






  # ---------------------------- Course and specifications ----------------------------

  st.subheader("Course and specifications", divider="red")

  with open(os.path.join(data_path, 'scrapper_info.txt')) as f:
    data = f.readlines()
    col1, col2 = st.columns([2, 1])
    col1.caption(data[0] + ' ' + data[1])
    col2.caption(data[2])
  st.markdown("<br>", unsafe_allow_html=True)


  col1, col2 = st.columns([2, 1])
  filter_course_type = col1.radio("Filter by course type",  courses['type'].unique(), horizontal=True, index=None)
  filter_available_courses = col2.toggle("Filter only available courses", True)

  if filter_course_type: courses = courses[courses['type'] == filter_course_type]
  if filter_available_courses:courses = courses[courses['url'].notnull()]
  choice = st.selectbox("Course Title", courses['full_title'], index=None, placeholder="Select a course name ...")
  st.markdown("<br>", unsafe_allow_html=True)

  if choice:
    with st.container():
      st.markdown( f"#### {choice}", unsafe_allow_html=True)
      deep_filtered_course = courses[courses['full_title'] == choice]
      
      col1, col2 = st.columns([2, 1])
      with col1:
        st.markdown("Course Code : <strong>" + deep_filtered_course['course_code'].values[0] + "</strong>", unsafe_allow_html=True)
        st.markdown("Type : <strong>" + deep_filtered_course['type'].values[0] + "</strong>", unsafe_allow_html=True)
      
      url = deep_filtered_course['url'].values[0]
      if type(url) == str:
        with col2:
          st.button("👁️ &nbsp; View Full Specifications", on_click=open_webpage, args=(url,), type="secondary")
      
        filtered_specs = course_specs[course_specs['url'] == url]
        
        
        entry_requirements = filtered_specs['entry_requirements'].values[0].replace("h4", "h5").replace("<h5>", "<br/><h5 style='color: #878787;'>")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h5>Entry Requirements</h5>", unsafe_allow_html=True)
        st.markdown(entry_requirements, unsafe_allow_html=True)
        
        course_requirements = filtered_specs['course_requirements'].values[0].replace("<table ", "<table style='width:100%;' ")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h5>Course Specifications</h5>", unsafe_allow_html=True)
        st.markdown(course_requirements, unsafe_allow_html=True)






with llm_tab:
  testing_value = """If the entry requirements for BSc (Hons) Business Management are 112 points and GCSE grade C/4 in English and Mathematics, an applicant must meet or exceed these requirements in order to be offered a place 
If an applicant submitted an application with 3 A Level results, achieving grade B in each subject"""
  
  st.markdown("<br>", unsafe_allow_html=True)
  application_context = st.text_area("Application Details", value=testing_value, placeholder="Type the application details ...")
  
  course_from_nlp = nlp({
    'question': 'Which course did the applicant apply for?',
    'context': application_context
  })
  
  available_courses = courses[courses['full_title'].str.contains(course_from_nlp['answer'])]

  exact_match = None
  if available_courses.empty:
      closest_match = process.extract(course_from_nlp['answer'], courses['full_title'], scorer=process.fuzz.token_sort_ratio, limit=8)
      
      if len(closest_match) > 0:
          st.warning(f"🤖 &nbsp; Closest matches found for {course_from_nlp['answer']}")
          course_choice = st.radio("Select one of the following course", [match[0] for match in closest_match], index=None)
          
          if course_choice:
              exact_match = courses[courses['full_title'] == course_choice]
      else:
          st.danger('🤖 &nbsp; No course found')
  else:
      exact_match = available_courses
      st.info(f"🤖 &nbsp; Exact Course found : {course_from_nlp['answer']}")
    
  if exact_match is not None:
    st.warning(":construction: &nbsp; Need a GPU to use other services (question answering using Llama model) ...")