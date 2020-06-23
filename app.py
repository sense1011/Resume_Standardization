import streamlit as st
import os
import spacy
import docx2txt
from spacy import displacy 

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from io import StringIO

custom_nlp = spacy.load("ner_ds_model")

st.title("Resume Standardiztion")

st.header("Upload Resume")

def extract_text_from_pdf(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # removed from the line above: , codec=codec
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    return data

def extract_text_from_doc(data):

    temp = docx2txt.process(data)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

def resumeConvertor(resumename):
    with open('resumeconverted.txt','w') as f:
    	if(resumename.endswith(".pdf")):
    		f.write(extract_text_from_pdf(resumename))
    	if(resumename.endswith(".docx")):
    		f.write(extract_text_from_doc(resumename))

    with open('resumeconverted.txt','r') as f:
        resume = f.read()
    return resume

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    if filenames is not None:
        selected_filename = st.selectbox('Select a file', filenames)
        return os.path.join(folder_path, selected_filename)

    else:
        st.write("Upload! Failed")

resumename = file_selector()

if resumename is not None:
    st.write('You selected `%s`' % resumename)

if st.checkbox('Show Resume'):
    st.write(resumeConvertor(resumename))

st.header("Parse Resume")

if st.checkbox('Parse Resume'):
	doc = custom_nlp(resumeConvertor(resumename))
	st.write(doc.ents)