---
dataset_info:
  features:
  - name: 'MSG #1'
    dtype: string
  - name: 'EHR #1'
    dtype: string
  - name: 'MSG #2'
    dtype: string
  - name: 'EHR #2'
    dtype: string
  - name: Label
    dtype: string
  splits:
  - name: INBOX_A
    num_bytes: 1370279
    num_examples: 435
  - name: INBOX_B
    num_bytes: 1430912
    num_examples: 434
  download_size: 119310
  dataset_size: 2801191
configs:
- config_name: default
  data_files:
  - split: INBOX_A
    path: data/INBOX_A-*
  - split: INBOX_B
    path: data/INBOX_B-*
license: cc-by-nc-4.0
---