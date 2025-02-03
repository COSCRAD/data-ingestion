class AudioLabel:
    def __init__(self, in_point, out_point, text, speaker_initials=None):
        self.in_point = in_point
        self.out_point = out_point
        self.text = text
        self.speaker_initials = speaker_initials

        self.audio = None

    def shift(self, delta):
        self.in_point = self.in_point - delta

        print(f"in_point after: {self.in_point}")

        self.out_point = self.out_point - delta

    def length(self):
        return self.out_point - self.in_point

    def has_audio(self):
        return self.audio is not None

    def assign_audio(self, chunk):
        self.audio = chunk
