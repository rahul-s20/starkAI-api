from transformers import T5ForConditionalGeneration, T5Tokenizer


class TranscriptsT5F:
    def __init__(self):
        # initialize the model architecture and weights
        self.model = T5ForConditionalGeneration.from_pretrained("t5-base")
        # initialize the model tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained("t5-base")

    def token_handler(self, script: str):
        inputs = self.tokenizer.encode("summarize: " + script, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4,
                                      early_stopping=True)
        return self.tokenizer.decode(outputs[0])
