import difflib
import StringIO

import pygments
from pygments.lexers import get_lexer_by_name
from pygments.lexer import RegexLexer
from pygments.formatters import HtmlFormatter
from pygments.token import *


class DefaultLexer(RegexLexer):
    """
    Simply lex each line as a token.
    """

    name = 'Default'
    aliases = ['default']
    filenames = ['*']

    tokens = {
        'root': [
            (r'.*\n', Text),
        ]
    }


class DiffHtmlFormatter(HtmlFormatter):
    """
    Formats a single source file with pygments and adds diff highlights based on the
    diff details given.
    """
    isLeft = False
    diffs = None

    def __init__(self, is_left, diffs, *args, **kwargs):
        self.is_left = is_left
        self.diffs = diffs
        super(DiffHtmlFormatter, self).__init__(*args, **kwargs)

    def wrap(self, source, outfile):
        return self._wrap_code(source)

    def get_diff_line_nos(self):
        ret_line_nos = []
        for idx, ((left_no, left_line), (right_no, right_line), change) in enumerate(self.diffs):
            no = None
            if self.isLeft:
                if change:
                    if isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_leftchange">' + str(left_no) + "</span>"
                    elif isinstance(left_no, int) and not isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_leftdel">' + str(left_no) + "</span>"
                    elif not isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_leftadd">  </span>'
                else:
                    no = '<span class="lineno_q">' + str(left_no) + "</span>"
            else:
                if change:
                    if isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_rightchange">' + str(right_no) + "</span>"
                    elif isinstance(left_no, int) and not isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_rightdel">  </span>'
                    elif not isinstance(left_no, int) and isinstance(right_no, int):
                        no = '<span class="lineno_q lineno_rightadd">' + str(right_no) + "</span>"
                else:
                    no = '<span class="lineno_q">' + str(right_no) + "</span>"

            ret_line_nos.append(no)

        return ret_line_nos

    def _wrap_code(self, source):
        source = list(source)
        yield 0, '<pre>'

        for idx, ((left_no, left_line), (right_no, right_line), change) in enumerate(self.diffs):
            #print idx, ((left_no, left_line),(right_no, right_line),change)
            try:
                if self.isLeft:
                    if change:
                        if isinstance(left_no, int) and isinstance(right_no, int) and left_no <= len(source):
                            i, t = source[left_no-1]
                            t = '<span class="left_diff_change">' + t + "</span>"
                        elif isinstance(left_no, int) and not isinstance(right_no, int) and left_no <= len(source):
                            i, t = source[left_no-1]
                            t = '<span class="left_diff_del">' + t + "</span>"
                        elif not isinstance(left_no, int) and isinstance(right_no, int):
                            i, t = 1, left_line
                            t = '<span class="left_diff_add">' + t + "</span>"
                        else:
                            raise
                    else:
                        if left_no <= len(source):
                            i, t = source[left_no-1]
                        else:
                            i = 1
                            t = left_line
                else:
                    if change:
                        if isinstance(left_no, int) and isinstance(right_no, int) and right_no <= len(source):
                            i, t = source[right_no-1]
                            t = '<span class="right_diff_change">' + t + "</span>"
                        elif isinstance(left_no, int) and not isinstance(right_no, int):
                            i, t = 1, right_line
                            t = '<span class="right_diff_del">' + t + "</span>"
                        elif not isinstance(left_no, int) and isinstance(right_no, int) and right_no <= len(source):
                            i, t = source[right_no-1]
                            t = '<span class="right_diff_add">' + t + "</span>"
                        else:
                            raise
                    else:
                        if right_no <= len(source):
                            i, t = source[right_no-1]
                        else:
                            i = 1
                            t = right_line
                yield i, t
            except:
                #print "WARNING! failed to enumerate diffs fully!"
                pass  # this is expected sometimes
        yield 0, '\n</pre>'

    def _wrap_tablelinenos(self, inner):
        dummy_out_file = StringIO.StringIO()
        lncount = 0
        for t, line in inner:
            if t:
                lncount += 1
            dummy_out_file.write(line)

        fl = self.linenostart
        mw = len(str(lncount + fl - 1))
        sp = self.linenospecial
        st = self.linenostep
        la = self.lineanchors
        aln = self.anchorlinenos
        nocls = self.noclasses

        lines = []
        for i in self.get_diff_line_nos():
            lines.append('%s' % (i,))

        ls = ''.join(lines)

        # in case you wonder about the seemingly redundant <div> here: since the
        # content in the other cell also is wrapped in a div, some browsers in
        # some configurations seem to mess up the formatting...
        if nocls:
            yield 0, ('<table class="%stable">' % self.cssclass +
                      '<tr><td><div class="linenodiv" '
                      'style="background-color: #f0f0f0; padding-right: 10px">'
                      '<pre style="line-height: 125%">' +
                      ls + '</pre></div></td><td class="code">')
        else:
            yield 0, ('<table class="%stable">' % self.cssclass +
                      '<tr><td class="linenos"><div class="linenodiv"><pre>' +
                      ls + '</pre></div></td><td class="code">')
        yield 0, dummyoutfile.getvalue()
        yield 0, '</td></tr></table>'


class CodeDiff(object):
    """
    Manages a pair of source files and generates a single html diff page comparing
    the contents.
    """
    pygmentsStyleOpt = "vs"
    pygmentsCssFile = "./deps/codeformats/%s.css" % pygmentsStyleOpt
    diffCssFile = "./deps/diff.css"
    diffJsFile = "./deps/diff.js"
    resetCssFile = "./deps/reset.css"
    semanticCssFile = "./deps/semantic.min.css"
    semanticJsFile = "./deps/semantic.min.js"
    jqueryJsFile = "./deps/jquery.min.js"
    commentJsFile = "./deps/comment.js"

    def __init__(self, from_file, to_file, from_txt=None, to_txt=None):

        self.from_file = from_file
        if from_txt is None:
            self.from_lines = open(from_file, 'U').readlines()
        else:
            self.from_lines = [n + "\n" for n in from_txt.splitlines()]
        self.left_code = "".join(self.from_lines)
      
        self.to_file = to_file
        if to_txt is None:
            self.to_lines = open(to_file, 'U').readlines()
        else:
            self.to_lines = [n + "\n" for n in to_txt.splitlines()]
        self.right_code = "".join(self.tolines)

    def get_diff_details(self, from_desc='', to_desc='', context=False, numlines=5, tabSize=8):

        # change tabs to spaces before it gets more difficult after we insert
        # markup
        def expand_tabs(linet):
            # hide real spaces
            linet = linet.replace(' ', '\0')
            # expand tabs into spaces
            linet = linet.expandtabs(tabSize)
            # replace spaces from expanded tabs back into tab characters
            # (we'll replace them with markup after we do differencing)
            linet = linet.replace(' ', '\t')
            return linet.replace('\0', ' ').rstrip('\n')

        self.from_lines = [expand_tabs(line) for line in self.from_lines]
        self.to_lines = [expand_tabs(line) for line in self.to_lines]

        # create diffs iterator which generates side by side from/to data
        if context:
            context_lines = numlines
        else:
            context_lines = None

        diffs = difflib._mdiff(self.from_lines, self.to_lines, context_lines, linejunk=None,
                               charjunk=difflib.IS_CHARACTER_JUNK)
        return list(diffs)

    def format(self, verbose=False):
        self.diffs = self.get_diff_details(self.from_file, self.to_file)

        if verbose:
            for diff in self.diffs:
                print "%-6s %-80s %-80s" % (diff[2], diff[0], diff[1])

        fields = ((self.left_code, True, self.from_file), (self.right_code, False, self.to_file))

        code_contents = []
        for (code, isLeft, filename) in fields:

            inst = DiffHtmlFormatter(isLeft,
                                     self.diffs,
                                     nobackground=False,
                                     linenos=True,
                                     style=self.pygmentsStyleOpt)

            try:
                self.lexer = get_lexer_by_name("sql")
            
            except pygments.util.ClassNotFound:
                if verbose:
                    print "No Lexer Found! Using default..."
                self.lexer = DefaultLexer()
         
            formatted = pygments.highlight(code, self.lexer, inst)
         
            code_contents.append(formatted)

        diffTemplate = open("./templates/diff_template.html", 'r').read()

        answers = {
            "html_title":     self.filename,
            "reset_css":   self.resetCssFile,
            "pygments_css":   self.pygmentsCssFile,
            "diff_css":       self.diffCssFile,
            "semantic_css":   self.semanticCssFile,
            "page_title":     self.filename,
            "original_code":  codeContents[0],
            "modified_code":  codeContents[1],
            "jquery_js":      self.jqueryJsFile,
            "semantic_js":    self.semanticJsFile,
            "diff_js":        self.diffJsFile,
            "comment_js":     self.commentJsFile,
        }

        self.htmlContents = diffTemplate % answers

    def write(self, path="index.html"):
        fh = open(path, 'w')
        fh.write(self.htmlContents.encode('utf8'))
        fh.close()


def diff2HtmlComp(fromfile, tofile, fromtext, totext):
    codeDiff = CodeDiff(fromfile, tofile, fromtext, totext)
    codeDiff.format()
    return codeDiff.htmlContents.encode("utf8")

