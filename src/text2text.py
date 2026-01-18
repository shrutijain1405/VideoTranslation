from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSeq2SeqLM


def load_model_trans(device):

    model_name = "Helsinki-NLP/opus-mt-en-de"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(device)

    return model, tokenizer

def load_llm_model(device):

    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(device)

    return model, tokenizer


def run_inference_translations(model, tokenizer, inp_text):
    inp_text = inp_text.strip()
    prompt = inp_text
    input_ids = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(model.device)

    output = model.generate(
        **input_ids,
        # do_sample=True,
        # temperature=0.5,
        # min_p=0.15,
        # repetition_penalty=1.05,
        max_new_tokens=2048,
    )

    output_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return output_text.strip()

def adjust_translation_length(translated_sentence, target_chars, model, tokenizer, device):

    prompt = f"Rewrite the following sentence to be approximately {target_chars} characters long, keeping meaning intact:\n{translated_sentence}"
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=200)
    adjusted = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
    return adjusted

def get_translations(sentence_groups, device):
    print("Translations: ")

    model_trans, tok_trans = load_model_trans(device)
    model_llm, tok_llm = load_llm_model(device)

    trans_sentences = []
    for sentence in sentence_groups:
        print("********************************")
        print("input sentence:       ", sentence["text"])
        output_text = run_inference_translations(model_trans, tok_trans, sentence["text"])
        print("original translation: ", output_text)
        diff = abs(len(sentence["text"]) - len(output_text)) 
        if( diff >= 10):
            output_text = adjust_translation_length(output_text, len(sentence["text"]), model_llm, tok_llm, device)
            print("adjusted translation: ", output_text)
        trans_sentences.append(output_text)
    return trans_sentences
