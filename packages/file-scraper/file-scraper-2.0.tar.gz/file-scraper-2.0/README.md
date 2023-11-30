# File Scraper

Scrape files for sensitive information, and generate an interactive HTML report. Based on Rabin2.

Customize the tool to your liking!

Tested on Kali Linux v2023.3 (64-bit).

Made for educational purposes. I hope it will help!

## Table of Contents

* [How to Install](#how-to-install)
* [How to Build and Install Manually](#how-to-build-and-install-manually)
* [Build the Template & Run](#build-the-template--run)
* [Usage](#usage)
* [Images](#images)

## How to Install

```bash
pip3 install file-scraper

pip3 install --upgrade file-scraper

apt-get -y install radare2
```

## How to Build and Install Manually

Run the following commands:

```bash
git clone https://github.com/ivan-sincek/file-scraper && cd file-scraper

python3 -m pip install --upgrade build

python3 -m build

python3 -m pip install dist/file_scraper-2.0-py3-none-any.whl

apt-get -y install radare2
```

## Build the Template & Run

Prepare a [template](https://github.com/ivan-sincek/file-scraper/blob/main/src/file_scraper/default.json):

```json
{
   "authorization":{
      "query":"[^\\w\\d\\n]+(?:basic|bearer)\\ .+",
      "ignorecase":true,
      "search":true
   },
   "variable":{
      "query":"(?:access|account|admin|basic|bearer|card|conf|cred|customer|email|history|id|info|jwt|key|kyc|log|otp|pass|pin|priv|refresh|salt|secret|seed|setting|sign|token|transaction|transfer|user)[\\w\\d]*(?:\\\"\\ *\\:|\\ *\\=).+",
      "ignorecase":true,
      "search":true
   },
   "comment":{
      "query":"[^\\w\\d\\n]+(?:bug|comment|fix|issue|note|problem|to(?:\\_|\\ |)do|work)[^\\w\\d\\n]+.+",
      "ignorecase":true,
      "search":true
   },
   "url":{
      "query":"\\w+\\:\\/\\/[\\w\\-\\.\\@\\:\\/\\?\\=\\%\\&\\#]+",
      "unique":true,
      "collect":true
   },
   "ip":{
      "query":"(?:\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(?:\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}",
      "unique":true,
      "collect":true
   },
   "base64":{
      "query":"(?:[a-zA-Z0-9\\+\\/]{4})*(?:[a-zA-Z0-9\\+\\/]{4}|[a-zA-Z0-9\\+\\/]{3}\\=|[a-zA-Z0-9\\+\\/]{2}\\=\\=)",
      "minimum":8,
      "decode":"base64",
      "unique":true,
      "collect":true
   },
   "hex":{
      "query":"(?:(?:0x|(?:\\\\)+x)[a-fA-F0-9]{2})+|[a-fA-F0-9]+",
      "minimum":12,
      "decode":"hex",
      "unique":true,
      "collect":true
   },
   "cert":{
      "query":"-----BEGIN (?:CERTIFICATE|PRIVATE KEY)-----[\\s\\S]+?-----END (?:CERTIFICATE|PRIVATE KEY)-----",
      "decode":"cert",
      "unique":true,
      "collect":true
   }
}
```

**Make sure your regular expressions return only one capturing group e.g. `[1, 2, 3, 4]`; and not a touple e.g. `[(1, 2), (3, 4)]`.**

Make sure to properly escape regular expression specific symbols in your template file, e.g. make sure to escape dot `.` as `\\.`, and forward slash `/` as `\\/`, etc.

| Name | Type | Required |Description |
| --- | --- | --- | --- |
| query | text | yes | Regular expression query. |
| search | boolean | no | Highlight matches within output; otherwise, extract matches. |
| ignorecase | boolean | no | Case-insensitive search. |
| minimum | integer | no | Show only matches longer than `int` characters. |
| maximum | integer | no | Show only matches lesser than `int` characters. |
| decode | boolean | no | Decode matches. Available decodings: `url`, `base64` `hex`, `cert`. |
| unique | boolean | no | Filter out duplicates. |
| collect | boolean | no | Collect all matches in one place. |

---

How I run the tool most of the time:

```fundamental
file-scraper -d directory -o results.html -e default
```

Default (built-in) exclude file types are as following:

```fundamental
car, css, gif, jpeg, jpg, mp3, mp4, nib, ogg, otf, png, storyboard, strings, svg, ttf, webp, woff, woff2, xib
```

## Usage

```fundamental
File Scraper v2.0 ( github.com/ivan-sincek/file-scraper )

Usage:   file-scraper -d directory -o out          [-t template     ] [-e excludes    ] [-th threads]
Example: file-scraper -d decoded   -o results.html [-t template.json] [-e jpeg,jpg,png] [-th 10     ]

DESCRIPTION
    Scrape files for sensitive information
DIRECTORY
    Directory containing files, or a single file to scrape
    -d <directory> - decoded | files | test.exe | etc.
TEMPLATE
    JSON template file with extraction information, or a single RegEx to use
    Default: built-in JSON template file
    -t <template> - template.json | "secret\: [\w\d]+" | etc.
EXCLUDES
    Exclude files by a file type
    Use comma-separated values
    Specify 'default' to load a built-in list
    -e <excludes> - mp3 | jpeg,jpg,png | default | etc.
INCLUDES
    Include files by a file type
    Use comma-separated values
    Overrides excludes
    -i <includes> - java | json,xml,yaml | etc.
BEAUTIFY
    Beautify [minified] JavaScript (.js) files
    -b <beautify> - yes
THREADS
    Number of parallel threads to run
    Default: 30
    -th <threads> - 10 | etc.
OUT
    Output HTML file
    -o <out> - results.html | etc.
```

## Images

<p align="center"><img src="https://github.com/ivan-sincek/file-scraper/blob/main/img/interactive_report.png" alt="Interactive Report"></p>

<p align="center">Figure 1 - Interactive Report</p>

<p align="center"><img src="https://github.com/ivan-sincek/file-scraper/blob/main/img/certificates.png" alt="Certificates"></p>

<p align="center">Figure 2 - Certificates</p>
