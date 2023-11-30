"""This single file is needed to build the Client development dashboard."""

from promptmodel import DevApp
from main import client as main_client

# Example imports
# from <dirname> import < objectname>

app = DevApp()

# Example usage
# This is needed to integrate your codebase with the prompt engineering dashboard

app.include_client(main_client)

app.register_sample(
    name="function_call_test/1",
    content={"user_message": "What is the weather like in Boston?"},
)

app.register_sample(
    name="summarize/attention",
    content={
        "text": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data. "
    },
)

# from main import get_current_weather, get_current_weather_desc

# app.register_function(get_current_weather_desc, get_current_weather)
