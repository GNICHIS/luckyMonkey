# In this module file, I will suggest using a simple and light (key  value) In-Memory data store
# Since we are not going to use so much advanced operations from either SQLite and Redis
# We can just stick with using the below code for both the read and write operations ! 
# SQLite in fact is a relational database managment system,
# And based on our requirements we need to somehow store objects and Json files ! 
# (URLs and list of associated code blocks)
# (e.g : "https://www.example.com" : ["sendAjax('c');", "document.getElementById('a').click()", "abc(1);abc(2);", "_____", "_____"])
# However we can use SQLite to somehow store JSON objects, but that will require using an ORM (Object-relation mapping).
#
# Using other DBMSes such as Mongodb or Redis is going to be painful ! requirements, installing, blah blah
# And in the end we will just use a few basic operations !

# Global overview of the design ! 

# Database management systems are nothing but just softwares that manage files (files that pretend to be a fancy databases when they are in fact just files) on the disk
# My colleagues hate me when I start giving some brief and naif defintions like the above one.
# But the reality is as a said , databases are just files, DBMS is just a software to read, write data in a structural and effecient ways into these files.

# The DBMS is going to read an entire json file from a disk in one go into memory ! 
# and deal with it as a hash Table, where the hashed(URL) is the key and the list of strings ('code block') is the value.
# Reading data from memory is much more faster than reading data from disk so obvious !
# Read operation takes O(1) time in the average case and O(n) in worst case (don't worry this can only happens when some how all the keys passed to the hash function collide on one value which is impossible I assume)


import json
import os

class blahblahDB:
    def __init__(self, file, exist=False):
        self.dbpath = file
        if not exist:
            if not os.path.exists(file):
                with open(file, 'a') as touchfile:
                    os.utime(file, None)
                touchfile.close()
            self.db = {}
        else:
            with open(file, "r") as dbfile:
                self.db = json.load(dbfile)
            dbfile.close()

    def get(self, url):
        return self.db[url]
    def saveEntireDb(self, jobject):
        try:
            with open(self.dbpath, "w") as wfile:
                #json.dumps(jobject, wfile)
                wfile.write(json.dumps(jobject))
            wfile.close()
        except Exception:
            return False
        return True
        
