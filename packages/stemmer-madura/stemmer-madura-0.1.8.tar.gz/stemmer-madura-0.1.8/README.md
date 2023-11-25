# Stemmer Madura

Stemmer Madura adalah sebuah program untuk melakukan stemming pada bahasa Madura. Stemming adalah proses mengubah kata berimbuhan menjadi kata dasar. Stemming pada bahasa Madura dilakukan dengan menghapus imbuhan yang terdapat pada kata. Program ini menggunakan pendekatan _rule based_ dan dibangun dengan bahasa pemrograman Python. Bagi pengembang yang menggunakan Typescript/Javascript, dapat menggunakan [stemmer-madura](https://www.npmjs.com/package/stemmer-madura) yang dibangun dengan Typescript.

## Instalasi

Untuk menggunakan program ini, Anda harus menginstal Python 3.6 atau yang lebih baru. Kemudian, Anda dapat menginstal program ini dengan menggunakan perintah berikut:

```bash
pip install stemmer-madura
```

## Penggunaan

Untuk menggunakan program ini, Anda dapat menggunakan perintah berikut:

```python
from stemmer_madura import stemmer

print(stemmer('nglerek nak-kanak ngakan roti', True))
# lerek kanak kakan roti
```