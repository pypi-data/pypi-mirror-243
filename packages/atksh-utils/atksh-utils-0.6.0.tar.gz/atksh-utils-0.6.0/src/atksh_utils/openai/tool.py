import io
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import tokenize
from code import InteractiveConsole
from contextlib import redirect_stderr, redirect_stdout
from itertools import islice
from threading import Lock, Semaphore

import requests
from black import FileMode, format_str
from bs4 import BeautifulSoup as bs4
from duckduckgo_search import DDGS

from .prompt import SEARCH_RESULT_SUMMARIZE_PROMPT, VISIT_PAGE_SUMMARIZE_PROMPT

# Create a temporary directory for storing files to $HOME/.cache/askgpt/
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "askgpt")
os.makedirs(CACHE_DIR, exist_ok=True)
SESSION_PATH = os.path.join(CACHE_DIR, "session.pkl")

Print_LOCK = Lock()
API_LOCK = Semaphore(1)
Python_LOCK = Lock()
Console_LOCK = Lock()
Shell_LOCK = Lock()
UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
PYTHON_PATH = sys.executable


CONSOLE = InteractiveConsole(locals=None)
MAX_ATTEMPTS = 5
MAX_SEARCH_RESULTS = 30
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def remove_comments_and_docstrings(source: str) -> str:
    """
    Returns 'source' minus comments and docstrings.
    """
    io_obj = io.StringIO(source)
    out = []

    prev_token_type = tokenize.INDENT  # Set initial previous token type to INDENT
    last_lineno = -1  # Initialize last_lineno
    last_col = 0

    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok.type
        token_string = tok.string
        start_line, start_col = tok.start
        end_line, end_col = tok.end
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out.append(" " * (start_col - last_col))

        # Ignore comments and docstrings
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_token_type == tokenize.INDENT or (
                start_line == last_lineno and prev_token_type == tokenize.NEWLINE
            ):
                # This is a docstring or a block string; ignore it.
                pass
            else:
                # This is a regular string; keep it.
                out.append(token_string)
        else:
            out.append(token_string)

        prev_token_type = token_type
        last_lineno = end_line
        last_col = end_col

    return "".join(out)


def verbose():
    return os.getenv("ASKGPT_VERBOSE", "0") == "1"


__all__ = [
    "get_browser_functions",
    "exec_python_code",
    "bash",
    "clear_all_python_session",
    "parse_args",
    "cb",
]


def random_sleep():
    for _ in range(3):
        time.sleep(random.uniform(0.1, 1.0))


def parse_args(arguments: str) -> dict:
    try:
        return json.loads(arguments)
    except json.decoder.JSONDecodeError:
        try:
            return json.loads(arguments, strict=False)
        except:
            return arguments


def cb(chunk, _):
    with Print_LOCK:
        light_cyan = "\033[96m"
        reset = "\033[0m"
        if (finish_reason := chunk.choices[0].dict().get("finish_reason")) is not None:
            if finish_reason == "stop":
                print("\n")
        token = chunk.choices[0].delta.content
        if token:
            print(f"{light_cyan}{token}{reset}", end="")


def get_browser_functions(ai: "OpenAI"):
    # visit_page_model_name = "gpt-3.5-turbo-1106"
    visit_page_model_name = ai.model_name

    visit_page_max_context_length = (
        60000 if "gpt-4-1106-preview" in visit_page_model_name else 10000
    )
    visit_page_child = ai.make_child(visit_page_model_name)
    visit_page_child.set_system_prompt(VISIT_PAGE_SUMMARIZE_PROMPT)

    search_result_child = ai.make_child(ai.model_name)
    search_result_child.set_system_prompt(SEARCH_RESULT_SUMMARIZE_PROMPT)

    def _search_summarize(query_text: str, results: str) -> str:
        """Summarizes the query text and results."""
        for i in range(MAX_ATTEMPTS):
            for _ in range(i + 1):
                random_sleep()
            try:
                with API_LOCK:
                    return search_result_child(
                        f"Query: {query_text}\nResults: {results}\nSummary: ",
                        stream_callback=cb if verbose() else None,
                    )[1]
            except Exception as e:
                continue
        return f"Error: {e}.\nPlease try again or try another query."

    def _page_summarize(query_text: str, page: str) -> str:
        """Summarizes the query text and page."""
        for i in range(MAX_ATTEMPTS):
            for _ in range(i + 1):
                random_sleep()
            try:
                with API_LOCK:
                    return visit_page_child(
                        f"Query: {query_text}\nPage: {page}\nSummary: ",
                        stream_callback=cb if verbose() else None,
                    )[1]
            except Exception as e:
                continue
        return f"Error: {e}.\nPlease try again or try another url or wait for a while."

    def web_search(query_text: str, lang: None | str = None) -> str:
        """Searches the web for the query text.

        :param query_text: The keywords to query. For example, `The capital of Japan` or `首都 日本`.
        :type query_text: str
        :param lang: The language of the query text. `en` or `ja` is supported. If None, the language is automatically detected.
        :type lang: str, optional
        :return: json dumped results (string)
        :rtype: str
        """
        attempts = 0
        search_results = []
        if lang is None:
            region = None
        elif lang == "en":
            region = "us-en"
        elif lang == "ja":
            region = "ja-ja"
        else:
            return "Error: lang must be either 'en' or 'ja'."
        while attempts < MAX_ATTEMPTS:
            ddgs = DDGS()
            time.sleep(1.5 + attempts)
            random_sleep()
            result = ddgs.text(query_text, region=region, safesearch="Off")
            search_results = list(islice(result, MAX_SEARCH_RESULTS))
            if search_results:
                break
            attempts += 1

        results = json.dumps(search_results, ensure_ascii=False, indent=2)
        ret = _search_summarize(query_text, results)
        return ret

    def visit_page(query_text: str, url: str) -> str:
        """Visits the page at the url and summarizes the text with respect to the query text. Recommended to use after web_search for each url.

        :param query_text: The text to query for summarization.
        :type query_text: str
        :param url: The url to visit (must be a valid url like `https://www.google.com`).
        :type url: str
        :return: The summarized text of the page.
        :rtype: str
        """
        try:
            random_sleep()
            response = requests.get(url, timeout=15, headers={"User-Agent": UserAgent})
            soup = bs4(response.text, "html.parser")
            body = soup.find("body").text.strip()
            ret = _page_summarize(query_text, body[:visit_page_max_context_length])
        except Exception as e:
            ret = f"Error: {e}.\nPlease try again or try another url."
        return ret

    return web_search, visit_page


def run_pyhton_with_session(code: str) -> str:
    """This is a function that executes Python code and returns the stdout. Don't forget to print the result.

    :param code: Python code of multiple lines. You must print the result. For example, `value = 2 + 3; print(value)`.
    :type code: str
    :return: stdout of running the Python code.
    :rtype: str
    """
    lines = code.split("\n")
    lines = ["    " + line for line in lines]
    code = "\n".join(lines)
    result = ""
    with Python_LOCK, io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        out = None
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py") as f:
            try:
                f.write("import traceback\n")
                f.write("import dill\n")
                f.write(f"try:\n    dill.load_session('{SESSION_PATH}')\nexcept:\n    pass\n")
                f.write("\n\n\n")
                f.write("try:\n")
                f.write(code)
                f.write(
                    "\nexcept Exception as e:\n    print(f'ERROR: {traceback.format_exc()}')\n    print('\\n\\n\\n')\n"
                )
                f.write("else:\n    print('\\n\\n\\nThe code is executed successfully.')\n")
                f.write("    print('The following is the system message about session.')\n")
                f.write(
                    f"\ntry:\n    dill.dump_session('{SESSION_PATH}')\nexcept Exception as e:"
                    "\n    print('[SYSTEM INFO]: Failed to save this session:', str(e))\n"
                    "else:\n    print('[SYSTEM INFO]: Saved this session.')\n"
                )
                f.flush()
                out = subprocess.check_output(f"{PYTHON_PATH} {f.name}", shell=True, text=True)
            except Exception as e:
                result += f"Error: {str(e)}.\nPlease try again.\n"
            if out == "":
                result += "NotPrintedError('The result is not printed.')\nPlease print the result in your code."
            elif out is not None:
                result += out
            result += ANSI_ESCAPE.sub("", buf.getvalue())
            result = result.strip()
    if verbose():
        print("=== Run Python Code ===")
        print(result)
        print("=======================")
    return result


def python_code_interpreter(code: str) -> str:
    """Run the given Python source code and return the result.

    :param code: Python source code. For example, `"import numpy as np\nnp.array([1, 2, 3])"`.
    :type code: str
    :return: The result of the execution of the Python source code. For example, `array([1, 2, 3])`.
    :rtype: str
    """
    global CONSOLE
    result = ""
    try:
        with io.StringIO() as buf, redirect_stdout(buf):
            for line in code.split("\n"):
                more = CONSOLE.push(line)
                if not more:
                    result = buf.getvalue()
                    buf.truncate(0)
                    buf.seek(0)
    except Exception as e:
        result = f"Error: {e}.\nPlease try again."
    result = ANSI_ESCAPE.sub("", result)
    result = result.strip()
    if verbose():
        print("=== Python Code Interpreter ===")
        print(result)
        print("===============================")
    return result


def bash(command: str) -> str:
    """Execute the given command and return the result.

    :param command: The command to execute. For example, `ls -l`.
    :type command: str
    :return: The result of the execution of the command.
    :rtype: str
    """
    with Shell_LOCK:
        try:
            ret = subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            output = e.output
            ret = f"Error: return_code={return_code}, output={output}"
        except Exception as e:
            ret = f"Error: {e}.\nPlease try again or try another command."
    ret = ANSI_ESCAPE.sub("", str(ret)).strip()
    if verbose():
        print("=== Bash ===")
        print(ret)
        print("============")
    return ret


def pip_install(command: str) -> str:
    """Install the given package with pip and return the result. Use this if and only if you encounter an error with `import`.

    :param command: The packages to install. For example, `numpy pandas`.
    :type command: str
    :return: The result of the installation of the package.
    :rtype: str
    """
    with Shell_LOCK:
        try:
            ret = subprocess.check_output(f"{PYTHON_PATH} -m pip install {command}", shell=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            output = e.output
            ret = f"Error: return_code={return_code}, output={output}"
        except Exception as e:
            ret = f"Error: {e}.\nPlease try again or try another command."
    ret = ANSI_ESCAPE.sub("", str(ret)).strip()
    if verbose():
        print("=== Pip Install ===")
        print(ret)
        print("===================")
    return ret


def clear_all_python_session():
    """Clears the exec_python_code session.

    :return: True if the session is cleared successfully.
    :rtype: bool
    """
    try:
        if os.path.exists(SESSION_PATH):
            os.remove(SESSION_PATH)
        return True
    except:
        return False
