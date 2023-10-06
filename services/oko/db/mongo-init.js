db = db.getSiblingDB('ctf_db')

db.createUser({
    'user': "ctf",
    'pwd' : "try_hack_me",
    'roles': [{
        'role': 'dbOwner',
        'db': 'ctf_db'
    }]
})

db.createCollection('firmware')

