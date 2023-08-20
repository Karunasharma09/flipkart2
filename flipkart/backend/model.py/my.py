import json
import os
from pprint import pprint

import bitsandbytes as bnb
import pandas as pd
import torch
import torch.nn as nn
import transformers
from datasets import load_dataset
from huggingface_hub import notebook_login
from peft import (
    LoraConfig,
    PeftConfig,
    PeftModel,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

# %%
with open("ecommerce-faq_gaur.json") as json_file:
    data = json.load(json_file)

# # %%
# pprint(data["questions"][0], sort_dicts=False)

# # %%
# pprint(data["questions"][1], sort_dicts=False)

# # %%
# pprint(data["questions"][2], sort_dicts=False)

# # %%
# pprint(data["questions"][3], sort_dicts=False)

# %%
with open("dataset.json", "w") as f:
    json.dump(data["questions"], f)

# %%
pd.DataFrame(data["questions"]).head()

# %% [markdown]
# ## Load Falcon Model & Tokenizer

# %%
MODEL_NAME = "tiiuae/falcon-7b"

# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16,
# )

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# %%
def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )

# %%
model.gradient_checkpointing_enable()
model = prepare_model_for_kbit_training(model)

# %%
config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["query_key_value"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, config)
print_trainable_parameters(model)

# %% [markdown]
## Inference Before Training

# %%
prompt = f"""
<human>: What is the compliance status of this log entry and also tell what action should be taken for this log entry Hostname: server-2 LogType: System LogMessage: Unauthorized file access detected LogSeverity: High Timestamp: 2023-08-20T02:27:25.896Z ProcessID: 9954 UserID: o4ruwdsn?
<assistant>:
""".strip()
print(prompt)

# %%
generation_config = model.generation_config
generation_config.max_new_tokens = 200
generation_config.temperature = 0.7
generation_config.top_p = 0.7
generation_config.num_return_sequences = 1
generation_config.pad_token_id = tokenizer.eos_token_id
generation_config.eos_token_id = tokenizer.eos_token_id

# %%
generation_config

# %%
device = "cuda"

encoding = tokenizer(prompt, return_tensors="pt").to(device)
with torch.inference_mode():
    outputs = model.generate(
        input_ids=encoding.input_ids,
        attention_mask=encoding.attention_mask,
        generation_config=generation_config,
    )
print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# %% [markdown]
# ## Build HuggingFace Dataset

# %%
data = load_dataset("json", data_files="dataset.json")

# %%
# data

# %%
# data["train"][0]

# %%
def generate_prompt(data_point):
    return f"""
<human>: {data_point["question"]}
<assistant>: {data_point["answer"]}
""".strip()


def generate_and_tokenize_prompt(data_point):
    full_prompt = generate_prompt(data_point)
    tokenized_full_prompt = tokenizer(full_prompt, padding=True, truncation=True)
    return tokenized_full_prompt

# %%
data = data["train"].shuffle().map(generate_and_tokenize_prompt)

# %%
data

# %% [markdown]
# ## Training

# %%
OUTPUT_DIR = "experiments"

# %%



training_args = transformers.TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    learning_rate=2e-4,
    fp16=True,
    save_total_limit=3,
    logging_steps=1,
    output_dir=OUTPUT_DIR,
    max_steps=100,
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    report_to="tensorboard",
)

trainer = transformers.Trainer(
    model=model,
    train_dataset=data,
    args=training_args,
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False),
)
model.config.use_cache = False
trainer.train()

# %% [markdown]
# ## Save Trained Model

# %%
model.save_pretrained("trained-model")

# %% [markdown]
# ## Load Trained Model

# %%
PEFT_MODEL = "curiousily/falcon-7b-qlora-chat-support-bot-faq"

config = PeftConfig.from_pretrained(PEFT_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    config.base_model_name_or_path,
    return_dict=True,
    device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
tokenizer.pad_token = tokenizer.eos_token

model = PeftModel.from_pretrained(model, PEFT_MODEL)

# %% [markdown]
# ## Inference

# %%
generation_config = model.generation_config
generation_config.max_new_tokens = 200
generation_config.temperature = 0.7
generation_config.top_p = 0.7
generation_config.num_return_sequences = 1
generation_config.pad_token_id = tokenizer.eos_token_id
generation_config.eos_token_id = tokenizer.eos_token_id


# %%
def generate_response(question: str) -> str:
    prompt = f"""
<human>: {question}
<assistant>:
""".strip()
    encoding = tokenizer(prompt, return_tensors="pt")
    with torch.inference_mode():
        outputs = model.generate(
            input_ids=encoding.input_ids,
            attention_mask=encoding.attention_mask,
            generation_config=generation_config,
        )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    assistant_start = "<assistant>:"
    response_start = response.find(assistant_start)
    return response[response_start + len(assistant_start) :].strip()

# %%
prompt = ""
print(prompt)
print(generate_response(prompt))

# %%

prompt = "What is the compliance status of this log entry and also tell what action should be taken for this log entry Hostname: server-2 LogType: System LogMessage: Unauthorized file access detected LogSeverity: High Timestamp: 2023-08-20T02:27:25.896Z ProcessID: 9954 UserID: o4ruwdsn?"
print(prompt)
print(generate_response(prompt))

# %%
prompt = "This is a log entry please generate compliance report Hostname: server-2 LogType: Application LogMessage: Unauthorized file access detected LogSeverity: High Timestamp: 2023-08-20T02:27:25.896Z ProcessID: 9372 UserID: tmncm1ud"
print(prompt)

print(generate_response(prompt))

# %%

prompt = "This is a log entry please generate compliance report Hostname: server-6 LogType: Application LogMessage: Normal log activity LogSeverity: Info Timestamp: 2023-08-20T02:27:25.896Z ProcessID: 5738 UserID: jshdv465"
print(prompt)

print(generate_response(prompt))


