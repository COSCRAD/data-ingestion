class AudioLabel:
    def __init__(self, in_point_ms, out_point_ms, text, speaker_initials=None):
        self.in_point_ms = in_point_ms
        self.out_point_ms = out_point_ms
        self.text = text
        self.speaker_initials = speaker_initials

        self.audio = None

    def shift(self, delta_ms):
        self.in_point_ms = self.in_point_ms - delta_ms

        print(f"in_point after: {self.in_point_ms}")

        self.out_point_ms = self.out_point_ms - delta_ms

    def length_ms(self):
        return self.out_point_ms - self.in_point_ms

    def has_audio(self):
        return self.audio is not None

    def assign_audio(self, chunk):
        self.audio = chunk

    def __str__(self):
        return f'[{self.in_point_ms},{self.out_point_ms}] ({self.speaker_initials}): {self.text}'

    def to_coscrad_line_item_dto(self,langaugeCode):
        return {
                "inPointMilliseconds": self.in_point_ms,
                "outPointMilliseconds": self.out_point_ms,
                "speakerInitials": self.speaker_initials,
                "text": self.text,
                "languageCode": langaugeCode
            } 
