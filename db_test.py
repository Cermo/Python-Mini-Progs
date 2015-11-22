import anydbm
import pickle
import shelve

db = shelve.open('bbc.db', 'c')

db = [['mmp3name','mp3link'],['mmp3name2','mp3link2']]

print db
