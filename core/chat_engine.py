from transformers import LlamaTokenizer, LlamaForCausalLM
import torch
class ChatEngine:
    def __init__(self, model_name="openchat/openchat-3.5-1210"):
        self.tokenizer = LlamaTokenizer.from_pretrained(model_name, token="your_token_here")
        self.model = LlamaForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16,
            token="your_token_here"
        )

    def generate_reply(self, user_input, max_tokens=512):
        prompt = f"<|user|>\n{user_input}\n<|assistant|>\n"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).split("<|assistant|>")[-1].strip()
