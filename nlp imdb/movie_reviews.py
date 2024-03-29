# -*- coding: utf-8 -*-
"""movie_reviews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uyf3sbm5TH73TvVHKOF-EmElWURtc7Wg
"""

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

from fastai.text import *

path = untar_data(URLs.IMDB_SAMPLE)

path.ls()

df = pd.read_csv(path/'texts.csv')

df.head()

df['text'][2]

data_lm = TextDataBunch.from_csv(path, 'texts.csv')

data_lm.save()

data = load_data(path)

data.show_batch()

data.vocab.itos[:10]

data.train_ds[0][0]

data.train_ds[0][0].data[:10]

data = (TextList.from_csv(path, 'texts.csv', cols='text')
                .split_from_df(col=2)
                .label_from_df(cols=0)
                .databunch())

bs=48

path = untar_data(URLs.IMDB)
path.ls()

(path/'train').ls()

data_lm = (TextList.from_folder(path)
            .filter_by_folder(include=['train', 'test', 'unsup']) 
            .split_by_rand_pct(0.1)
            .label_for_lm()           
            .databunch(bs=bs))
data_lm.save('data_lm.pkl')

data_lm = load_data(path, 'data_lm.pkl', bs=bs)

data_lm.show_batch()

learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.3)

learn.lr_find()

learn.recorder.plot(skip_end=15)

learn.fit_one_cycle(1, 1e-2, moms=(0.8,0.7))

learn.save('fit_head')

learn.load('fit_head');

learn.unfreeze()

learn.fit_one_cycle(1, 1e-3, moms=(0.8,0.7))

learn.save('fine_tuned')

learn.load('fine_tuned')

TEXT = "This movie was an absolute waste of time beacause"
N_WORDS = 40
N_SENTENCES = 3

print("\n".join(learn.predict(TEXT, N_WORDS, temperature=0.75) for _ in range(N_SENTENCES)))

learn.save_encoder('fine_tuned_enc')

"""<h2>Classifier for movie reviews</h2>"""

path = untar_data(URLs.IMDB)

data_clas = (TextList.from_folder(path, vocab=data_lm.vocab)
             .split_by_folder(valid='test')
             .label_from_folder(classes=['neg', 'pos'])
             .databunch(bs=bs))

data_clas.save('data_clas.pkl')

data_clas = load_data(path, 'data_clas.pkl', bs=bs)

data_clas.show_batch()

learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn.load_encoder('fine_tuned_enc')

learn.lr_find()

learn.recorder.plot()

learn.fit_one_cycle(1, 2e-3, moms=(0.8,0.7))

learn.save('first')

learn.load('first')

learn.freeze_to(-2)
learn.fit_one_cycle(1, slice(1e-2/(2.6**4),1e-2), moms=(0.8,0.7))

learn.save('second')

learn.load('second')

learn.freeze_to(-3)
learn.fit_one_cycle(1, slice(5e-3/(2.6**4),5e-3), moms=(0.8,0.7))

learn.save('third')

learn.load('third')

learn.unfreeze()
learn.fit_one_cycle(2, slice(1e-3/(2.6**4),1e-3), moms=(0.8,0.7))

learn.predict("My son saw this movie with my husband. He is 13. They are both big movie buffs and my son is a very mature movie goer. We do restrict him on some movies but this one we allowed. Both my husband and him thought it was excellent! I think this movie is good for mature teenagers who are watching it with an adult. By contrast, I also have an 11 year old who is not ready for this and did not see it. It's important to know your kid.")

