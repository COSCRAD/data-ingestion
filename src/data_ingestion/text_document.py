from docx import Document
import re

from data_ingestion.audio_label import AudioLabel

def parse_timestamp(text_for_timestamp):
   numeric_parts = text_for_timestamp.replace("_","").replace("[","").split(":")

   if len(numeric_parts) == 0:
      return 0.0
   
   hours, minutes, seconds = numeric_parts

   return (float(hours)*3600 + float(minutes)*60 + float(seconds))*1000  #ms


class CoscradParagraph:
   def __init__(self, text):
      self.text = text

# The timestamp_offset allows us to shift timestamps appropriately
   def emit_audio_labels(self,timestamp_offset):
      # TODO Ingect the strategy for processing labels
      delimiter_pattern = r"(_\d\d:\d\d:\d\d_)"
      search = re.split(delimiter_pattern,self.text)
      result = [] if search is None else search

      first_timestamp = timestamp_offset if timestamp_offset is not None else 0.0

      timestamps = [first_timestamp]

      labels = []

      for index,text in enumerate(result):
         if re.match(delimiter_pattern,text):
            timestamps.append(parse_timestamp(text))

      for text in result:
         if not re.match(delimiter_pattern,text) and text.replace(" ","") != "":
            index = len(labels) - 1
            labels.append(AudioLabel(in_point=timestamps[index],out_point=timestamps[index+1],text=text)) 

      return labels           

      


class TextDocument:
   def __init__(self, name):
      self.name = name

      self.paragraphs = []

   def add_paragraph(self,text):
      self.paragraphs.append(CoscradParagraph(text=text))

   def emit_audio_labels(self):
      all_labels = []
      for p in self.paragraphs:
         for l in p.emit_audio_labels(0.0):
            # TODO pass in outpoint of last previous label
            all_labels.append(l)

      return all_labels

   def from_docx(file_path, name):
      doc = TextDocument(name=name)

      docx_doc = Document(file_path)

      for p in docx_doc.paragraphs:
         doc.add_paragraph(p.text)

      return doc

