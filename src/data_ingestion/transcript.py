from data_ingestion.audio_label import AudioLabel
from pydub import AudioSegment


class Transcript:
    def __init__(self, name):
        self.name = name

        self.labels = []

    def append(self, label):
        self.labels.append(label)

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

            transcript.append(AudioLabel(in_point=float(i), out_point=float(o), text=t))

        return transcript

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
                delta = delta + label.length()

        return filtered_transcript

    def sort(self):
        get_in_point = lambda label: label.in_point

        self.labels.sort(key=get_in_point)

    def apply_audio(self, audio_segment):
        # for each label
        for l in self.labels:
            # use pydub to get the audio segment from l.in_point to l.out_point
            audio_chunk = audio_segment[l.in_point : l.out_point]

            l.assign_audio(audio_chunk)

    def get_audio(self):
        full_audio = AudioSegment.empty()

        for l in self.labels:
            if l.has_audio():
                full_audio = full_audio + l.audio

        return full_audio
