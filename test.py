import transformers
from transformers import AutoModel, AutoTokenizer

transformers.logging.set_verbosity_error()

AutoTokenizer.from_pretrained("sayby/rna_torsionbert", trust_remote_code=True)
model = AutoModel.from_pretrained("sayby/rna_torsionbert", trust_remote_code=True)
