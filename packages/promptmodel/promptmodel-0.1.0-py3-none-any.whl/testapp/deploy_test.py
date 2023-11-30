from promptmodel import init
from promptmodel import PromptModel, ChatModel
from promptmodel.types.response import PromptModelConfig
from datetime import datetime

init(use_cache=True)

text = "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data. "


res = PromptModel("summarize").run({"text": text})
print(res.raw_output)


deployed_version_config: PromptModelConfig = PromptModel(
    "summarize", version="deploy"
).get_config()

print("DEPLOYED PROMPT")
print(deployed_version_config.prompts)


version_2_config: PromptModelConfig = PromptModel("summarize", version=2).get_config()

print("VERSION 2 PROMPT")
print(version_2_config.prompts)


latest_version_config: PromptModelConfig = PromptModel(
    "summarize", version="latest"
).get_config()

print("LATEST VERSION PROMPT")
print(latest_version_config.prompts)
