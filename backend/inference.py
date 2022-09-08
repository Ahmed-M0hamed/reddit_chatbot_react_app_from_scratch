from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 

import torch 
from utils import Seq2SeqTransformer ,sequential_transforms ,tensor_transform ,greedy_decode
from torchtext.data.utils import get_tokenizer 
from torch.nn.utils.rnn import pad_sequence
from pydantic import BaseModel

app = FastAPI() 

origins =  ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware , 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)




vocab_transform = torch.load('../model/vocab_transform.pth') 
token_transform = get_tokenizer('spacy', language='en_core_web_sm')

SRC_VOCAB_SIZE = len(vocab_transform)
TGT_VOCAB_SIZE = len(vocab_transform)
EMB_SIZE = 512
NHEAD = 8
FFN_HID_DIM = 512
NUM_ENCODER_LAYERS = 3
NUM_DECODER_LAYERS = 3
UNK_IDX, PAD_IDX, BOS_IDX, EOS_IDX = 0, 1, 2, 3
DEVICE = torch.device('mps' if torch.cuda.is_available() else 'cpu')


model = Seq2SeqTransformer(NUM_ENCODER_LAYERS, NUM_DECODER_LAYERS, EMB_SIZE, 
                                 NHEAD, SRC_VOCAB_SIZE, TGT_VOCAB_SIZE, FFN_HID_DIM)
model.load_state_dict(torch.load('../model/model_v_1.pth')) 
model = model.to(DEVICE)
                            



# src and tgt language text transforms to convert raw strings into tensors indices

text_transform = sequential_transforms(token_transform, #Tokenization
                                        vocab_transform, #Numericalization
                                        tensor_transform) # Add BOS/EOS and create tensor


# actual function to translate input sentence into target language
def chat(model: torch.nn.Module, src_sentence: str):
    model.eval()
    src = text_transform(src_sentence).view(-1, 1)
    num_tokens = src.shape[0]
    src_mask = (torch.zeros(num_tokens, num_tokens)).type(torch.bool)
    tgt_tokens = greedy_decode(
        model,  src, src_mask, max_len=num_tokens + 100, start_symbol=BOS_IDX).flatten()
    return " ".join(vocab_transform.lookup_tokens(list(tgt_tokens.cpu().numpy()))).replace("<bos>", "").replace("<eos>", "")



@app.post('/predict/') 
def predict(data :dict ) : 
    data = dict(data)
    return chat(model , data['question'])