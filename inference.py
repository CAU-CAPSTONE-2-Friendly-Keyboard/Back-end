from transformers import AutoTokenizer, BertForSequenceClassification, TextClassificationPipeline

# model_output 폴더 path
PATH = './model_output'

model = BertForSequenceClassification.from_pretrained(
    PATH
)

'''pretrained model 불러오기'''
tokenizer = AutoTokenizer.from_pretrained(PATH)

pipe = TextClassificationPipeline(
    model = model,
    tokenizer = tokenizer,
    device=-1, # device = "cpu"
    return_all_scores=True,
    #function_to_apply='sigmoid'
    )

def loadModel():
    global PATH, model, pipe
    
    # model_output 폴더 path
    PATH = './model_output'

    model = BertForSequenceClassification.from_pretrained(
        PATH
    )

    '''pretrained model 불러오기'''
    tokenizer = AutoTokenizer.from_pretrained(PATH)

    pipe = TextClassificationPipeline(
        model = model,
        tokenizer = tokenizer,
        device=-1, # device = "cpu"
        return_all_scores=True,
        #function_to_apply='sigmoid'
        )

def get_predicated_label(output_labels, min_score):
    labels = []
    for label in output_labels:
        if label['score'] > min_score:
            labels.append(1)
        else:
            labels.append(0)
    return labels


def get_inference_hate_speech(text):
    global pipe
    
    out = get_predicated_label(pipe(text)[0], 0.5)
    if out[9] == 1:
        result = 'clean'
    else:
        result = 'notClean'
    return result