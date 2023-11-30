#!/usr/bin/env python3

import datetime, sys, os, json, jq, regex as re, base64, threading, concurrent.futures, subprocess, urllib.parse, bs4, jsbeautifier
from cryptography import x509
import OpenSSL.crypto

start = datetime.datetime.now()

# ----------------------------------------

def unique(sequence):
	seen = set()
	return [x for x in sequence if not (x in seen or seen.add(x))]

def check_directory_files(directory):
	tmp = []
	for path, dirs, files in os.walk(directory):
		for file in files:
			file = os.path.join(path, file)
			if os.path.isfile(file) and os.access(file, os.R_OK) and os.stat(file).st_size > 0:
				tmp.append(file)
	return tmp

def validate_template_reject(obj):
	for key in obj:
		for subkey in obj[key]:
			if subkey not in ["query", "search", "ignorecase", "minimum", "maximum", "decode", "unique", "collect"]:
				obj[key].pop(subkey, None)
	return obj

def validate_template_query(obj):
	subkey = "query"
	for key in obj:
		if subkey not in obj[key] and not isinstance(obj[key][subkey], str) or len(obj[key][subkey]) < 1:
			obj.pop(key, None)
	return obj

def validate_template_search(obj):
	subkey = "search"
	for key in obj:
		if subkey in obj[key]:
			if not isinstance(obj[key][subkey], bool) or obj[key][subkey] != True:
				obj[key].pop(subkey, None)
			else:
				const = ".*"
				obj[key][subkey] = const + obj[key]["query"].strip(const) + const
	return obj

def validate_template_ignorecase(obj):
	subkey = "ignorecase"
	for key in obj:
		if subkey in obj[key]:
			if not isinstance(obj[key][subkey], bool) or obj[key][subkey] != True:
				obj[key].pop(subkey, None)
	return obj

def validate_template_min_max(obj):
	for subkey in ["minimum", "maximum"]:
		for key in obj:
			if subkey in obj[key]:
				if not isinstance(obj[key][subkey], int) or obj[key][subkey] < 1:
					obj[key].pop(subkey, None)
	return obj

def validate_template_decode(obj):
	subkey = "decode"
	for key in obj:
		if subkey in obj[key]:
			if not isinstance(obj[key][subkey], str) or len(obj[key][subkey]) < 1 or obj[key][subkey].lower() not in ["url", "base64", "hex", "cert"]:
				obj[key].pop(subkey, None)
			else:
				obj[key][subkey] = obj[key][subkey].lower()
	return obj

def validate_template_unique(obj):
	subkey = "unique"
	for key in obj:
		if subkey in obj[key]:
			if not isinstance(obj[key][subkey], bool) or obj[key][subkey] != True:
				obj[key].pop(subkey, None)
	return obj

def validate_template_collect(obj):
	subkey = "collect"
	for key in obj:
		if subkey in obj[key]:
			if not isinstance(obj[key][subkey], bool) or obj[key][subkey] != True:
				obj[key].pop(subkey, None)
	return obj

def validate_template_all(obj):
	obj = validate_template_reject(obj)
	obj = validate_template_query(obj)
	obj = validate_template_search(obj)
	obj = validate_template_ignorecase(obj)
	obj = validate_template_min_max(obj)
	obj = validate_template_decode(obj)
	obj = validate_template_unique(obj)
	obj = validate_template_collect(obj)
	return obj

encoding = "ISO-8859-1"

def read_json(file, validate = True):
	tmp = []
	try:
		tmp = json.loads(open(file, "r", encoding = encoding).read())
	except json.decoder.JSONDecodeError:
		pass
	if validate and tmp:
		tmp = validate_template_all(tmp)
	return tmp

def jquery(obj, query):
	tmp = []
	try:
		tmp = jq.compile(query).input(obj).all()
	except ValueError:
		pass
	return tmp

def jdump(data):
	return json.dumps(data, indent = 4, ensure_ascii = False)

def write_file(data, out):
	confirm = "yes"
	if os.path.isfile(out):
		print(("'{0}' already exists").format(out))
		confirm = input("Overwrite the output file (yes): ")
	if confirm.lower() == "yes":
		try:
			open(out, "w").write(data)
			print(("Results have been saved to '{0}'").format(out))
		except FileNotFoundError:
			print(("Cannot save results to '{0}'").format(out))

# ----------------------------------------

class FileScraper:

	def __init__(
		self,
		files,
		template,
		beautify,
		threads,
		out
	):
		self.__files      = files
		self.__template   = template
		self.__out        = out
		self.__beautify   = beautify
		self.__threads    = threads
		self.__print_lock = threading.Lock()
		self.__res_enc    = "ISO-8859-1"
		self.__url_enc    = "UTF-8"
		self.__highlight  = {
			"matched": "file-scraper-matched",
			"decoded": "file-scraper-decoded"
		}
		self.__soup       = None
		self.__results    = []

	def run(self):
		print(("Files to scrape: {0}").format(len(self.__files)))
		print("Press CTRL + C to exit early - results will be saved")
		with concurrent.futures.ThreadPoolExecutor(max_workers = self.__threads) as executor:
			subprocesses = []
			try:
				for file in self.__files:
					subprocesses.append(executor.submit(self.__run, file))
				for subprocess in concurrent.futures.as_completed(subprocesses):
					result = subprocess.result()
					if isinstance(result, dict) and "file" in result:
						print(result["file"])
						self.__results.append(result)
			except KeyboardInterrupt:
				executor.shutdown(wait = True, cancel_futures = True)
		if not self.__results:
			print("No results")
		else:
			self.__results = jquery(self.__results, "sort_by(.file | ascii_downcase)[]")
			self.__set_html_content()
			write_file(self.__soup, self.__out)

	def __run(self, file):
		response = None
		try:
			if self.__beautify and file.endswith(".js"):
				data = jsbeautifier.beautify_file(file)
				open(file, "w").write(data)
			response = subprocess.run(("rabin2 -zzzqq '{0}'").format(file), shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT).stdout
			if response:
				response = response.decode(self.__res_enc).replace("\\n", "\n")
				response = self.__grep(response)
				if response:
					response = {"file": file, "matched": response}
		except Exception as ex:
			response = None
			self.__print(ex)
		return response

	def __grep(self, response):
		tmp = {}
		for key in self.__template:
			subtemplate = self.__template[key]
			flags = re.MULTILINE | (re.IGNORECASE if "ignorecase" in subtemplate else 0)
			try:
				if "search" in subtemplate:
					# --------------------
					array = []
					searched = re.findall(subtemplate["search"], response, flags)
					if searched:
						if "unique" in subtemplate:
							searched = unique(searched)
						for i in range(len(searched)):
							results = {"matched": unique(re.findall(subtemplate["query"], searched[i], flags)), "decoded": []}
							if results["matched"]:
								if any(subkey in ["minimum", "maximum", "decode"] for subkey in subtemplate):
									results = self.__validate_matched(results["matched"], subtemplate)
								if results["matched"]:
									for j in range(len(results["matched"])):
										searched[i] = searched[i].replace(results["matched"][j], ("<{0}>{1}</{0}>").format(self.__highlight["matched"], results["matched"][j])).strip()
									for j in range(len(results["decoded"])):
										searched[i] += ("\n<{0}>{1}</{0}>").format(self.__highlight["decoded"], results["decoded"][j])
									array.append(searched[i])
						if array:
							tmp[key] = array
					# --------------------
				else:
					# --------------------
					results = {"matched": re.findall(subtemplate["query"], response, flags), "decoded": []}
					if "unique" in subtemplate:
						results["matched"] = unique(results["matched"])
					if any(subkey in ["minimum", "maximum", "decode"] for subkey in subtemplate):
						results = self.__validate_matched(results["matched"], subtemplate)
					if results["matched"]:
						for i in range(len(results["decoded"])):
							results["matched"][i] += ("\n<{0}>{1}</{0}>").format(self.__highlight["decoded"], results["decoded"][i])
						tmp[key] = results["matched"]
					# --------------------
			except Exception as ex:
				self.__print(ex)
		return tmp

	def __validate_matched(self, matched, subtemplate):
		tmp = {"matched": [], "decoded": []}
		for match in matched:
			length = len(match)
			if ("minimum" in subtemplate and length < subtemplate["minimum"]) or ("maximum" in subtemplate and length > subtemplate["maximum"]):
				continue
			if "decode" in subtemplate:
				try:
					decoded = ""
					if subtemplate["decode"] == "url":
						decoded = urllib.parse.unquote(match, encoding = self.__url_enc)
						decoded = self.__replace(decoded, binary = False)
					elif subtemplate["decode"] == "base64":
						decoded = base64.b64decode(match)
						decoded = self.__replace(decoded, binary = True)
					elif subtemplate["decode"] == "hex":
						decoded = bytes.fromhex(match.replace("0x", "").replace("\\", "").replace("x", ""))
						decoded = self.__replace(decoded, binary = True)
						match = match.replace("\\\\", "\\")
					elif subtemplate["decode"] == "cert":
						if "CERTIFICATE" in match.upper():
							decoded = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, match)
							decoded = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_TEXT, decoded)
						else:
							decoded = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, match)
							decoded = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_TEXT, decoded)
						decoded = self.__replace(decoded, binary = True)
					if decoded:
						tmp["decoded"].append(decoded)
						tmp["matched"].append(match)
				except Exception:
					continue
		return tmp

	def __replace(self, string, binary = False):
		if binary:
			return string.replace(b"\x00", b"").replace(b"\r", b"").decode(self.__url_enc).strip()
		else:
			return string.replace("\x00", "").replace("\r", "").strip()

	def __set_html_content(self):
		self.__soup = """
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="UTF-8">
				<title></filename> | File Scraper</title>
				<meta name="author" content="Ivan Šincek">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<style>
					html {
						height: 100%;
					}
					body {
						background-color: #F8F8F8;
						margin: 0;
						height: inherit;
						color: #262626;
						font-family: "Fira Code Medium", sans-serif;
						font-size: 0.8em;
						font-weight: 400;
						text-align: left;
						word-break: break-all;
					}
					nav {
						right: 0;
						bottom: 0;
						position: fixed;
						z-index: 3301;
					}
					ul {
						display: flex;
						flex-wrap: wrap;
						margin: 0;
						padding: 0;
						list-style-type: none;
					}
					div {
						/* display: flex; */
						flex-direction: column;
						padding: 1em;
					}
					div.modal {
						top: 0;
						right: 0;
						bottom: 0;
						left: 0;
						position: fixed;
					}
					a {
						text-decoration: none;
					}
					h2 {
						margin: 0.8em 0 0.2em 0;
						color: #717171;
						font-size: inherit;
						cursor: pointer;
						font-weight: inherit;
					}
					button {
						/* display: block; */
						background-color: #C8C8C8;
						padding: 0.2em 0.4em;
						color: inherit;
						font-family: inherit;
						font-size: inherit;
						text-transform: lowercase;
						text-align: inherit;
						cursor: pointer;
						border: 0.07em solid #B8B8B8;
					}
					pre {
						/* display: block; */
						background-color: #E8E8E8;
						margin: 0;
						padding: 0.2em;
						font-family: inherit;
						font-size: 1em;
						white-space: pre-wrap;
						border: 0.07em solid #B8B8B8;
					}	
					div.modal pre {
						/* display: none; */
						height: 100%;
						overflow-y: scroll;
					}	
					span.matched {
						color: #FF1919;
					}
					span.decoded {
						color: #1919FF;
					}
				</style>
			</head>
			<body>
				<nav>
					<ul>
						<li>
							<button onclick="collapse_all()">Hide All</button>
						</li>
						<li>
							<button onclick="uncollapse_all()">Show All</button>
						</li>
					</ul>
				</nav>
				<div style="display: flex;">
					<a href="https://github.com/ivan-sincek/file-scraper">https://github.com/ivan-sincek/file-scraper</a>
				</div>
				<div class="modal" style="display: none;"></div>
				<script>
					const nav_main = document.getElementsByTagName('nav')[0];
					const nav_main_buttons = nav_main.getElementsByTagName('button');
					// --------------------
					const div_main = document.getElementsByTagName('div')[0];
					const div_main_headers = div_main.getElementsByTagName('h2');
					const div_main_buttons = div_main.getElementsByTagName('button');
					const div_main_pres = div_main.getElementsByTagName('pre');
					// --------------------
					const div_modal = document.getElementsByTagName('div')[1];
					const div_modal_pres = div_modal.getElementsByTagName('pre');
					// --------------------
					const button_inactive = '#C8C8C8';
					const button_active = '#64C76A';
					// --------------------
					for (let i = 0; i < div_main_buttons.length; i++) {
						div_main_buttons[i].addEventListener('click', function() {
							div_main_pres[i].style.display = div_main_pres[i].style.display !== 'none' ? 'none' : 'block';
						});
					}
					// --------------------
					function set_file_method(button) {
						let header = button.previousElementSibling;
						while (header && header.tagName !== 'H2') {
							header = header.previousElementSibling;
						}
						if (button.style.display !== 'none') {
							header.setAttribute('onclick', 'collapse_file(this)');
						} else {
							header.setAttribute('onclick', 'uncollapse_file(this)');
							let next = header.nextElementSibling;
							while (next && next.tagName !== 'H2') {
								if (next.style.display !== 'none') {
									header.setAttribute('onclick', 'collapse_file(this)');
									break;
								}
								next = next.nextElementSibling;
							}
						}
					}
					function modify_file(header, display, method) {
						let next = header.nextElementSibling;
						while (next && next.tagName !== 'H2') {
							next.style.display = display;
							next = next.nextElementSibling;
						}
						header.setAttribute('onclick', method);
					}
					function collapse_file(header) {
						modify_file(header, 'none', 'uncollapse_file(this)');
					}
					function uncollapse_file(header) {
						modify_file(header, 'block', 'collapse_file(this)');
					}
					// --------------------
					function hide_modal() {
						div_modal.style.display = 'none';
						for (let i = 0; i < div_modal_pres.length; i++) {
							div_modal_pres[i].style.display = 'none';
						}
						for (let i = nav_main_buttons.length - div_modal_pres.length; i < nav_main_buttons.length; i++) {
							nav_main_buttons[i].style.backgroundColor = button_inactive;
						}
					}
					// --------------------
					function modify_all(display, method_file, method_nav, color) {
						div_main.style.display = 'flex';
						for (let i = 0; i < div_main_headers.length; i++) {
							div_main_headers[i].setAttribute('onclick', method_file);
						}
						for (let i = 0; i < div_main_buttons.length; i++) {
							div_main_buttons[i].style.display = div_main_pres[i].style.display = display
						}
						for (let i = 2; i < nav_main_buttons.length - div_modal_pres.length; i++) {
							nav_main_buttons[i].setAttribute('onclick', method_nav);
							nav_main_buttons[i].style.backgroundColor = color;
						}
						hide_modal();
					}
					function collapse_all() {
						modify_all('none', 'uncollapse_file(this)', 'uncollapse_single(this)', button_inactive);
					}
					function uncollapse_all() {
						modify_all('block', 'collapse_file(this)', 'collapse_single(this)', button_active);
					}
					// --------------------
					function modify_single(button, display, method, color) {
						div_main.style.display = 'flex';
						for (let i = 0; i < div_main_buttons.length; i++) {
							if (div_main_buttons[i].className === button.className) {
								div_main_buttons[i].style.display = div_main_pres[i].style.display = display;
								set_file_method(div_main_buttons[i]);
							}
						}
						button.setAttribute('onclick', method);
						button.style.backgroundColor = color;
						hide_modal();
					}
					function collapse_single(button) {
						modify_single(button, 'none', 'uncollapse_single(this)', button_inactive);
					}
					function uncollapse_single(button) {
						modify_single(button, 'block', 'collapse_single(this)', button_active);
					}
					// --------------------
					function pop_modal(button) {
						for (let i = nav_main_buttons.length - div_modal_pres.length; i < nav_main_buttons.length; i++) {
							nav_main_buttons[i].style.backgroundColor = button_inactive;
						}
						for (let i = 0; i < div_modal_pres.length; i++) {
							if (div_modal_pres[i].className !== button.className) {
								div_modal_pres[i].style.display = 'none';
							} else if (div_modal_pres[i].style.display !== 'none') {
								div_modal.style.display = 'none';
								div_modal_pres[i].style.display = 'none';
								div_main.style.display = 'flex';
							} else {
								div_modal.style.display = 'flex';
								div_modal_pres[i].style.display = 'block';
								button.style.backgroundColor = button_active;
								div_main.style.display = 'none';
							}
						}
					}
				</script>
			</body>
		</html>
		"""
		print(("Files with valid results: {0}").format(len(self.__results)))
		print("Generating report...")
		self.__soup = self.__soup.replace("</filename>", self.__out.rsplit(os.path.sep)[-1], 1)
		self.__soup = bs4.BeautifulSoup(self.__soup, "html.parser")
		for result in self.__results:
			self.__add_header(result["file"])
			for key in result["matched"]:
				self.__add_results(key, ("\n").join(result["matched"][key]))
		for key in self.__template:
			if "collect" in self.__template[key]:
				tmp = []
				for array in jquery(self.__results, (".[].matched.\"{0}\" | select(. != null)").format(key)):
					tmp.extend(array)
				if tmp:
					self.__add_collection(key, ("\n").join(sorted(unique(tmp), key = str.casefold)))
		self.__soup = self.__soup.prettify()
		for key in self.__highlight:
			self.__soup = self.__soup.replace(("&lt;{0}&gt;").format(self.__highlight[key]), ("<span class=\"{0}\">").format(key))
			self.__soup = self.__soup.replace(("&lt;/{0}&gt;").format(self.__highlight[key]), "</span>")

	def __add_header(self, filename):
		attributes = {"onclick": "collapse_file(this)"}
		h2 = self.__soup.new_tag("h2", **attributes)
		h2.string = filename
		self.__soup.html.body.find_all("div")[0].append(h2)

	def __add_results(self, key, results):
		attributes = {"class": key, "onclick": "collapse_single(this)", "style": "background-color: #64C76A;"}
		if not self.__soup.html.body.nav.ul.find_all("button", attributes):
			button = self.__soup.new_tag("button", **attributes)
			button.string = key
			li = self.__soup.new_tag("li")
			li.append(button)
			self.__soup.html.body.nav.ul.append(li)
		# --------------------
		attributes = {"class": key, "style": "display: block;"}
		button = self.__soup.new_tag("button", **attributes)
		button.string = key
		self.__soup.html.body.find_all("div")[0].append(button)
		# --------------------
		attributes = {"style": "display: block;"}
		pre = self.__soup.new_tag("pre", **attributes)
		pre.string = results
		self.__soup.html.body.find_all("div")[0].append(pre)

	def __add_collection(self, key, collection):
		attributes = {"class": key, "onclick": "pop_modal(this)", "style": "background-color: #C8C8C8;"}
		if not self.__soup.html.body.nav.ul.find_all("button", attributes):
			button = self.__soup.new_tag("button", **attributes)
			button.string = key + " all"
			li = self.__soup.new_tag("li")
			li.append(button)
			self.__soup.html.body.nav.ul.append(li)
		# --------------------
		attributes = {"class": key, "style": "display: none;"}
		pre = self.__soup.new_tag("pre", **attributes)
		pre.string = collection
		self.__soup.html.body.find_all("div")[1].append(pre)

	def __print(self, msg):
		with self.__print_lock:
			print(msg)

# ----------------------------------------

# my own validation algorithm

class Validate:

	def __init__(self):
		self.__proceed = True
		self.__args    = {
			"directory": None,
			"template" : None,
			"excludes" : None,
			"includes" : None,
			"beautify" : None,
			"threads"  : None,
			"out"      : None
		}

	def __basic(self):
		self.__proceed = False
		print("File Scraper v2.0 ( github.com/ivan-sincek/file-scraper )")
		print("")
		print("Usage:   file-scraper -d directory -o out          [-t template     ] [-e excludes    ] [-th threads]")
		print("Example: file-scraper -d decoded   -o results.html [-t template.json] [-e jpeg,jpg,png] [-th 10     ]")

	def __advanced(self):
		self.__basic()
		print("")
		print("DESCRIPTION")
		print("    Scrape files for sensitive information")
		print("DIRECTORY")
		print("    Directory containing files, or a single file to scrape")
		print("    -d <directory> - decoded | files | test.exe | etc.")
		print("TEMPLATE")
		print("    JSON template file with extraction information, or a single RegEx to use")
		print("    Default: built-in JSON template file")
		print("    -t <template> - template.json | \"secret\\: [\\w\\d]+\" | etc.")
		print("EXCLUDES")
		print("    Exclude files by a file type")
		print("    Use comma-separated values")
		print("    Specify 'default' to load a built-in list")
		print("    -e <excludes> - mp3 | jpeg,jpg,png | default | etc.")
		print("INCLUDES")
		print("    Include files by a file type")
		print("    Use comma-separated values")
		print("    Overrides excludes")
		print("    -i <includes> - java | json,xml,yaml | etc.")
		print("BEAUTIFY")
		print("    Beautify [minified] JavaScript (.js) files")
		print("    -b <beautify> - yes")
		print("THREADS")
		print("    Number of parallel threads to run")
		print("    Default: 30")
		print("    -th <threads> - 10 | etc.")
		print("OUT")
		print("    Output HTML file")
		print("    -o <out> - results.html | etc.")

	def __print_error(self, msg):
		print(("ERROR: {0}").format(msg))

	def __error(self, msg, help = False):
		self.__proceed = False
		self.__print_error(msg)
		if help:
			print("Use -h for basic and --help for advanced info")

	def __build_template(self, query):
		const = ".*"
		return {
			"query": {
				"query": query,
				"ignorecase": True,
				"search": const + query.strip(const) + const,
				"collect": True
			}
		}

	def __load_default_template(self):
		file = os.path.join(os.path.abspath(os.path.split(__file__)[0]), "default.json")
		if os.path.isfile(file) and os.access(file, os.R_OK) and os.stat(file).st_size > 0:
			self.__args["template"] = read_json(file)
		if not self.__args["template"]:
			self.__error("Cannot load the default JSON template file")

	def __parse_excludes(self, value, special):
		tmp = []
		const = "."
		for entry in value.split(","):
			entry = entry.strip()
			if not entry:
				continue
			elif entry == special: # default
				tmp.extend([const + e for e in ["car", "css", "gif", "jpeg", "jpg", "mp3", "mp4", "nib", "ogg", "otf", "png", "storyboard", "strings", "svg", "ttf", "webp", "woff", "woff2", "xib"]])
			else:
				entry = entry.lstrip(const)
				if entry:
					tmp.append(const + entry)
		return unique(tmp)

	def __parse_includes(self, value):
		tmp = []
		const = "."
		for entry in value.split(","):
			entry = entry.strip().lstrip(const)
			if entry:
				tmp.append(const + entry)
		return unique(tmp)

	def __exclude_files(self):
		tmp = []
		for file in self.__args["directory"]:
			if not any(file.endswith(exclude) for exclude in self.__args["excludes"]):
				tmp.append(file)
		if not tmp:
			self.__error("No valid files were found")
		self.__args["directory"] = tmp

	def __include_files(self):
		tmp = []
		for file in self.__args["directory"]:
			if any(file.endswith(exclude) for exclude in self.__args["includes"]):
				tmp.append(file)
		if not tmp:
			self.__error("No valid files were found")
		self.__args["directory"] = tmp

	def __validate(self, key, value):
		value = value.strip()
		if len(value) > 0:
			# --------------------
			if key == "-d" and self.__args["directory"] is None:
				self.__args["directory"] = value
				if not os.path.exists(self.__args["directory"]):
					self.__error("Directory containing files, or a single file does not exists")
				elif os.path.isdir(self.__args["directory"]):
					self.__args["directory"] = check_directory_files(self.__args["directory"])
					if not self.__args["directory"]:
						self.__error("No valid files were found")
				else:
					if not os.access(self.__args["directory"], os.R_OK):
						self.__error("File does not have read permission")
					elif not os.stat(self.__args["directory"]).st_size > 0:
						self.__error("File is empty")
					else:
						self.__args["directory"] = [self.__args["directory"]]
			# --------------------
			elif key == "-t" and self.__args["template"] is None:
				self.__args["template"] = value
				if os.path.isfile(self.__args["template"]):
					if not os.access(self.__args["template"], os.R_OK):
						self.__error("Template file does not have read permission")
					elif not os.stat(self.__args["template"]).st_size > 0:
						self.__error("Template file is empty")
					else:
						self.__args["template"] = read_json(self.__args["template"])
						if not self.__args["template"]:
							self.__error("Template file has invalid JSON format")
				else:
					self.__args["template"] = self.__build_template(self.__args["template"])
			# --------------------
			elif key == "-e" and self.__args["excludes"] is None:
				self.__args["excludes"] = self.__parse_excludes(value.lower(), "default")
				if not self.__args["excludes"]:
					self.__error("No valid exclude file types were found")
			# --------------------
			elif key == "-i" and self.__args["includes"] is None:
				self.__args["includes"] = self.__parse_includes(value.lower())
				if not self.__args["includes"]:
					self.__error("No valid include file types were found")
			# --------------------
			elif key == "-b" and self.__args["beautify"] is None:
				self.__args["beautify"] = value.lower()
				if self.__args["beautify"] != "yes":
					self.__error("Specify 'yes' to beautify JavaScript files")
			# --------------------
			elif key == "-th" and self.__args["threads"] is None:
				self.__args["threads"] = value
				if not self.__args["threads"].isdigit():
					self.__error("Number of parallel files to download must be numeric")
				else:
					self.__args["threads"] = int(self.__args["threads"])
					if self.__args["threads"] < 1:
						self.__error("Number of parallel files to download must be greater than zero")
			# --------------------
			elif key == "-o" and self.__args["out"] is None:
				self.__args["out"] = value
			# --------------------

	def __check(self, argc):
		count = 0
		for key in self.__args:
			if self.__args[key] is not None:
				count += 1
		return argc - count == argc / 2

	def run(self):
		# --------------------
		argc = len(sys.argv) - 1
		# --------------------
		if argc == 0:
			self.__advanced()
		# --------------------
		elif argc == 1:
			if sys.argv[1] == "-h":
				self.__basic()
			elif sys.argv[1] == "--help":
				self.__advanced()
			else:
				self.__error("Incorrect usage", True)
		# --------------------
		elif argc % 2 == 0 and argc <= len(self.__args) * 2:
			for i in range(1, argc, 2):
				self.__validate(sys.argv[i], sys.argv[i + 1])
			if self.__args["directory"] is None or self.__args["out"] is None or not self.__check(argc):
				self.__error("Missing a mandatory option (-d, -o) and/or optional (-t, -e, -i, -b, -th)", True)
		# --------------------
		else:
			self.__error("Incorrect usage", True)
		# --------------------
		if self.__proceed:
			if not self.__args["template"]:
				self.__load_default_template()
			if self.__args["excludes"] and not self.__args["includes"]:
				self.__exclude_files()
			if self.__args["includes"]:
				self.__include_files()
			if not self.__args["threads"]:
				self.__args["threads"] = 30
		# --------------------
		return self.__proceed
		# --------------------

	def get_arg(self, key):
		return self.__args[key]

# ----------------------------------------

def main():
	validate = Validate()
	if validate.run():
		print("###########################################################################")
		print("#                                                                         #")
		print("#                            File Scraper v2.0                            #")
		print("#                                    by Ivan Sincek                       #")
		print("#                                                                         #")
		print("# Scrape files for sensitive information.                                 #")
		print("# GitHub repository at github.com/ivan-sincek/file-scraper.               #")
		print("# Feel free to donate ETH at 0xbc00e800f29524AD8b0968CEBEAD4cD5C5c1f105.  #")
		print("#                                                                         #")
		print("###########################################################################")
		file_scraper = FileScraper(
			validate.get_arg("directory"),
			validate.get_arg("template"),
			validate.get_arg("beautify"),
			validate.get_arg("threads"),
			validate.get_arg("out")
		)
		file_scraper.run()
		print(("Script has finished in {0}").format(datetime.datetime.now() - start))

if __name__ == "__main__":
	main()
