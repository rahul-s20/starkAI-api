from googletrans import Translator, constants


class LanguageTranslate:
    def __init__(self):
        self.translator = Translator()

    def tras_lation(self, input_text: str, dest: str = "en") -> dict:
        try:
            translation = self.translator.translate(text=input_text, dest=dest)
            res = {"input": translation.origin, "input_lang": translation.src, "output": translation.text,
                   "output_lang": translation.dest}
            return res
        except Exception as er:
            return er
