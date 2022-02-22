from transformers import AutoTokenizer, AutoModel, AutoConfig, AutoModelForTokenClassification, \
    TokenClassificationPipeline
import torch
import multiprocessing


class BioProcessor:
    def __init__(self, model_name):
        # If there's a GPU available...
        if torch.cuda.is_available():

            # Tell PyTorch to use the GPU.
            device = torch.device("cuda")
            self.gpu_flag = True
            print('There are %d GPU(s) available.' % torch.cuda.device_count())

            print('We will use the GPU:', torch.cuda.get_device_name(0))

        # If not...
        else:
            print('No GPU available, using the CPU instead.')
            self.gpu_flag = False
            device = torch.device("cpu")
            torch.set_num_threads(int(multiprocessing.cpu_count()/2))

        self.model_name = model_name
        # print(self.model_name)
        self.config = AutoConfig.from_pretrained(self.model_name)
        # print('config set')
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            use_fast=True,
            return_offsets_mapping=False
        )
        # print('tokenizer set')
        self.model = AutoModelForTokenClassification.from_pretrained(
            self.model_name,
            config=self.config
        )
        # print('model set')

        if self.gpu_flag:
            try:
                self.pipeline = TokenClassificationPipeline(model=self.model, tokenizer=self.tokenizer, framework='pt',
                                                            task='ner',
                                                            grouped_entities=True,
                                                            device=0)
            except:
                print('It was not possible to allocate model pipeline in GPU, setting it on CPU')
                self.gpu_flag = False
                device = torch.device("cpu")
                torch.set_num_threads(int(multiprocessing.cpu_count()/2))
                self.config = AutoConfig.from_pretrained(self.model_name)
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    use_fast=True,
                    return_offsets_mapping=True
                )
                self.model = AutoModelForTokenClassification.from_pretrained(
                    self.model_name,
                    config=self.config
                )
                self.pipeline = TokenClassificationPipeline(model=self.model, tokenizer=self.tokenizer, framework='pt',
                                                            task='ner',
                                                            grouped_entities=True,
                                                            )
        else:
            self.pipeline = TokenClassificationPipeline(model=self.model, tokenizer=self.tokenizer, framework='pt',
                                                        task='ner',
                                                        grouped_entities=True,
                                                        )
        # print('pipeline set')
        #self.sequence = ''
        #self.offset = 0
        #self.results = {}

    def predict(self, sequence):
        #print("predict:",sequence)
        results =  self.pipeline(str(sequence))
        #print("results:",results)
        return results
