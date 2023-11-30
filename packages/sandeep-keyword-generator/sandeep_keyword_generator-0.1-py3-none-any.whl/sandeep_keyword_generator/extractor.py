import os
from transformers import pipeline, AutoTokenizer
import torch
from langchain import HuggingFacePipeline, PromptTemplate, LLMChain


class sandeep_keyword_generator:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.pipeline = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=self.tokenizer,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            max_length=512,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id
        )
        self.llm = HuggingFacePipeline(pipeline=self.pipeline, model_kwargs={'temperature':0.3})

    def extract_keywords(self, input_text):
        template = """
        You are an intelligent AI Assistant. Extract relevant keywords that represent the main ideas, concepts, entities, or themes mentioned in the provided text.
        Input: {input_text}
        Answer:"""
        prompt = PromptTemplate(template=template, input_variables=["input_text"])
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)
        return llm_chain.run(input_text)
    
    
