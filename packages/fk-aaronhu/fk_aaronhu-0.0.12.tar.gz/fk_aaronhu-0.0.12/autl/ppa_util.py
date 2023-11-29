import torch
import hashlib

def ahash(seq:str):
    return str(hashlib.sha3_256(seq.encode()).hexdigest())

def write_t5emb_by_protein_seq(seq:str,emb:torch.tensor,file_path:str="./data/protein_seq_t5_emb/"):
    filename = file_path + ahash(seq) + ".pth"
    torch.save(emb,filename)

def read_t5emb_by_protein_seq(seq:str,file_path:str="./data/protein_seq_t5_emb"):
    filename = file_path + ahash(seq) + ".pth"
    return torch.load(filename)

