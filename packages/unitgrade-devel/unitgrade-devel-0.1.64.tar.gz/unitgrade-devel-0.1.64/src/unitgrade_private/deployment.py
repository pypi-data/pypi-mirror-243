import inspect
from unitgrade.utils import hide, methodsWithDecorator
import os
import importlib
import snipper

# import re, inspect
#
# FUNC_BODY = re.compile('^(?P<tabs>[\t ]+)?def (?P<name>[a-zA-Z0-9_]+)([^\n]+)\n(?P<body>(^([\t ]+)?([^\n]+)\n)+)', re.M)
#
# class Source(object):
#     @staticmethod
#     def investigate(focus: object, strfocus: str) -> str:
#         with open(inspect.getsourcefile(focus), 'r') as f:
#             for m in FUNC_BODY.finditer(f.read()):
#                 if m.group('name') == strfocus:
#                     tabs = m.group('tabs') if not m.group('tabs') is None else ''
#                     return f"{tabs}'''\n{m.group('body')}{tabs}'''"
#
#
# def decorator(func):
#     def inner():
#         print("I'm decorated")
#         func()
#
#     return inner
#
#
# @decorator
# def test():
#     a = 5
#     b = 6
#     return a + b
#
#
# print(Source.investigate(test, 'test'))


def remove_hidden_methods(ReportClass, outfile=None):
    # Given a ReportClass, clean out all @hidden tests from the imports of that class.
    file = ReportClass()._file()
    with open(file, 'r') as f:
        source = f.read().splitlines()

    lines_to_rem = []

    for l in source:
        if l.strip().startswith("@hide"):
            print(l)


    for Q,_ in ReportClass.questions:
        ls = list(methodsWithDecorator(Q, hide))
        # print("hide decorateed is", ls)
        for f in ls:
            assert inspect.getsourcefile(f) == file, "You must apply the @hide decorator as the inner-most decorator, i.e., just above the function you wish to remove."

            s, start = inspect.getsourcelines(f)
            end = len(s) + start
            lines_to_rem += list(range(start-1, end-1))

        print("All hidden funcs")
        print(ls)

    source = list([l for k, l in enumerate(source) if k not in lines_to_rem])
    source = "\n".join(source)

    if outfile == None:
        outfile = file[:-3] + "_nohidden.py"

    if os.path.exists(outfile) and os.path.samefile(file, outfile):
        raise Exception("Similar file paths identified!")

    # Allows us to use the !b;silent tags in the code. This is a bit hacky, but allows timeouts, etc. to make certain tests more robust
    from snipper.fix_bf import fix_b
    from snipper.snipper_main import fix_tags
    from snipper.snip_dir import censor_file
    from snipper.snip_dir import snip_dir

    lines, _, _ = fix_b(fix_tags(source.rstrip().splitlines()))
    source = "\n".join(lines)
    # print(source)
    with open(os.path.dirname(file) + "/" + outfile, 'w') as f:
        f.write(source)

    module_name = ReportClass.__module__
    # module_name.find(".")
    i = module_name.rfind(".")
    module_name = (module_name[:i] if i >=0 else module_name) + "." + os.path.basename(outfile)[:-3]


    module = importlib.import_module(module_name)
    HiddenReportClass = getattr(module, ReportClass.__name__)
    return outfile, HiddenReportClass
