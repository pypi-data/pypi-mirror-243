from enum import Enum

class OpenAIModels(Enum):
    GPT_3_5_TURBO = 'gpt-3.5-turbo'
    GPT_3_5_TURBO_16K = 'gpt-3.5-turbo-16k'
    GPT_3_5_TURBO_MARCH = 'gpt-3.5-turbo-0301'
    GPT_4 = 'gpt-4'
    GPT_4_MARCH = 'gpt-4-0314'
    GPT_4_32K = 'gpt-4-32k'
    GPT_4_32K_MARCH = 'gpt-4-32k-0314'
    GPT_4_TURBO = 'gpt-4-1106-preview'
    GPT_4_VISION = 'gpt-4-vision-preview'

class OllamaModels(Enum):
    LLAMA_2 = 'llama2'
    CODE_LLAMA = 'codellama'
    VICUNA = 'vicuna'
    MISTRAL = 'mistral'

ACCEPTED_OPENAI_MODELS = {
    OpenAIModels.GPT_3_5_TURBO.value,
    OpenAIModels.GPT_3_5_TURBO_16K.value,
    OpenAIModels.GPT_4.value,
    OpenAIModels.GPT_4_32K.value,
    OpenAIModels.GPT_4_TURBO.value
}

ACCEPTED_OLLAMA_MODELS = {
    OllamaModels.LLAMA_2.value,
    OllamaModels.CODE_LLAMA.value,
    OllamaModels.VICUNA.value,
    OllamaModels.MISTRAL.value
}

