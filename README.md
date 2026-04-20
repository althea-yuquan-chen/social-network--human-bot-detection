# Social Network Human/Bot Detection

Binary classification of Twitter/Weibo accounts as **human** or **bot**, built for the [1st Social Collective Intelligence Algorithm Competition (track 1)](). Two modelling approaches are implemented: a gradient boosting classifier on structured profile features, and a BERT-based transformer on account descriptions.

---

## Repository Structure

```
.
├── data/
│   ├── competition_data_processed/   # Competition splits (train/dev/test) after feature engineering
│   │   ├── train_new.xlsx
│   │   ├── dev_new.xlsx
│   │   └── test_new.xlsx
│   ├── processed_with_url/           # Dev/test sets with image URL feature vectors appended
│   │   ├── dev_withurl.xlsx
│   │   └── test_withurl.xlsx
│   └── output_lgbm.xlsx              # LightGBM predictions on the test set
│
├── account_age.py                    # Feature – compute account age in days from created_at
├── langdetect.py                     # Feature – detect language of user description
├── pos_tagging.py                    # Feature – POS tagging of user description (EN/AR/JA/KO)
├── rgb_mapping.py                    # Feature – map hex profile colours to CSS3 colour names
├── lightGBM.ipynb                    # Model 1 – HistGradientBoosting on structured features + image embeddings
└── transformer.ipynb                 # Model 2 – Fine-tuned BERT on user description text
```

---

## Data

The dataset comes from the competition and is split into three sets:

| File | Description |
|------|-------------|
| `data/competition_data_processed/train_new.xlsx` | Training set after feature engineering |
| `data/competition_data_processed/dev_new.xlsx` | Validation set |
| `data/competition_data_processed/test_new.xlsx` | Test set |
| `data/processed_with_url/dev_withurl.xlsx` | Dev set with MobileNetV2 image embeddings |
| `data/processed_with_url/test_withurl.xlsx` | Test set with MobileNetV2 image embeddings |
| `data/output_lgbm.xlsx` | Final predictions from the LightGBM model |

Key features used across models: `followers_count`, `friends_count`, `statuses_count`, `verified`, `lang`, `account_age`, profile colour fields, image embedding vectors, description language, description POS distribution, sentiment.

---

## Feature Engineering Scripts

These scripts are run on the raw competition data before training. Run them in order.

### 1. Account Age (`account_age.py`)
Parses the `created_at` timestamp and computes how many days old each account is relative to the current date. Appends an `account_age` column.

> **Before running:** update the input/output paths.

**Requirements:** `pandas`

### 2. Language Detection (`langdetect.py`)
Detects the language of the `user/description` field using `langid`. Also strips emoji characters before running a second pass, producing both `language1` (raw) and `language2` (cleaned) columns.

> **Before running:** update the input/output paths.

**Requirements:** `pandas`, `langid`

### 3. POS Tagging (`pos_tagging.py`)
Runs part-of-speech tagging on `user/description` using spaCy models for English, Arabic, Japanese, and Korean in parallel, appending `pos_en`, `pos_ar`, `pos_ja`, `pos_ko` columns.

> **Before running:** update the input/output paths and install the required spaCy language models (see below).

**Requirements:** `pandas`, `spacy`

```bash
python -m spacy download en_core_web_sm
python -m spacy download ar_core_news_sm
python -m spacy download ja_core_news_sm
python -m spacy download ko_core_news_sm
```

### 4. RGB Colour Mapping (`rgb_mapping.py`)
Converts hex colour values in profile colour columns (background, link, sidebar, text, etc.) to the nearest CSS3 named colour using Euclidean distance in RGB space. Operates on CSV input.

> **Before running:** update `csv_file_path`, `output_file_path`, and `color_column_indices` to match your data.

**Requirements:** `webcolors`

---

## Models

### Model 1 — Gradient Boosting (`lightGBM.ipynb`)

Uses `sklearn.ensemble.HistGradientBoostingClassifier` (equivalent to LightGBM) on structured profile features plus MobileNetV2 image embeddings extracted from profile image URLs.

**Pipeline:**
1. Loads `train_new.xlsx`, `dev_new.xlsx`, `test_new.xlsx`
2. Fetches profile images from URLs and extracts feature vectors via MobileNetV2 (`imagenet` weights, global average pooling)
3. Merges image features with tabular features; drops raw text/URL columns
4. Merges train + dev, re-splits 80/20, encodes categoricals with `LabelEncoder`
5. Trains `HistGradientBoostingClassifier(max_iter=150, learning_rate=0.05, max_depth=3)`
6. Predicts on test set and saves to `data/output_lgbm.xlsx`

> **Before running:** update all file paths in the data-loading cells.

**Requirements:** `pandas`, `numpy`, `scikit-learn`, `tensorflow`, `Pillow`, `requests`, `openpyxl`

### Model 2 — BERT Transformer (`transformer.ipynb`)

Fine-tunes `bert-base-uncased` on the `description` text field for binary classification (bot=0, human=1).

**Pipeline:**
1. Loads `train_new.xlsx` and `dev_new.xlsx`
2. Tokenises descriptions with `BertTokenizer` (max length 128, padded)
3. Custom `nn.Module` wraps `BertModel` + a linear classification head (768 → 2)
4. Trains with `AdamW` (lr=1e-5), `CrossEntropyLoss`, 4 epochs, batch size 8
5. Evaluates accuracy on the dev set

> **Before running:** ensure `train_new.xlsx` and `dev_new.xlsx` are in the working directory, or update the paths.

**Requirements:** `torch`, `transformers`, `pandas`, `openpyxl`

---

## Reproducing the Analysis

```bash
# 1. Install Python dependencies
pip install pandas langid spacy webcolors openpyxl requests Pillow
pip install scikit-learn tensorflow
pip install torch transformers

# 2. Install spaCy language models
python -m spacy download en_core_web_sm
python -m spacy download ar_core_news_sm
python -m spacy download ja_core_news_sm
python -m spacy download ko_core_news_sm

# 3. Run feature engineering (update paths in each script first)
python account_age.py
python langdetect.py
python pos_tagging.py
python rgb_mapping.py

# 4. Run models
jupyter notebook lightGBM.ipynb
jupyter notebook transformer.ipynb
```

> **Note:** All scripts and notebooks contain hardcoded local file paths. Search for `read_excel`, `to_excel`, or path strings and update them before running.


