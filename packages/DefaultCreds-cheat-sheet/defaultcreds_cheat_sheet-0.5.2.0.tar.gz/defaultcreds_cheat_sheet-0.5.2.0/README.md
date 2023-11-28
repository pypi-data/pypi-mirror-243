
# Default Credentials Cheat Sheet

<p align="center">
  <img src="https://media.moddb.com/cache/images/games/1/65/64034/thumb_620x2000/Lockpicking.jpg"/>
</p>

**One place for all the default credentials to assist pentesters during an engagement, this document has several products default login/password gathered from multiple sources.**

> P.S : Most of the credentials were extracted from changeme,routersploit and Seclists projects, you can use these tools to automate the process https://github.com/ztgrace/changeme , https://github.com/threat9/routersploit (kudos for the awesome work)


## Installation & Usage

The Default Credentials Cheat Sheet tool is available on [pypi](https://pypi.org/project/defaultcreds-cheat-sheet/)

```bash
$ pip3 install defaultcreds-cheat-sheet
$ creds search tomcat
```

| Operating System   | Tested         |
|---------------------|-------------------|
| Linux(Kali,Ubuntu,Lubuntu)             | ✔️      |
| Windows             | ✔️               |
| macOS               | ❌               |

##### Manual Installation

```bash
$ git clone https://github.com/ihebski/DefaultCreds-cheat-sheet
$ pip3 install -r requirements.txt
$ cp creds /usr/bin/ && chmod +x /usr/bin/creds
$ creds search tomcat
```

## Creds script

### Usage Guide
```bash
# Search for product creds
➤ creds search tomcat                                                                                                      
+----------------------------------+------------+------------+
| Product                          |  username  |  password  |
+----------------------------------+------------+------------+
| apache tomcat (web)              |   tomcat   |   tomcat   |
| apache tomcat (web)              |   admin    |   admin    |
...
+----------------------------------+------------+------------+

# Update records
➤ creds update
Check for new updates...🔍
New updates are available 🚧
[+] Download database...

# Export Creds to files (could be used for brute force attacks)
➤ creds search tomcat export
+----------------------------------+------------+------------+
| Product                          |  username  |  password  |
+----------------------------------+------------+------------+
| apache tomcat (web)              |   tomcat   |   tomcat   |
| apache tomcat (web)              |   admin    |   admin    |
...
+----------------------------------+------------+------------+

[+] Creds saved to /tmp/tomcat-usernames.txt , /tmp/tomcat-passwords.txt 📥
```

**Run creds through proxy**
```bash
# Search for product creds
➤ creds search tomcat --proxy=http://localhost:8080

# update records
➤ creds update --proxy=http://localhost:8080

# Search for Tomcat creds and export results to /tmp/tomcat-usernames.txt , /tmp/tomcat-passwords.txt
➤ creds search tomcat --proxy=http://localhost:8080 export
```

## Contribute

If you cannot find the password for a specific product, please submit a pull request to update the dataset.<br>

> ### Disclaimer
> **For educational purposes only, use it at your own responsibility.** 