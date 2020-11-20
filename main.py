import streamlit as st

from gensim.summarization import summarize

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import spacy
from spacy import displacy


from bs4 import BeautifulSoup
from urllib.request import urlopen

import spacy_streamlit

from textblob import TextBlob    

from wordcloud import WordCloud
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


st.set_option('deprecation.showPyplotGlobalUse', False)










HTML_WRAPPER= """<div style="overflow-x:x auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding 1rem">{}</div>"""

# def get_color_styles(color: str) -> str:
#     """Compile some hacky CSS to override the theme color."""
#     # fmt: off
#     color_selectors = ["a", "a:hover", "*:not(textarea).st-ex:hover", ".st-en:hover"]
#     bg_selectors = [".st-da", "*:not(button).st-en:hover"]
#     border_selectors = [".st-ft", ".st-fs", ".st-fr", ".st-fq", ".st-ex:hover", ".st-en:hover"]
#     # fmt: on
#     css_root = "#root { --primary: %s }" % color
#     css_color = ", ".join(color_selectors) + "{ color: %s !important }" % color
#     css_bg = ", ".join(bg_selectors) + "{ background-color: %s !important }" % color
#     css_border = ", ".join(border_selectors) + "{ border-color: %s !important }" % color
#     other = ".decoration { background: %s !important }" % color
#     return f"<style>{css_root}{css_color}{css_bg}{css_border}{other}</style>"


# st.write(get_color_styles("#09A3D5"), unsafe_allow_html=True)
# nlp=spacy.load('en_core_web_sm')


def get_text(raw_url):
	page= urlopen(raw_url)
	soup= BeautifulSoup(page)
	fetched_text= ' '.join(map(lambda p:p.text, soup.find_all('p')))
	return fetched_text








def sumy_summarizer(docx):
	parser= PlaintextParser.from_string(docx, Tokenizer('english'))
	lex_summarizer= LexRankSummarizer()
	summary= lex_summarizer(parser.document,3)
	summary_list= [str(sentence) for sentence in summary]
	result= ''.join(summary_list)
	return result



# @st.cache(allow_output_mutation=True)
# def analyze_text(text):
# 	return nlp(text)





def main():
	#summary entity checker




	st.title('Analyze and Summarize your Text')
	image= Image.open("img2.jpg")

	st.image(image, use_column_width=True)

	#activities = ['Summarize', 'NER checker', 'NER for URL']
	# activities = ['Summarize', 'NER checker', 'Sentiment Analyzer', 'Word Cloud']
	# choice= st.sidebar.selectbox('Select Activity', activities)

	# raw_text= st.text_area('Enter text here', 'Type Here')
	# st.checkbox('Summarize')
	# st.checkbox('NER checker')
	# st.checkbox('Sentiment Analyzer')
	# st.checkbox('Word Cloud')


	if st.checkbox('Summarize'):
		st.subheader('Summarize your text using Natural Language Processing')
		raw_text= st.text_area('Enter text to summarize:', 'Paste Here')
		summary_choice = st.selectbox('Summary Choice', ['Summary model (Gensim)', 'Summary model (Sumy)'])
		if st.button('Summarize'):
			if summary_choice == 'Summary model (Gensim)':
				summary_result= summarize(raw_text)
			elif summary_choice == 'Summary model (Sumy)':
				summary_result= sumy_summarizer(raw_text)
			st.write(summary_result)

	if st.checkbox('Named Entity Recognition'):
		st.subheader('Entity Recognition')
		raw_text= st.text_area('Enter text to identify labels: ', 'Paste Here')
		if st.button('Scan'):
			docx= nlp(raw_text)
			spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe('ner').labels)

			# docx= nlp(raw_text)
			# html= displacy.render(docx, style= 'ent')
			# html= html.replace('\n\n', '\n')
			# st.write(html, unsafe_allow_html=True)
			# st.markdown(html, unsafe_allow_html=True)



		# st.subheader('Entity Recognition with Spacy')
		# raw_text= st.text_area('Enter text here', 'Type Here')
		# docx= nlp(raw_text)
		# spacy_streamlit.visualize_ner(docx, labels=nlp.get_pipe('ner').labels)

	# if choice == 'NER for URL':
	# 	st.subheader('Analyze text from URL')
	# 	raw_url= st.text_input('Enter URL', 'Type here')
	# 	text_length= st.slider('Length to preview', 50,100)
	# 	if st.button('Extract'):
	# 		if raw_url != 'Type here':
	# 			result = get_text(raw_url)
	# 			len_of_full_text= len(result)
	# 			len_of_short_text= round(len(result)/text_length)
	# 			st.info('Length:: Full Text::{}'.format(len_of_full_text))
	# 			st.info('Length:: Short Text::{}'.format(len_of_short_text))
	# 			st.write(result[:len_of_short_text])
	# 			summary_docx= sumy_summarizer(result)
	# 			docx= nlp(summary_docx)
	# 			html= displacy.render(docx, style= 'ent')
	# 			html= html.replace('\n\n', '\n')
	# 			st.write(html, unsafe_allow_html=True)
	# 			# st.markdown(html, unsafe_allow_html=True)

	if st.checkbox('Sentiment Analyzer'):
		st.subheader('Sentiment analysis')
		message= st.text_area('Enter text for sentiment analysis: ', 'Paste Here')
		if st.button('Analyze'):
			blob = TextBlob(message)
			result_sentiment= blob.sentiment
			st.success(result_sentiment)
			# st.bar_chart(result_sentiment)
			
	if st.checkbox('Word Cloud'):
		st.subheader('Word Cloud of your text')
		message= st.text_area('Enter text to create word cloud: ', 'Paste here')
		if st.button('Create Cloud'):
			wordcloud= WordCloud().generate(message)
			plt.imshow(wordcloud, interpolation='bilinear')
			plt.xticks([])
			plt.yticks([])
			st.pyplot()


if __name__ == '__main__':
	main()