import os
import re
import shutil
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import IO
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import yaml

from . import __version__, util

ROOT = Path(__file__).absolute().parent


@dataclass
class Library:
    variables: set[str]
    loopvariables: set[str]
    calls: set[str]
    # if true, accumulate everything found to library
    teaching: bool


# aggregate full report here
full_report: dict[str, int] = {}


# ruff lead this alone man
emit = print


def do_import(fnames: str) -> None:
    target_dir = get_app_local_dir()
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    for f in fnames:
        if f.startswith("http"):
            lastpart = f.split("/")[-1]
            emit(lastpart)

            if not lastpart.endswith(".zip"):
                lastpart = "downloaded.zip"
            tfile = Path(target_dir) / lastpart
            emit("Fething:", f, "->", tfile)
            urllib.request.urlretrieve(f, tfile)
        elif f.endswith(".zip"):
            emit("Copying:", f, "->", target_dir)
            shutil.copy(f, target_dir)
        else:
            emit("Not a zip file:", f)


def get_app_local_dir() -> Path:
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "anyerplint"
    raise Exception("Could not find LOCALAPPDATA")


def do_check(
    libs: list[str],
    targets: list[str],
    teaching: bool,
    nostdlib: bool = False,
) -> dict[str, str | dict[str, list[str]]]:
    emit(f"AnyErpLintVersion: {__version__.strip()}")

    lib_vars = Library(
        variables=set(),
        calls=set(),
        teaching=teaching,
        loopvariables=set(),
    )

    # always feed the "standard library, except when unit testing (nostdlib)

    if not nostdlib:
        local_app_data = get_app_local_dir()
        feed_lib(lib_vars, local_app_data)

    for lib in libs:
        feed_lib(lib_vars, Path(lib))

    has_errors = False
    all_errors: dict[str, str | dict[str, list[str]]] = {}
    for target in targets:
        if os.path.isdir(target):
            errs = check_dir(lib_vars, Path(target))
        else:
            assert target.lower().endswith(".xml")
            try:
                r = parse_file(target, teaching)
            except (ElementTree.ParseError, PermissionError, UnicodeDecodeError) as e:
                all_errors[target] = report_fatal(Path(target), e)
                has_errors = True
                continue
            error_report = report(lib_vars, target, r)
            errs = {target: error_report} if error_report else {}
        if errs:
            all_errors.update(errs)
            has_errors = True

    if lib_vars.teaching:
        emit("Writing found function to:")

        def write_file(fname: Path, lines: list[str]) -> None:
            emit("  - ", fname)
            f = open(fname, "wb")
            for line in lines:
                try:
                    enc = line.strip().encode()
                except UnicodeEncodeError:
                    # skip bad lines for now
                    ...
                f.write(enc)
                f.write(b"\n")

        stdlib = get_app_local_dir()
        functions_file = stdlib / "builtin_calls.txt"
        write_file(functions_file, sorted(lib_vars.calls))

        vars_file = stdlib / "builtin_vars.txt"
        write_file(vars_file, sorted(lib_vars.variables))

        loopvars_file = stdlib / "builtin_loopvars.txt"
        write_file(loopvars_file, sorted(lib_vars.loopvariables))

    if has_errors:
        emit("Errors found: >")
        rep = sorted((k, v) for (k, v) in full_report.items())
        for line in rep:
            emit("  ", line[0], ";", line[1])

    return all_errors


def feed_lib(lib_vars: Library, libdir: Path) -> None:
    def feed_set(set: set[str], fobj: IO[bytes]) -> None:
        set.update(line.decode().strip() for line in fobj.readlines())

    def visit_file(fname: str, fobj: IO[bytes]) -> None:
        if fname.endswith("_calls.txt"):
            feed_set(lib_vars.calls, fobj)
        elif fname.endswith("_vars.txt"):
            feed_set(lib_vars.variables, fobj)
        elif fname.endswith("_loopvars.txt"):
            feed_set(lib_vars.loopvariables, fobj)

    if not libdir.exists():
        return

    # files on file system
    for p in libdir.glob("*_*.txt"):
        visit_file(str(p), p.open("rb"))

    # files in all the zip files
    for f in libdir.glob("*.zip"):
        zf = zipfile.ZipFile(f, "r")
        for zn in zf.namelist():
            visit_file(zn, zf.open(zn, "r"))


def report_fatal(fname: Path, ex: Exception) -> str:
    message = f"FATAL, {ex}"
    emit(f"{fname}: {message}")
    return message


def should_skip_file(fpath: Path) -> bool:
    with util.open_text_file(fpath) as f:
        text = f.read(10000)
        return not ("<erpConnector" in text or "<section" in text)


def check_dir(lib_vars: Library, root: Path) -> dict[str, dict[str, list[str]]]:
    errs = {}
    for f in root.glob("**/*.xml"):
        try:
            if should_skip_file(f):
                emit(f"{f}: SKIP nontemplate")
                continue
            r = parse_file(f, lib_vars.teaching)
        except (ElementTree.ParseError, PermissionError, UnicodeDecodeError) as e:
            # TODO: Add this to the report
            report_fatal(f, e)
            continue

        errlist = report(lib_vars, str(f), r)
        if errlist:
            errs[str(f)] = errlist
            full_report[str(f)] = len(errlist)

    return errs


@dataclass
class Parsed:
    var_decl: set[str]
    var_used: set[str]
    calls: set[str]
    syntax_errors: list[str]
    loop_var_decl: set[str]
    loop_var_use: set[str]


def report(lib_vars: Library, fname: str, p: Parsed) -> dict[str, list[str]]:
    undeclared_vars = p.var_used - p.var_decl
    undeclared_vars.difference_update(lib_vars.variables)
    unknown_loop_variables = p.loop_var_use - p.loop_var_decl
    unknown_loop_variables.difference_update(lib_vars.loopvariables)

    if lib_vars.teaching:
        lib_vars.calls.update(p.calls)
        lib_vars.variables.update(undeclared_vars)
        lib_vars.loopvariables.update(unknown_loop_variables)

    errors = {}

    if undeclared_vars:
        errors["Unknown variables"] = sorted(undeclared_vars)

    unknown_calls = p.calls
    unknown_calls.difference_update(lib_vars.calls)

    if unknown_calls:
        errors["Unknown calls"] = sorted(unknown_calls)

    if p.syntax_errors:
        errors["Other errors"] = list(p.syntax_errors)

    if unknown_loop_variables:
        errors["Unknown loop variables"] = sorted(unknown_loop_variables)

    if errors:
        emit(yaml.dump({fname: errors}).strip())

    return errors


key_params: dict[str, str] = {
    "bw_file_functions": "command",
    "bw_table_method": "command",
    "bw_string_functions": "operation",
    "bw_ws_function": "method",
}


def summarize_call(node: Element) -> str:
    name = node.attrib["name"].lower()
    full = name
    params = {
        p.attrib["name"]: (p.text or "TEXTMISSING") for p in node.iter("parameter")
    }
    suboperation_param_name = key_params.get(name)
    if suboperation_param_name:
        suboperation = params.get(suboperation_param_name, "UNK")
        full += "." + suboperation

    return full + " - " + ",".join(sorted(params))


def summarize_tag(node: Element) -> str:
    at = " " + " ".join(sorted(node.attrib.keys())) if node.attrib else ""

    full = "<" + node.tag + at + ">"
    return full


def brace_check(s: str) -> list[str]:
    stack: list[tuple[str, int]] = []
    lines = s.splitlines()
    closers = {"{": "}", "[": "]", "(": ")"}
    lnum = 0
    errors: list[str] = []
    for l in lines:
        lnum += 1
        cnum = 0
        flush_stack = False
        in_quote = False
        for ch in l:
            cnum += 1
            if ch == '"':
                # only care about quotes if we are in some nested operation already, top level quotes are not considered
                if stack:
                    in_quote = not in_quote

            if in_quote:
                continue

            if ch in "{([":
                stack.append((ch, lnum))
            if ch in "})]":
                try:
                    from_stack, _ = stack.pop()
                except IndexError:
                    errors.append(
                        f"Too many closing braces at line {lnum}, looking at '{ch}' on col {cnum}: ==> {l[cnum-10:cnum]} <==: {l.strip()}",
                    )
                    flush_stack = True
                    break

                expected = closers[from_stack]
                if expected != ch:
                    errors.append(
                        f"Expected brace {expected}, got {ch} at line {lnum} col {cnum}: {l.strip()}",
                    )
                    flush_stack = True
                    break
        if flush_stack:
            stack = []
    if stack:
        errors.append(
            f"File ended with mismatched braces, remaining in stack (char, linenum): {stack}",
        )
    return errors


# xxx not really needed due to new logic
MAGIC_VAR_NAMES = {"error", "return", "response", "invoice.i"}


def describe_node(n: Element) -> str:
    return "<" + n.tag + str(n.attrib) + ">"


def describe_jump(n: Element) -> str:
    params = sorted(
        child.attrib.get("name", "NONAME").strip() for child in n.iter("parameter")
    )
    target = n.attrib.get("jumpToXPath", "NOXPATH")
    prefix = "//section[@name='"
    if target.startswith(prefix):
        target = "..." + target[len(prefix) :].rstrip("]'")

    desc = (
        "Jump "
        + n.attrib.get("jumpToXmlFile", "NOFILE")
        + " -- "
        + target
        + " -- "
        + " ".join(params)
    )
    return desc.strip()


def replace_commented_xml_with_empty_lines(xml_string: str) -> str:
    # Define a regular expression pattern to match XML comments
    comment_pattern = "<!--(.*?)-->"
    cdata_pattern = r"<!\[CDATA\[(.*?)\]\]>"

    # Use re.sub to replace the matched comments with an equivalent number of empty lines
    def replace(match: re.Match[str]) -> str:
        comment = match.group(0)
        empty_lines = "\n" * comment.count("\n")
        return empty_lines

    result = re.sub(comment_pattern, replace, xml_string, flags=re.DOTALL)
    result = re.sub(cdata_pattern, replace, result, flags=re.DOTALL)
    return result


def is_illegal_password(name: str, value: str) -> bool:
    if "passw" not in name.lower():
        return False
    stripped = (value or "").strip()
    if not stripped:
        return False
    if stripped.startswith("{"):
        # password should always be references to variables or expressions, never literal values
        return False
    return True


def parse_file(fname: str | Path, teaching: bool = False) -> Parsed:
    tree = ElementTree.parse(fname)
    cont = ElementTree.tostring(tree.getroot())

    vardecl = {
        v.attrib.get("name", "unknown_var"): (v.text or "")
        for v in tree.iter("variable")
    }
    all_params = {
        v.attrib.get("name", "unknown_var"): (v.text or "")
        for v in tree.iter("parameter")
    }

    propaccess = {
        (m.group(1).decode(), m.group(2).decode())
        for m in re.finditer(b"([a-zA-Z.]+),(\\w+)", cont)
    }
    varuse = {n for k, n in propaccess if k == "v"}
    expruse = {"f," + n for k, n in propaccess if k == "f"}

    # what to do with p params?
    otherpropaccess = {k for k, v in propaccess if k.lower() not in ["v", "f", "p"]}
    otherpropaccess.difference_update(MAGIC_VAR_NAMES)
    calls = {summarize_call(v) for v in tree.iter("builtInMethodParameterList")}
    alltags = {summarize_tag(t) for t in tree.iter()}
    loop_data_source_attribs = {n.attrib.get("loopDataSource") for n in tree.iter()}
    loop_data_sources = {
        ls.split(";")[0].lower() for ls in loop_data_source_attribs if ls
    }
    return_names = {
        n.attrib.get("name", "UNNAMED_RETURN").lower() for n in tree.iter("return")
    }
    loop_data_sources.update(return_names)

    jumps = (
        describe_jump(n) for n in tree.iter("method") if n.attrib.get("jumpToXmlFile")
    )

    calls.update(expruse)
    calls.update(alltags)
    calls.update(jumps)
    errors = []

    if not teaching:
        raw_cont = util.open_text_file(fname).read()
        parsed_cont = replace_commented_xml_with_empty_lines(raw_cont)

        errors.extend(brace_check(parsed_cont))

        no_text_allowed_tags = [
            "sections",
            "section",
            "method",
            "output",
            "outputCommands",
            "builtInMethodParameterList",
        ]
        for notext in no_text_allowed_tags:
            nodes = tree.iter(notext)
            for n in nodes:
                if n and n.text and n.text.strip():
                    errors.append(
                        "Node should not contain text: "
                        + describe_node(n)
                        + " -- "
                        + n.text.strip(),
                    )
        var_passwords = {v for v in vardecl if is_illegal_password(v, vardecl[v])}
        param_passwords = {
            p for p in all_params if is_illegal_password(p, all_params[p])
        }
        passwords = var_passwords | param_passwords
        if passwords:
            errors.append("Passwords contains literal text: " + ",".join(passwords))

    return Parsed(
        var_decl=set(vardecl),
        var_used=varuse,
        calls=calls,
        syntax_errors=errors,
        loop_var_decl=loop_data_sources,
        loop_var_use=otherpropaccess,
    )
