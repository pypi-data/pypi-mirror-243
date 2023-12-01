"""\
Script to store password in plaintext in ~/.subversion/auth/svn.simple/

Useful in case Subversion is compiled without support for writing
passwords in plaintext.

Only use this script if the security implications are understood
and it is acceptable by your organization to store passwords in plaintext.

See https://subversion.apache.org/faq.html#plaintext-passwords
"""

# ====================================================================
#    Licensed to the Apache Software Foundation (ASF) under one
#    or more contributor license agreements.  See the NOTICE file
#    distributed with this work for additional information
#    regarding copyright ownership.  The ASF licenses this file
#    to you under the Apache License, Version 2.0 (the
#    "License"); you may not use this file except in compliance
#    with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing,
#    software distributed under the License is distributed on an
#    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#    KIND, either express or implied.  See the License for the
#    specific language governing permissions and limitations
#    under the License.
# ====================================================================

import hashlib
import os
import sys
from typing import Any

TERMINATOR = b"END\n"


def _read_one_datum(fd: Any, letter: bytes) -> Any:
    """\
    Read a 'K <length>\\n<key>\\n' or 'V <length>\\n<value>\\n' block from
    a svn_hash_write2()-format FD.

    LETTER identifies the first letter, as a bytes object.
    """
    assert letter in {b"K", b"V"}  # nosec assert_used

    # Read the letter and the space
    readletter = fd.read(1)
    if readletter != letter or fd.read(1) != b" ":
        raise ValueError("Hash file format error: Expected {!r} got {!r}".format(letter, readletter))

    # Read the length and the newline
    line = fd.readline()
    if line[-1:] != b"\n":
        raise ValueError("Hash file format error: Expected trailing \\n")
    expected_length = int(line[:-1])

    # Read the datum and its newline
    datum = fd.read(expected_length)
    if len(datum) != expected_length:
        raise ValueError("Hash file format error: Expected length {} got {}".format(expected_length, len(datum)))
    if fd.read(1) != b"\n":
        raise ValueError("Hash file format error: Extra data after reading {} bytes, expected \\n")

    return datum


# Our version of svn_hash_read2(), named without "svn_" prefix to avoid
# potential naming conflicts with stuff star-imported from svn.core.
def hash_read(fd: Any) -> dict[bytes, bytes]:
    """\
    Read a svn_hash_write2()-formatted file from FD, terminated by "END".

    Return a dict mapping bytes to bytes.
    """
    assert "b" in fd.mode  # nosec assert_used
    assert TERMINATOR[0] not in {b"K", b"V"}  # nosec assert_used

    ret: dict[bytes, bytes] = {}
    while True:
        if fd.peek(1)[0] == TERMINATOR[0]:
            if fd.readline() != TERMINATOR:
                raise ValueError("Hash file format error: Expected file terminator {!r}".format(TERMINATOR))
            if fd.peek(1):
                raise ValueError("Hash file format error: Extra content after file terminator")
            return ret

        key = _read_one_datum(fd, b"K")
        value = _read_one_datum(fd, b"V")
        ret[key] = value


def outputHash(fd: Any, hash_data: dict[bytes, bytes]) -> None:
    """\
    Write a dictionary HASH to an open file descriptor FD in the
    svn_hash_write2()-format, terminated by "END\\n".

    The keys and values must have datatype 'bytes' and strings must be
    encoded using utf-8.
    """
    assert "b" in fd.mode  # nosec assert_used

    for key, val in hash_data.items():
        fd.write(b"K " + bytes(str(len(key)), "utf-8") + b"\n")
        fd.write(key + b"\n")
        fd.write(b"V " + bytes(str(len(val)), "utf-8") + b"\n")
        fd.write(val + b"\n")
    fd.write(TERMINATOR)


def writeHashFile(filename: str, hash_data: dict[bytes, bytes]) -> None:
    """\
    Write the dict HASH to a file named FILENAME in svn_hash_write2()
    format.
    """
    tmpFilename = filename + ".tmp"
    try:
        with open(tmpFilename, "xb") as fd:
            outputHash(fd, hash_data)
            os.rename(tmpFilename, filename)
    except FileExistsError:
        print(
            "{}: File {!r} already exist. Is the script already running?".format(
                os.path.basename(__file__), tmpFilename
            ),
            file=sys.stderr,
        )
    except Exception:
        os.remove(tmpFilename)
        raise


def svn_store_plaintext_password(realm: str, username: str, password: str) -> None:
    # The file name is the md5encoding of the realm
    m = hashlib.new("md5", usedforsecurity=False)
    m.update(realm.encode("utf-8"))
    auth_file_name = os.path.join(os.path.expanduser("~/.subversion/auth/svn.simple/"), m.hexdigest())

    auth_file_exists = os.path.exists(auth_file_name)

    # In an existing file, we add/replace password/username/passtype
    if auth_file_exists:
        hash_data = hash_read(open(auth_file_name, "rb"))
        hash_data[b"username"] = username.encode("utf-8")
        hash_data[b"password"] = password.encode("utf-8")
        hash_data[b"passtype"] = b"simple"

    # For a new file, set realmstring, username, password and passtype
    else:
        hash_data = {
            b"svn:realmstring": realm.encode("utf-8"),
            b"username": username.encode("utf-8"),
            b"passtype": b"simple",
            b"password": password.encode("utf-8"),
        }

    # Write out the resulting file
    writeHashFile(auth_file_name, hash_data)
