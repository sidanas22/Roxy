### Roxy


This project implements a bare-bones web proxy called Roxy that passes requests and data between
multiple web clients and web servers, concurrently.

1. HTTP communications between client and server.
2. HTTPs communications between client and server.
3. Caching of popular content using at least two scheduling algorithms.
4. Content filtering (filtering rules should be configurable via admin console).

Also contained in this repo is a further iteration of the ideas from Roxy where reliable data transfer (RDT) protocol used by TCP has been developed from scratch.

# Features implemented:
<ul>
<li>RDT ACK</li>
<li>RDT Timeout</li>
<li>RDT Duplication Check</li>
<li>Checksum Validity Check</li>
<li>Sequence and acknowledgment numbers will be based on the number of bytes transferred</li>
<li>Fix timeout period</li>
</ul>

## Set up:

All the code was run using python 3.6 but should work well with any othere version too. 


## Video Demo and Explanation:
Google Drive Link: https://drive.google.com/file/d/1GBK5BT3ORQcyVordl6QaHIruVZ2RP5qO/view?usp=sharing


## Reference

- [StackOverflow - How many characters can UTF-8 encode?](https://stackoverflow.com/questions/10229156/how-many-characters-can-utf-8-encode)
- [RealPython - Python Sockets](https://realpython.com/python-sockets/)
- [GitHub, sgtb3 - Reliable Data Transfer Protocol](https://github.com/sgtb3/Reliable-Data-Transfer-Protocol)
- [Python Docs - Socket Programming](https://docs.python.org/3/library/socket.html#socket.socket.settimeout)
- [Stack Exchange, Network Engineering - Why can't a single port be used for both incoming and outgoing traffic?](https://networkengineering.stackexchange.com/questions/33061/why-cant-a-single-port-be-used-for-both-incoming-and-outgoing-traffic)
- [RealPython - An Intro to Threading in Python](https://realpython.com/intro-to-python-threading/)
- [UTF8.com, UTF-8 and Unicode](https://www.utf8.com/#:~:text=It%20is%20an%20efficient%20encoding,character%20set%20on%20the%20Web.)
- [StackOverflow, Convert binary to ASCII and vice versa](https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa)
- [Docs Python, OpenSSL - Self-signed Certificates](https://docs.python.org/3.6/library/ssl.html#self-signed-certificates)
