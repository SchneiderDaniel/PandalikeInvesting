from bs4 import BeautifulSoup
import urllib, re

WPM = 200
WORD_LENGTH = 5


def count_words_in_text(text_list, word_length):
	total_words = 0
	for current_text in text_list:
		total_words += len(current_text)/word_length
	return total_words

# 3
def estimate_reading_time(text_list):
	total_words = count_words_in_text(text_list, WORD_LENGTH)
	return total_words/WPM


def extract_text(text):
	
	soup = BeautifulSoup(text, 'html.parser')
	texts = soup.findAll(text=True)

	result =''

	for text in texts:
		result +=text
	return result