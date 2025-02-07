from data_ingestion.audio_label import AudioLabel
from pydub import AudioSegment


class Transcript:
    def __init__(self, name):
        self.name = name

        self.labels = []

    def append(self, label):
        self.labels.append(label)

    def __str__(self):
        return '\n'.join([l.text for l in self.labels])

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

    def from_docx(doc):
        raise Exception("not implmented")
    
    def from_whisper_timestamped_transcript(raw_transcript,threshold_confidence_inclusive=0.51):
        t = Transcript(name="TODO add name")

            
        for s in raw_transcript['segments']:
            words = s.get('words',None)

            if words is None:
                # Should we raise an exception here?
                return
            
            for w in words:
                in_point_s = w.get('start',None)

                out_point_s = w.get('end',None)

                text = w.get('text',None)

                has_label_data = in_point_s is not None and out_point_s is not None and text is not None

                if w['confidence'] >= threshold_confidence_inclusive and has_label_data:
                    # TODO Should we null check these props?
                    l = AudioLabel(in_point_ms=in_point_s*1000,out_point_ms=out_point_s*1000,text=text)

                    t.append(l)

            return t

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
