from docx import Document
from data_ingestion.audio_label import AudioLabel
from pydub import AudioSegment
import re

def parse_timestamp(text_for_timestamp):
    numeric_parts = text_for_timestamp.replace("_", "").replace("[", "").replace("]","").split(":")

    if len(numeric_parts) == 0:
        return 0.0

    hours, minutes, seconds = numeric_parts

    return (float(hours) * 3600 + float(minutes) * 60 + float(seconds)) * 1000  # ms

class Transcript:
    def __init__(self, name):
        self.name = name

        self.title = None

        self.labels = []

    def append(self, label):
        self.labels.append(label)

    def __str__(self):
        return '\n'.join([l.text for l in self.labels])
    
    def __len__(self):
        return 0 if self.is_empty() else len(self.labels)
    
    def is_empty(self):
        return len(self.labels) == 0
    
    def last(self):
        return None if self.is_empty() else self.labels[-1]

    def fromTsvRows(rows, name):
        transcript = Transcript(name)

        for row in rows:
            columns = row.split("\t")

            if len(columns) != 3:
                # TODO should we return errors intead?
                raise Exception(
                    f"invalid format. expected 3 tab separated values. Received: {row}"
                )

            i, o, t = columns

            transcript.append(
                AudioLabel(in_point_ms=float(i), out_point_ms=float(o), text=t)
            )

        return transcript

    def from_docx(filepath,name,timestamp_pattern= r"(\[\d\d:\d\d:\d\d\])"):
        doc = Document(filepath)
        
        transcript = Transcript(name)

        # TODO inject a parser to support different formats?
        # first we parse the paragraphs in between time-stamps
        for p in doc.paragraphs:
            # For now, we only accept a match at the beginning of the line
            search = re.match(timestamp_pattern, p.text)

            if search is not None:
                split = re.split(timestamp_pattern,p.text,maxsplit=1)

                if split is None:
                    continue

                trimmed_split = [t for t in split if t.replace(' ','') != '']

                timestamp_text = trimmed_split[0]

                text = trimmed_split[1]

                timestamp = parse_timestamp(timestamp_text)

                new_label = AudioLabel(in_point_ms=timestamp,out_point_ms=None,text=text)

                transcript.append(new_label)
            else:
                if transcript.is_empty():
                    if(transcript.title is None):
                        # TODO Do we want the full paragraph \ runs
                        # TODO Support multi-line titles
                        transcript.title = p.text

        return transcript
    
    def from_whisper_timestamped_transcript(raw_transcript,name,threshold_confidence_inclusive=0.51):
        t = Transcript(name=name)

        for w in raw_transcript.get('segments',[]):
            in_point_s = w.get('start',None)

            out_point_s = w.get('end',None)

            text = w.get('text',None)

            has_label_data = in_point_s is not None and out_point_s is not None and text is not None

            if w.get('confidence',0.0) >= threshold_confidence_inclusive and has_label_data:
                # TODO Should we null check these props?
                l = AudioLabel(in_point_ms=in_point_s*1000,out_point_ms=out_point_s*1000,text=text)

                t.append(l)

        return t

    """
    Return a shallow clone with the given transformation applied
    """
    def map_label_text(self,transform_text):
        transformed_transcript = Transcript(self.name)

        for l in self.labels:
            new_label = AudioLabel(in_point_ms=l.in_point_ms,out_point_ms=l.out_point_ms,speaker_initials=l.speaker_initials,text=transform_text(l.text))

            transformed_transcript.append(new_label)

        return transformed_transcript

    """
    Return a shallow clone with only labels that satisfy the given predicate function
    """
    def filter(self, predicate):
        filtered_transcript = Transcript(self.name)

        # why clone if we have a side-effect on self?
        self.sort()

        delta = 0.0

        for label in self.labels:
            if predicate(label):
                # correct time stamp for missing labels
                label.shift(delta)
                filtered_transcript.append(label)
            else:
                delta = delta + label.length_ms()

        return filtered_transcript
    
    def shift_labels_to_negative(self,padding_ms=50):
        """[summary]
        Some recordings involve reading an identifier for a phrase (e.g., "12332") and then
        reading the phrase (e.g., "dog"). ASR results in labelling both the identifiers and
        the phrases, which come out as gibberish in the event that the phrase is in an underresourced
        language. We apply post-processing to remove the phrases, resulting in a transcript that 
        transcribed all of the labels,e.g., 
        ```json
        {
            in: 12010,
            out: 13100,
            text: "12332"
        }
        ```

        This utility method shifts the label for the identifier ("12332") to where the phrase was spoken.
        Note that the text is still the identifier. This allows us to export clips that are named
        after said ID (e.g., "12332.wav") upstream to be linked with the term in the database in an
        automated way.

        This method is named because the empty space in the label track occupied by the phrases can be
        visualized as a negative of the original label track.
        """
        transformed_transcript = Transcript(self.name)
    
        for index,l in enumerate(self.labels):
            new_in = l.out_point_ms

            new_out = new_in if index == len(self.labels)-1 else self.labels[index+1].in_point_ms

            new_label = AudioLabel(in_point_ms=new_in+padding_ms,out_point_ms=new_out+padding_ms,text=l.text,speaker_initials=l.speaker_initials)
            
            transformed_transcript.append(new_label)

        return transformed_transcript\
        
    # TODO We should have an e2e test for this
    def to_coscrad(self,aggregateCompositeIdentifier,languageCode):
        create_transcript = {
            "type": "CREATE_TRANSCRIPT",
            "payload": {
                "aggregateCompositeIdentifier": aggregateCompositeIdentifier
            }
        }

        line_items = [
            l.to_coscrad_line_item_dto(languageCode) for l in self.labels
        ]

        import_line_items_to_transcript = {
            "type": "IMPORT_LINE_ITEMS_TO_TRANSCRIPT",
            "payload": {
                "aggregateCompositeIdentifier": aggregateCompositeIdentifier,
                "lineItems": line_items
            }
        }

        return [
            create_transcript,
            import_line_items_to_transcript
        ]
    
    # Should this return a list of labels instead of a string?
    def to_audacity_labels(self):
        # TODO Consider filtering out incomplete labels
        # Note that Audacity works in seconds not milliseconds
        return '\n'.join([f"{l.in_point_ms/1000}\t{l.out_point_ms/1000}\t{l.text}\t" for l in self.labels])

    def sort(self):
        get_in_point = lambda label: label.in_point_ms

        self.labels.sort(key=get_in_point)

    def apply_audio(self, audio_segment):
        # for each label
        for l in self.labels:
            # use pydub to get the audio segment from l.in_point to l.out_point
            audio_chunk = audio_segment[l.in_point_ms : l.out_point_ms]

            l.assign_audio(audio_chunk)

    def get_audio(self):
        full_audio = AudioSegment.empty()

        for l in self.labels:
            if l.has_audio():
                full_audio = full_audio + l.audio

        return full_audio
    
    def __json__(self):
        return {
            'name': self.name,
            'items': [l.to_coscrad_line_item_dto('en') for l in self.labels]
        }
