from .train.regression import *
from .downloader import download_from_drive
import os
import deepspeed
import json

class SEScore2:

    def __init__(self, lang):
        # load in the weights of SEScore2
        exp_config.device_id = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        if lang == 'en':
            if not os.path.exists("sescore2_en_supervised_3B.ckpt"):
                download_from_drive(FILE_ID='1XBfjvNbm5tpxdD62_gVpKQhwwrqXyewt', FILENAME='sescore2_en_supervised_3B.ckpt')
            # load in english version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/mt5-xl")
            model_named_dict = torch.load('sescore2_en_supervised_3B.ckpt', map_location=torch.device(exp_config.device_id))
            # for key in list(model_named_dict.keys()):
            #    model_named_dict[key.replace('roberta.', '')] = model_named_dict.pop(key)
            hidden_size = 2048
            exp_config.hidden_size = hidden_size
            exp_config.hidden_size_FNN = [hidden_size * 2, hidden_size]
            self.model = Regression_XLM_Roberta(f"google/mt5-xl")

            self.model.load_state_dict(model_named_dict)  # .to(exp_config.device_id)
            self.model.to(exp_config.device_id)
            self.model.eval()
        elif lang == 'de':
            # load in english version
            if not os.path.exists("sescore2_de_supervised_3B.ckpt"):
                download_from_drive(FILE_ID='1KAbZkIwfdSrYNszAFOnD1UnzOcM5J1mf', FILENAME='sescore2_de_supervised_3B.ckpt')
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/mt5-xl")
            model_named_dict = torch.load('sescore2_de_supervised_3B.ckpt', map_location=torch.device(exp_config.device_id))
            # for key in list(model_named_dict.keys()):
            #    model_named_dict[key.replace('roberta.', '')] = model_named_dict.pop(key)
            hidden_size = 2048
            exp_config.hidden_size = hidden_size
            exp_config.hidden_size_FNN = [hidden_size * 2, hidden_size]
            self.model = Regression_XLM_Roberta(f"google/mt5-xl")

            self.model.load_state_dict(model_named_dict)  # .to(exp_config.device_id)
            self.model.to(exp_config.device_id)
            self.model.eval()
        elif lang == 'ja':
            # load in japanese version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_ja.ckpt').to(exp_config.device_id)
        elif lang == 'es':
            # load in spainish version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_es.ckpt').to(exp_config.device_id)
        elif lang == 'zh':
            # load in chinese version
            self.tokenizer = AutoTokenizer.from_pretrained(f"google/rembert")
            self.model = torch.load('sescore2_zh.ckpt').to(exp_config.device_id)
        else:
            print("We currently only support five languages: en, de, ja, es, zh!")
            exit(1)

        self.model.eval()
        ds_engine = deepspeed.init_inference(self.model,
                                 mp_size=1,
                                 dtype=torch.half,
                                 checkpoint=None,
                                 replace_with_kernel_inject=True)
        self.model = ds_engine.module

    def score(self, refs, outs, batch_size):
        scores_ls = []
        cur_data_dict = {'pivot': refs, 'mt': outs}
        cur_data_loader = preprocess_data(cur_data_dict, self.tokenizer, exp_config.max_length, batch_size,
                                          shuffle=False, sampler=False, mode='test')
        for batch in cur_data_loader:
            # generate a batch of ref, mt embeddings
            score = self.model(batch, 'last_layer').squeeze(1).tolist()
            scores_ls.extend(score)
        return scores_ls
