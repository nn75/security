# uncompyle6 version 3.4.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
# [GCC 8.2.0]
# Embedded file name: cryptotest.py
# Compiled at: 2018-09-26 21:10:38
import subprocess, sys, os, zlib, getpass, socket, datetime, hashlib
from StringIO import StringIO
suppress_output = True
HEADER = 'cryptotest v1.2.0 by Dr. Tyler Bletsch (Tyler.Bletsch@duke.edu)'
color_cmd = '33'
color_status = '32'
color_tests = '44;96'

def hash_self():
    return hash_file(sys.argv[0])


def hash_file(filename):
    with open(filename, 'rb') as (fp):
        m = hashlib.md5()
        m.update(fp.read() + 'vg' + 'slt')
        return m.hexdigest()


def hash_string(s):
    m = hashlib.md5()
    m.update(s + 'vg' + 'slt')
    return m.hexdigest()


def cprint(s, color=''):
    if sys.stdout.isatty():
        print '\x1b[%sm%s\x1b[m' % (str(color), s)
    else:
        print s


def status_print(s=''):
    cprint('\n' + s, color_status)


def my_call(cmd, stdin_content=''):
    if isinstance(cmd, str):
        cmd_str = cmd
    else:
        cmd_str = (' ').join(cmd)
    if suppress_output:
        child_out = open(os.devnull, 'w')
    else:
        child_out = None
    cprint('  $ %s' % cmd_str, color_cmd)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=child_out, stderr=child_out)
    p.communicate(stdin_content)
    sys.stdout.write('\n\n')
    return p.returncode


input_file_data = ('\n').join('Nice, cool looking input line #%d' % x for x in range(1, 1000))

def make_input_file(filename):
    with open(input_file, 'wb') as (fp):
        fp.write(input_file_data)


def get_compression_ratio(filename):
    full = os.path.getsize(filename)
    with open(filename, 'r') as (fp):
        data = fp.read()
    compressed = len(zlib.compress(data))
    return float(compressed) / full


def is_cryptish(filename):
    return get_compression_ratio(filename) > 0.95


def file_cmp(filename1, filename2, ignore_missing=False):
    if not os.path.exists(filename1):
        if not ignore_missing:
            print 'Warning: %s: No such file' % filename1
        return False
    if not os.path.exists(filename2):
        if not ignore_missing:
            print 'Warning: %s: No such file' % filename2
        return False
    with open(filename1, 'rb') as (fp1):
        with open(filename2, 'rb') as (fp2):
            return fp1.read() == fp2.read()


def tamper(input_file, output_file):
    with open(input_file, 'rb') as (fp_in):
        with open(output_file, 'wb') as (fp_out):
            data = fp_in.read()
            pos = int(len(data) / 2)
            data = data[:pos] + chr(ord(data[pos]) ^ 1) + data[pos + 1:]
            fp_out.write(data)


total_points = 0
total_points_awarded = 0
points_awarded_list = []

def do_test(name, points, result, fail_msg='', pass_msg=''):
    global total_points
    global total_points_awarded
    if result:
        result_str = 'ok'
        msg = pass_msg
        points_awarded = points
    else:
        result_str = 'FAIL'
        msg = fail_msg
        points_awarded = 0
    total_points += points
    total_points_awarded += points_awarded
    points_awarded_list.append(points_awarded)
    cprint('  %-30s [%4s] %2d/%2d pts   %s' % (name, result_str, points_awarded, points, msg), color_tests)


if len(sys.argv) != 2:
    print HEADER
    print '   Syntax: %s <encryption_tool>' % sys.argv[0]
    print ''
    print '  Example: %s duke-crypter' % sys.argv[0]
    print ''
    print 'Self-test and self-grading for the programming component of Computer & Information Security Homework 2 at Duke University.'
    print 'Produces a verifiable certificate of the test results for submission.'
    print ''
    sys.exit(1)
binary_name = sys.argv[1]
if not os.path.exists(binary_name):
    print '%s: No such file' % binary_name
    sys.exit(1)
if not os.path.isabs(binary_name):
    binary_name = os.path.join('.', binary_name)
right_secret_key = 'awesomekey1'
wrong_secret_key = 'wrongkey2'
input_file = 'test_input'
cipher_file = 'test_ciphered'
deciphered_file = 'test_ciphered_deciphered'
bad_deciphered_file = 'test_ciphered_deciphered_bad'
tampered_file = 'test_ciphered_tampered'
deciphered_tampered_file = 'test_ciphered_tampered_deciphered'
report_filename = 'cryptotest-report.txt'
right_secret_key_stdin = (right_secret_key + '\n') * 3
wrong_secret_key_stdin = (wrong_secret_key + '\n') * 3
print '\x1b[37;1;97;4m' + HEADER + '\x1b[m\n'
for f in [input_file, cipher_file, deciphered_file, tampered_file, deciphered_tampered_file]:
    try:
        os.remove(f)
    except OSError:
        pass

status_print("Generating input file '%s'..." % input_file)
make_input_file(input_file)
status_print("Encrypting to '%s'..." % cipher_file)
r = my_call([binary_name, '-e', input_file, cipher_file], stdin_content=right_secret_key_stdin)
do_test('Encryption exit status == 0?', 1, r == 0, 'Non-zero status indicates an error where none should have occurred.')
status_print('Calculating compression ratio...')
ratio = get_compression_ratio(cipher_file)
do_test('Cipher compressability > 95%?', 3, ratio > 0.95, 'The cipher file is too compressable (Ratio: %.2f%%).' % (ratio * 100), '(Ratio: %.2f%%)' % (ratio * 100))
status_print("Decrypting to '%s'..." % deciphered_file)
r = my_call([binary_name, '-d', cipher_file, deciphered_file], stdin_content=right_secret_key_stdin)
do_test('Decryption exit status == 0?', 1, r == 0, 'Non-zero status indicates an error where none should have occurred.')
status_print("Comparing '%s' and '%s'..." % (input_file, deciphered_file))
do_test('Decrypted content matches?', 6, file_cmp(input_file, deciphered_file), "Deciphered file doesn't match input.")
status_print("Attempting decryption with wrong secret key to '%s'..." % bad_deciphered_file)
r = my_call([binary_name, '-d', cipher_file, bad_deciphered_file], stdin_content=wrong_secret_key_stdin)
do_test('Decryption exit status != 0?', 1, r != 0, "Exit status %d means the tool didn't notice the key was wrong." % r, '(Exit status %d).' % r)
status_print("Comparing '%s' and '%s'..." % (input_file, bad_deciphered_file))
do_test('Mis-decrypted content differs?', 4, not file_cmp(input_file, bad_deciphered_file, ignore_missing=True), 'Deciphered file matches input even though the wrong key was used!')
status_print("Tampering with ciphertext to produce '%s'..." % tampered_file)
tamper(cipher_file, tampered_file)
status_print("Attempting decryption of tampered file to '%s'..." % deciphered_tampered_file)
r = my_call([binary_name, '-d', tampered_file, deciphered_tampered_file], stdin_content=right_secret_key_stdin)
do_test('Decryption exit status != 0?', 4, r != 0, "Exit status %d means the tool didn't detect the tampering." % r, '(Exit status %d).' % r)
cprint('-' * 54, color_tests)
cprint('  %-30s        %2d/%2d pts' % ('TOTAL', total_points_awarded, total_points), color_tests + ';1')
print ''
status_print('Writing certified report to %s...' % report_filename)
fp = StringIO()
fp.write(HEADER + '\n')
fp.write('= Certified results report =\n')
fp.write('\n')
fp.write('Binary under test: %s\n' % binary_name)
fp.write('Test points: %s\n' % str(tuple(points_awarded_list)))
fp.write('Total points: %d / %d\n' % (total_points_awarded, total_points))
fp.write('Current username: %s\n' % getpass.getuser())
fp.write('Current hostname: %s\n' % socket.gethostname())
fp.write('Timestamp: %s\n' % datetime.datetime.now())
fp.write('\n')
fp.write('Signatures:\n')
fp.write('%s\n' % hash_self())
fp.write('%s\n' % hash_file(binary_name))
this_file_hash = hash_string(fp.getvalue())
fp.write('%s\n' % this_file_hash)
with open(report_filename, 'wb') as (real_fp):
    real_fp.write(fp.getvalue())
status_print("\x1b[97m\nWhen you're satisfied, zip up your source code, the binary you used for this \ntest, and %s into a file called:\n\n  <netid>_homework2_crypter.zip \n\nSubmit this ZIP to Sakai.\n" % report_filename)
# okay decompiling cryptotest.pyc
