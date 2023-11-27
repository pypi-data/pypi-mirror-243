import os
os.environ["CUDA_VISIBLE_DEVICES"] = '1'

import io
import re
import copy
from contextlib import redirect_stdout
import pandas as pd
import random
from pathlib import Path
import gc

from chatmof.agents.agent import ChatMOF
from chatmof.llm import get_llm
from chatmof.config import config as config_default
from langchain.callbacks import StdOutCallbackHandler


##### model
model = 'gpt-3.5-turbo-16k'
temperature = 0.1
file = 'test/predictor2.txt'
task = 'predictor'
######

with open(file) as f:
    questions = [line.strip() for line in f]

config = copy.deepcopy(config_default)


qna = []

save_path = Path(f'./test/{task}_{model}')
save_path.mkdir(exist_ok=True, parents=True)

for i, question in enumerate(questions):
    #if i <= 45:
    if i not in [4, 8, 9, 10, 13, 15, 18, 23, 25, 28, 29, 36, 37, 39, 41, 45, 47, 48, 51, 54, 56, 61, 62, 63, 64, 68, 69, 74, 76, 77, 78, 80, 83, 86, 87, 89, 92, 93, 98, 97, ]:
        print (f'skip {i} step')
        continue

    print (f'running {i} step')
    question = question.strip()

    llm = get_llm(model, temperature=temperature)
    callback_manager = [StdOutCallbackHandler()]

    chatmof = ChatMOF.from_llm(
        llm=llm, 
        verbose = True,
        search_internet = False,
    )

    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            output = chatmof.run(question, callbacks=callback_manager)
        except Exception as e:
            print (type(e), e)
            output = None
        log = buf.getvalue()

    qna.append([i, question, output])

    with (save_path/f'{i}_.output').open('w') as f:
        f.write(log)

    del llm
    del chatmof
    gc.collect()

df = pd.DataFrame(qna)
df.to_csv(f'test/predictor_csv_{model}.csv')
