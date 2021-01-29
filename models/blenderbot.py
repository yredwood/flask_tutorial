from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

class HuggingfaceBlenderbot():
    def __init__(self):
        self.name = 'facebook/blenderbot-400M-distill'
        self.model = BlenderbotForConditionalGeneration.from_pretrained(self.name)
        self.tokenizer = BlenderbotTokenizer.from_pretrained(self.name)

    
    def __call__(self, histories, sentence):
        self.model.eval()
        inputs = self._make_input(histories, sentence)['input_ids']
        res = self.model.generate(input_ids=inputs, num_beams=5, max_length=128)
        decoded = self.tokenizer.decode(res[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
        return decoded

    def _make_input(self, histories, sentence):
        strings = ''
        for hist in histories:
            strings += hist['user'] + '\n'
            strings += hist['bot'] + '\n'
        strings += sentence
        
        inputs = self.tokenizer(strings, return_tensors='pt', truncation=True)
        return inputs


if __name__ == '__main__':
    hist = []
    sent = 'hihi'

    bot = HuggingfaceBlenderbot()
    res = bot(hist, sent)
    print (res)
        
