import openai

class ChatGPT:
    def input_data(self, failure):
        openai.api_key = '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'

        # Set up the model and prompt
        model_engine = "text-davinci-003"
        prompt = "How much maximum temperature in Thailand?"

        # Generate a response
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completion.choices[0].text
        return