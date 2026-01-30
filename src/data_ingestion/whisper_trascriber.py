# Note that we pull the weights for Whisper and run inference locally. No data is sent to OpenAI's API
import whisper_timestamped as wt
from data_ingestion.transcript import Transcript

# Note that this is primarily useful for dictionary recordings with sequential word labels (numericall slugs)
class WhisperTranscriber:
    def __init__(self, model='turbo'):
        # TODO We may want to make this configurable
        self.transcriber = wt.load_model(model)

        self.threshold_confidence = 0.88

    def transcribe(self,file,name):
        audio = wt.load_audio(file)

        # TODO Ensure the Whisper \ WhisperTimestamped version is part of this data in case their schema changes later
        raw_transcript = wt.transcribe(self.transcriber,audio,'en')
        # We return the raw Whisper (Timestamped) transcript in case we want to modify the post-processing later to avoid information loss
        return [Transcript.from_whisper_timestamped_transcript(raw_transcript,name, self.threshold_confidence),name,raw_transcript]


        