# similarity_check

similarity_check is a Python package for measuring the similarity of two texts.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install similarity_check.

```bash
pip install similarity_check 
```

## Usage
### sentence tranformer
#### documentation
* sentence_tranformer(
        targets: Union[List[str], pd.DataFrame], 
        target_group: Optional[Union[List[str], pd.DataFrame]]=None,
        target_cols: Optional[str]=None, 
        device: Optional[str] = None,
        model: Optional[str]=None, 
        lang: Optional[str]='en', 
        only_include: Optional[List[str]]=None,
        encode_batch: Optional[int] = 32,
        encode_target: Optional[bool] = True,
        remove_punct: Optional[bool]=True, 
        remove_stop_words: Optional[bool]=True, 
        stemm: Optional[bool]=False
  ):
  * parameters:
    * targets: dataframe or list of targets text to compare with.
    * target_group (optional): goups ids for the target to match only a single target for each group, can either provide list of ids,
    * or the column name in the target dataframe.
    * target_cols (partially optional): the target column names used to match, *must be specified for dataframe matching*.
    * device: the device to do the encoding on operations in (cpu|cuda),
    * model (optional): a string of the sentence tranformer model, to use instead of the default one, for more [details](https://www.sbert.net/).
    * lang (optional): the languge of the model ('en'|'ar').
    * only_include (optional): used only for dataframe matching, allow providing a list of column names to only include for the target matches, provide empty list to get only target_col.
    * encode_batch (optional): the number of sentences to encode in a batch.
    * encode_target: boolean flag to indicate whatever to enocde the targets when initilizing the object (to cache target encoding).
    * remove_punct: boolean flag to indicate whatever to remove punctuations. 
    * remove_stop_words: boolean flag to indicate whatever to remove stop words.
    * stemm: boolean flag to indicate whatever to do stemming.
* sentence_tranformer.match(
        source: Union[List[str], pd.DataFrame], 
        source_mapping: Optional[Union[str, List]]=None, 
        topn: Optional[int]=1, 
        return_match_idx: Optional[bool]=False, 
        threshold: Optional[float]=0.5, 
        batch_size: Optional[int]=128
    ) -> pd.DataFrame:
  * parameters:
    * source: dataframe or list of input texts to find closest match for.
    * source_mapping (partially optional) *must be specified for dataframe matching*: a list with each element being a tuple with the following three values (the target column name, source column name, the weight for this match), if a string is passed it and one target was only passed it will be mapped to the that target, with a the full weight of 1.0, note that the the overall weights must equal 1.0.
    * topn: number of matches to return.
    * threshold: the lowest threeshold for a match, matches below it are ignored.
    * batch_size: the size of the batch in inputs to match with targets (to limit space/memory usage).
  * returns:
    * a data frame with 3 main values (source, target columns, score), and two extra values for each extra match (target columns, score_2, target columns, score_3 ...)
#### examples
the given examples will only use english to present the output in the correct format, if you like to use arabic matching change the lang attribute of the sentence_tranformer object to 'ar'.
##### using lists
```python
from similarity_check.checkers import sentence_tranformer_checker

X = ['test', 'remove test']
y =  ['tests', 'stop the test', 'testing']

### arabic example:
# X = ['حذف الاختبار', 'اختبار']
# y =  ['اختبارات', 'ايقاف الاختبار']
# st = sentence_tranformer(lang='ar')
st = sentence_tranformer_checker()

st.init_targets(X)
match_df = st.match(y, topn=4, threshold=0.6)
```
output:
| source      |    score | prediction    |   match_idx |    score_2 | prediction_2   |   match_idx_2 |    score_3 | prediction_3   |   match_idx_3 | score_4   | prediction_4   | match_idx_4   |
|:------------|---------:|:--------------|------------:|-----------:|:---------------|--------------:|-----------:|:---------------|--------------:|:----------|:---------------|:--------------|
| test        | 0.922843 | tests         |           0 |   0.908599 | testing        |             2 |   0.721023 | stop the test  |             1 |           |                |               |
| remove test | 0.728872 | stop the test |           1 | nan        |                |           nan | nan        |                |           nan |           |                |               |
##### using dataframes
```python
from similarity_check.checkers import sentence_tranformer_checker

X = pd.DataFrame({
    'text': ['Cholera, a unspecified', 'remove test'],
    'id': [1, 2],
}
)

y = pd.DataFrame({
    'new_text': ['Cholera', 'stop the test', 'testing'],
    'new_id': [1, 2, 3],
    'tags': ['pos', 'neg', 'pos'],
    'num': [10, 22, 40],
    'day': [3, 5, 2],
}
)

st = sentence_tranformer_checker()
st.init_targets(y, target_cols='new_text',target_group='tags', only_include=['new_id'])
match_df = st.match(X, source_mapping=[('new_text','text', 1)], topn=4, threshold=0.6, batch_size=1)
```
output:
| text        |   id |   score_1 | new_text_1    |   new_id_1 |   score_2 | new_text_2   |   new_id_2 |   score_3 | new_text_3    |   new_id_3 | score_4   | new_text_4   | new_id_4   |
|:------------|-----:|----------:|:--------------|-----------:|----------:|:-------------|-----------:|----------:|:--------------|-----------:|:----------|:-------------|:-----------|
| test        |    1 |  0.922843 | tests         |          1 |  0.908599 | testing      |          3 |  0.721023 | stop the test |          2 |           |              |            |
| remove test |    2 |  0.728872 | stop the test |          2 |           |              |            |           |               |            |           |              |            |

### word mover distance (deprecated)
#### english
```python
# for medical use #
# from gensim.models import KeyedVectors
# download the model from here: https://github.com/ncbi-nlp/BioSentVec
# model = KeyedVectors.load_word2vec_format('BioWordVec_PubMed_MIMICIII_d200.vec.bin', binary=True)

# for general usage #
import gensim.downloader as api
from similarity_check.checkers import word_mover_distance

model = api.load('glove-wiki-gigaword-300')

X = ['test now', 'remove test']
y =  ['tests', 'stop the test']

wmd = word_mover_distance(X, y, model)
wmd.clean_data()
match_df = wmd.match(topn=3)
```
#### arabic
```python
from gensim.models import Word2Vec
from similarity_check.checkers import word_mover_distance

# download the embedding from here: https://github.com/bakrianoo/aravec (N-Grams Models, Wikipedia-SkipGram, Vec-Size:300)
model = Word2Vec.load('full_grams_sg_300_wiki/full_grams_sg_300_wiki.mdl')
# take the keydvectors as the model
model = model.wv

X = ['حذف الاختبار', 'اختبار']
y =  ['اختبارات', 'ايقاف الاختبار']

wmd = word_mover_distance(X, y, model)
wmd.clean_data()
match_df = wmd.match(topn=3)
match_df
```
* word_mover_distance(source_names, target_names, model):
  * parameters:
    * source_names: a list of input texts to find closest match for.
    * target_names: a list of targets text to compare with.
    * model (optional): a keyed vectors model (embeddings) to use for more [details](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html).
* word_mover_distance.clean_data(remove_punct=True, remove_stop_words=True, stemm=False, lang='en'):
  * parameters:
    * remove_punct: boolean flag to indicate whatever to remove punctuations. 
    * remove_stop_words: boolean flag to indicate whatever to remove stop words.
    * stemm: boolean flag to indicate whatever to do stemming.
    * lang: language of the text to clean ('en'|'ar').
* sentence_tranformer.match(topn=1, return_match_idx=False):
  * parameters:
    * topn: number of matches to return.
    * return_match_idxs: return an extra column for each match containing the index of the match within the target_names.
  * returns: 
    * a data frame with 3 columns (source, target, score), and two extra columns for each extra match (target_2, score_2 ...), and an optional extra column for each match containg the match index, if return_match_idxs set to True.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)