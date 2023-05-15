from lime import lime_text
from lime.lime_text import LimeTextExplainer
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import torch
import numpy as np

# setting
'''
첫 실행 시 다운로드가 필요해 미리 할당
'''
model = AutoModelForSequenceClassification.from_pretrained('JminJ/kcElectra_base_Bad_Sentence_Classifier')
tokenizer = AutoTokenizer.from_pretrained('JminJ/kcElectra_base_Bad_Sentence_Classifier')
classifier = pipeline("sentiment-analysis", model=model,tokenizer=tokenizer)

def loadBadwordsModel():
    global model, tokenizer, classifier
    
    model = AutoModelForSequenceClassification.from_pretrained('JminJ/kcElectra_base_Bad_Sentence_Classifier')
    tokenizer = AutoTokenizer.from_pretrained('JminJ/kcElectra_base_Bad_Sentence_Classifier')
    classifier = pipeline("sentiment-analysis", model=model,tokenizer=tokenizer)

def mk_predlist(inps):
    global classifier
    
    outputs = classifier(inps)
    result = []
    for output in outputs:
        if output['label'] == 'bad_sen':
            result.append([output['score'], 1-output['score']])
        else:
            result.append([1-output['score'], output['score']])
    return np.array(result)

explainer = LimeTextExplainer(class_names=['bad','ok'])

def get_inference_badwords(text):
    global explainer
    
    if classifier(text)[0]['label'] == 'bad_sen':
        exp = explainer.explain_instance(text, mk_predlist,top_labels=1)

        badword = exp.as_list(label=0)[0][0]
        print('비속어 있음')
        print(badword)
        print(exp.as_list(label=0))

    else:
        print('비속어 없음')