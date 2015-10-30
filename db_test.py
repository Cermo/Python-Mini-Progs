import anydbm
import pickle
import shelve

db = shelve.open('bbc.db', 'c')

db['1'] = ['mmp3name','mp3link']

print db['1']
