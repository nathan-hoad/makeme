#!/usr/bin/python2
import sys
import hashlib
import re
import os
sys.path.append('/'.join(os.getcwd().split('/')[:-1]))
import config

def stderr_print(text):
    sys.stderr.write(text + '\n')

if sys.argv[4].upper().find('HELP') != -1:
    stderr_print("This script can be used by any other script to ensure only authorised users are able to send instructions.")
    stderr_print("To set the password, run this script outside makeme with the args 'set <password>' where password is the one you want to use. It will be stored in your makeme config and called by every script that implements security.")
    stderr_print("To actually use it to ensure that you can get your instructions acted on, simply put security <password> into the body of your email.")
    sys.exit(0)

def get_password():
    """This should read from a text file, or a user's config, or something like that."""
    conf = config.get_config(os.path.join(os.environ['HOME'], '.makemerc'), '/usr/share/makeme/makemerc')
    try:
        return conf['settings']['security']
    except KeyError:
        stderr_print("You need to specify a security option in your config file to use the security module!")
        sys.exit(1)

    hashlol = hashlib.new('sha512')
    hashlol.update("text")
    return hashlol.hexdigest()

if __name__ == "__main__":
    if sys.argv[1].lower() == 'set':
        hasher = hashlib.new('sha512')
        hasher.update(sys.argv[2])
        conf = config.get_config(os.path.join(os.environ['HOME'], '.makemerc'), '/usr/share/makeme/makemerc')
        conf['settings']['security'] = hasher.hexdigest()
        conf.save()
    else:
        print "You can only run this script to set your password"
else:
    search = re.compile(r'security (\S+)', re.IGNORECASE)
    result = search.search(sys.argv[4].upper())

    if result:
        stored_password = get_password()

        hasher = hashlib.new('sha512')
        hasher.update(result.groups()[0])
        if hasher.hexdigest() != stored_password:
            stderr_print("Access Denied.")
            sys.exit(0)
    else:
        stderr_print("Access Denied.")
        sys.exit(0)
