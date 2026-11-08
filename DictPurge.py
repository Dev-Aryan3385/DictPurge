#!/usr/bin/env python3
# dictpurge.py

r"""
Copyright (C) 2024 Aryan Kumar Shrivastav

 ____  _      _   ____
|  _ \(_) ___| |_|  _ \ _   _ _ __ ___  ___
| | | | |/ __| __| |_) | | | | '__/ __/ _ \
| |_| | | (__| |_|  __/| |_| | |  \__ \  __/
|____/|_|\___|\\__|_|    \__,_|_|  |___/\___|

        DictPurge - Wordlist Management Tool
"""

import sys
import os
import optparse
import time
import zipfile
import tarfile
import bz2
import gzip
import io
from time import sleep
from termcolor import colored

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE_DIR, 'doc', 'VERSION')
LOGO_FILE = os.path.join(BASE_DIR, 'txt', 'logo.txt')
ARCHIVE_FORMATS_FILE = os.path.join(BASE_DIR, 'txt', 'archive_formats.txt')

def getVersion():
    try:
        with open(VERSION_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().strip()
    except Exception:
        return '1.0'

def displayLogo():
    version = getVersion()

    # ── ASCII art logo ──
    try:
        with open(LOGO_FILE, 'r', encoding='utf-8', errors='ignore') as f:
            logo = f.read()
    except IOError:
        logo = ''

    border = colored('=' * 68, 'white', attrs=['bold'])

    print()
    print(border)

    # Print logo in bold cyan
    for line in logo.splitlines():
        if line.strip():
            print(colored(line, 'cyan', attrs=['bold']))

    print()
    # SEToolkit-style information block
    bracket = colored('[---]', 'red', attrs=['bold'])
    line1 = colored('The DictPurge Toolkit (DictPurge)', 'white', attrs=['bold']) + (' ' * 7)
    line2 = colored('Created by: ', 'white') + colored('Aryan Kumar Shrivastav', 'green', attrs=['bold']) + (' ' * 6)
    line3 = colored('Version: ', 'white') + colored(version, 'yellow', attrs=['bold']) + colored('  |  Platform: ', 'white') + colored('Python 3.x', 'yellow', attrs=['bold']) + (' ' * 3)
    line4 = colored('Codename: ', 'white') + colored("'Wordlist Purger'", 'cyan', attrs=['bold']) + (' ' * 13)

    print(f"  {bracket}        {line1}        {bracket}")
    print(f"  {bracket}        {line2}        {bracket}")
    print(f"  {bracket}        {line3}        {bracket}")
    print(f"  {bracket}        {line4}        {bracket}")

    print(border)

    # Concise colored description of what the tool does (few clean lines, not messy)
    print(colored("  DictPurge is an advanced wordlist manipulation & dictionary merging tool.", 'yellow'))
    print(colored("  Crafted for security researchers, penetration testers & password audits.\n", 'white'))

    print(colored("  [+] Core Capabilities:", 'cyan', attrs=['bold']))
    print(f"      {colored('•', 'green', attrs=['bold'])} {colored('Merge', 'green', attrs=['bold'])}       : Combine multiple wordlists & directory trees into one")
    print(f"      {colored('•', 'green', attrs=['bold'])} {colored('Purge', 'green', attrs=['bold'])}       : Remove duplicate passwords while maintaining list order")
    print(f"      {colored('•', 'green', attrs=['bold'])} {colored('Sort/Invert', 'green', attrs=['bold'])} : Alphabetize (-s) or reverse (-r) dictionary contents")
    print(f"      {colored('•', 'green', attrs=['bold'])} {colored('Compress', 'green', attrs=['bold'])}    : Output directly to ZIP, GZ, BZ2, TAR archives (-z)")
    print(f"      {colored('•', 'green', attrs=['bold'])} {colored('Inject', 'green', attrs=['bold'])}      : Insert targeted phrases/passwords on-the-fly (-i)")

    print(border)
    print()

def flushPrint(msg, error=False, ext=False):
    if ext:
        msg, msg_e = msg.split(' --> ')
        msg += ' --> '

    if fast:
        if error:
            sys.stdout.write(colored('\n[-] ', 'red'))
            sys.stdout.write(colored(msg, 'red'))
            if ext:
                sys.stdout.write(colored(msg_e, 'red', attrs = ['bold']))
        else:
            sys.stdout.write(colored('\n[+] ', 'green'))
            sys.stdout.write(colored(msg, 'green'))
            if ext:
                sys.stdout.write(colored(msg_e, 'green', attrs = ['bold']))
    else:
        if error:
            sys.stdout.write(colored('\n[-] ', 'red'))
            for char in msg:
                sleep(0.03)
                sys.stdout.write(colored(char, 'red'))
                sys.stdout.flush()
            if ext:
                for char in msg_e:
                    sleep(0.03)
                    sys.stdout.write(colored(char, 'red', attrs = ['bold']))
                    sys.stdout.flush()
        else:
            sys.stdout.write(colored('\n[+] ', 'green'))
            for char in msg:
                sleep(0.03)
                sys.stdout.write(colored(char, 'green'))
                sys.stdout.flush()
            if ext:
                for char in msg_e:
                    sleep(0.03)
                    sys.stdout.write(colored(char, 'green', attrs = ['bold']))
                    sys.stdout.flush()

def delayEffect():
    if fast:
        return
    else:
        time.sleep(.5)

def appendListGenerator(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def readFiles():
    if len(argv) > 1:
        flushPrint("Reading Dictionaries")
        delayEffect()
        flushPrint("Merging Dictionaries")
    else:
        flushPrint("Reading Dictionary(ies)")

    # Load archive formats to reject compressed files early before reading
    try:
        with open(ARCHIVE_FORMATS_FILE, 'r', encoding='utf-8', errors='ignore') as af:
            commonFormats = [fmt.strip() for fmt in af.read().splitlines() if fmt.strip()]
    except IOError:
        commonFormats = []

    for i in range(len(argv)):
        # Check if dictionary file is compressed
        for archiveFormat in commonFormats:
            if argv[i].endswith(archiveFormat):
                delayEffect()
                flushPrint("Invalid Dictionary File Format --> Please Enter A Valid File", True, True)
                flushPrint("System Exit\n", True)
                raise SystemExit

        if not os.path.exists(argv[i]):
            delayEffect()
            flushPrint("Dictionary(ies) Not Found --> Please Enter A Valid Path", True, True)
            flushPrint("System Exit\n", True)
            raise SystemExit

        if os.path.getsize(argv[i]) == 0:
            delayEffect()
            flushPrint("Dictionary Is Empty --> Please Enter A Valid File", True, True)
            flushPrint("System Exit\n", True)
            raise SystemExit

        # Universal encoding handler: handles UTF-8, Latin-1, CP1252, and raw binary dumps
        try:
            try:
                with open(argv[i], 'r', encoding='utf-8', errors='surrogateescape') as myFile:
                    first_line = True
                    for line in myFile:
                        if first_line and line.startswith('\ufeff'):
                            line = line[1:]
                        first_line = False
                        wordList.append(line.rstrip('\r\n'))
            except UnicodeError:
                with open(argv[i], 'r', encoding='latin-1', errors='ignore') as myFile:
                    first_line = True
                    for line in myFile:
                        if first_line and line.startswith('\ufeff'):
                            line = line[1:]
                        first_line = False
                        wordList.append(line.rstrip('\r\n'))
        except IOError:
            delayEffect()
            flushPrint("Dictionary(ies) Not Found --> Please Enter A Valid Path", True, True)
            flushPrint("System Exit\n", True)
            raise SystemExit

def includeValues():
    flushPrint("Including Prompted Values")
    for value in include_values:
        wordList.append(value)

def makeUnique():
    global wordList

    flushPrint("Removing All Duplicates")
    # wordList = list(set(wordList)) --> This Messes Up The Order
    seen = set()
    seen_add = seen.add
    wordList = [i for i in wordList if not (i in seen or seen_add(i))]

def sortList():
    global wordList

    flushPrint("Sorting Dictionary Alphabetically")
    wordList = sorted(wordList)

def reverseList():
    global wordList

    flushPrint("Reversing Dictionary Items")
    wordList = list(reversed(wordList))

def uniqueOutFile(fName, fType):
    global dicFile
    global zipFile
    global compress
    global outFile

    if compress:
        checkFile = zipFile
        fType += '.' + zipType
    else:
        checkFile = dicFile
    if os.path.exists(checkFile):
        fList = list(fName)
        exists = True
        fName += '-{}'
        i = 1
        while exists:
            tempFile = (str(fName)+'.'+str(fType))
            tempFile = tempFile.format(i)
            if os.path.exists(tempFile):
                i += 1
            else:
                outFile = tempFile
                exists = False
    else:
        outFile = checkFile

def zipIt():
    global wordList
    global dicFile
    global zipFile
    global zipType
    global dicFileIn

    flushPrint("Zipping File")
    wordListStr = '\n'.join(wordList)
    wordListBytes = wordListStr.encode('utf-8', errors='surrogateescape')

    if zipType == 'zip':
        with zipfile.ZipFile('%s' % (outFile), 'w', zipfile.ZIP_DEFLATED) as zf:
            try:
                zf.writestr(dicFileIn, wordListBytes)
            finally:
                zf.close()
    elif zipType == 'tar' or zipType == 'tar.bz2' or zipType == 'tar.gz':
        if zipType == 'tar':
            mode = 'w'
        elif zipType == 'tar.bz2':
            mode = 'w:bz2'
        else:
            mode = 'w:gz'
        with tarfile.open('%s' % (outFile), '%s' % (mode)) as zf:
            try:
                zfInfo = tarfile.TarInfo('%s' % (dicFileIn))
                zfInfo.size = len(wordListBytes)
                zf.addfile(zfInfo, io.BytesIO(wordListBytes))
            finally:
                zf.close()
    elif zipType == 'gz':
        with gzip.GzipFile('%s' % (outFile), 'w', compresslevel = 9) as zf:
            try:
                zf.write(wordListBytes)
            finally:
                zf.close()
    elif zipType == 'bz2':
        with bz2.BZ2File('%s' % (outFile), 'w', compresslevel = 9) as zf:
            try:
                zf.write(wordListBytes)
            finally:
                zf.close()

def taskComplete():
    global wordList
    global dicFile
    global zipType
    global zipFile
    global outFile
    global compress
    global dicFileIn

    dicFile = output_file
    dList = dicFile.split('/')
    dicFileIn = dList[len(dList)-1]

    dList2 = dicFileIn.split('.')
    if len(dList2[0]) < 1:
        dList2[0] = 'dictpurged'
        dicFileIn = '.'.join(dList2)
        dList[len(dList)-1] = dicFileIn
        dicFile = '/'.join(dList)

    zipType = zip_type

    compress = False

    # to compress or to !compress
    if zipType != 'txt':
        compress = True

    f = dicFile.split('.')
    fName = f[0]
    # check if file format was inputed
    if len(f) > 1:
        fType = f[1]
    else:
        fName = dicFile
        fType = 'txt'

    # convert format into legit extension
    if zipType == 'bzip2':
        zipType = 'bz2'
    elif zipType == 'gzip':
        zipType = 'gz'
    elif zipType == 'bz2tar':
        zipType = 'tar.bz2'
    elif zipType == 'gztar':
        zipType = 'tar.gz'

    dicFile = (str(fName) + '.' + str(fType))
    zipFile = (str(dicFile) + '.' + str(zipType))

    uniqueOutFile(fName, fType)

    if not compress:
        try:
            with open(outFile, 'w+', encoding='utf-8', errors='surrogateescape') as myFile:
                for word in wordList:
                    myFile.write(str(word)+'\n')
        except IOError: # Error --> "Invalid Output File Path"
            delayEffect()
            flushPrint("Invalid Path To Out File Given --> Please Enter a Valid Path", True, True)
            flushPrint("System Exit\n", True)
            raise SystemExit
    else:
        # validate compression file type
        formats = ['zip', 'bz2', 'gz', 'tar', 'tar.bz2', 'tar.gz']
        if zipType in formats:
            delayEffect()
            zipIt()
        else:
            delayEffect()
            flushPrint("Invalid Zip Format --> Please Enter A Valid Zip Format", True, True)
            flushPrint("Choose from --> 'zip', 'bz2', 'gz', 'tar', 'bz2tar', 'gztar'", True, True)
            flushPrint("System Exit\n", True)
            raise SystemExit

    flushPrint("Task Successfully Complete")
    delayEffect()
    saved = "Final Dictionary Saved As --> " + str(outFile)
    flushPrint(saved, False, True)
    print("\nComp/tional Time Elapsed:", (time.perf_counter() - start))

def globalizeValues(o, i, z, s, u, r, f, a):
    global output_file
    global include_values
    global zip_type
    global sort
    global unique
    global reverse
    global fast
    global argv

    output_file = o
    include_values = i
    zip_type = z
    sort = s
    unique = u
    reverse = r
    fast = f
    argv = a

def main():

    global start
    global info
    global wordList

    start = time.perf_counter()

    displayLogo()

    optparse.OptionParser.format_epilog = lambda self, formatter: self.epilog

    version = getVersion()
    info = 'DictPurge ' + version + ' - Aryan Kumar Shrivastav'

    examples = ('\nExamples:\n'+
		'  DictPurge ~/dictionaries/ -s -u -o ~/powerful.txt\n' +
                '  DictPurge /usr/share/wordlists/rockyou.txt /lists/cewl.txt -s -u\n' +
                '  DictPurge /lists/cewl.txt /lists/awlg.txt -s -u -i and,this\n' +
                '  DictPurge ~/fsocity.dic -u -r -o ~/clean.txt\n' +
                '  DictPurge /dicts/crunch.txt /dicts/john.txt -u -f -z bz2\n')

    parser = optparse.OptionParser(epilog=examples,
                                   usage='DictPurge {dictionaries} [options]',
                                   prog='DictPurge', version=('DictPurge ' + version))

    parser.add_option('-o', '--output', action='store', default='dictpurged.txt',
                      dest='output_file', help='output filename')

    parser.add_option('-i', '--include', action='callback',
                      callback=appendListGenerator, type='string',
                      dest='include_values', help='include specified values in dictionary')

    parser.add_option('-z', '--zip', action='store', default='txt',
                      dest='zip_type', help='zip file with specified archive format')

    parser.add_option('-s', '--sort', action='store_true', default=False,
                      dest='sort', help='sort output alphabetically')

    parser.add_option('-u', '--unique', action='store_true', default=False,
                      dest='unique', help='remove dictionary duplicates')

    parser.add_option('-r', '--reverse', action='store_true', default=False,
                      dest='reverse', help='reverse dictionary items')

    parser.add_option('-f', '--fast', action='store_true', default=False,
                      dest='fast', help='finish task asap')

    (options, argv) = parser.parse_args()

    output_file = options.output_file
    include_values = options.include_values
    zip_type = options.zip_type
    sort = options.sort
    unique = options.unique
    reverse = options.reverse
    fast = options.fast

    # directory argument implementation
    expanded_argv = []
    for path in argv:
        if os.path.isdir(path):
            for file in sorted(os.listdir(path)):
                full_path = os.path.join(path, file)
                if os.path.isfile(full_path):
                    expanded_argv.append(full_path)
        else:
            expanded_argv.append(path)
    argv = expanded_argv

    globalizeValues(options.output_file, options.include_values, \
                    options.zip_type, options.sort, options.unique, \
                    options.reverse, options.fast, argv)

    wordList = []

    argLen = len(sys.argv[1:])
    dicLen = len(argv)

    if argLen > 1 and dicLen > 0:

        flushPrint("Starting Dictionary Merge Task")

        readFiles()
        delayEffect()

        if include_values != None:
            includeValues()
        delayEffect()

        if unique:
            makeUnique()
        delayEffect()

        if sort:
            sortList()
        delayEffect()

        if reverse:
            reverseList()
        delayEffect()

        taskComplete()

    elif argLen > 0 and dicLen < 1:
        flushPrint("No Dictionaries To Merge --> Use '-h' For Usage Help", True, True)
        flushPrint("System Exit\n", True)
    elif argLen > 0 and dicLen > 0 and dicLen < 2:
        flushPrint("No Options Selected --> Use '-h' For Usage Help", True, True)
        flushPrint("System Exit\n", True)
    else:
        print(colored("  [!] Quick Usage Examples:", "yellow", attrs=["bold"]))
        print(colored("      DictPurge <dict1.txt> <dict2.txt> -s -u -o powerful.txt", "white"))
        print(colored("      DictPurge ~/dictionaries/ -u -z bz2 -o clean.txt", "white"))
        print(colored("      DictPurge rockyou.txt cewl.txt -s -u -i admin,root,secret", "white"))
        print(colored("\n  [+] For all available options and syntax, run: ", "green") + colored("DictPurge -h\n", "white", attrs=["bold"]))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        flushPrint("System Exit\n", True)
        raise SystemExit
