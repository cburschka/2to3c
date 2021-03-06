import sys
import re

# I wasn't able to express this refactoring in SmPLs; the implied comma embedded
# in the _HEAD_INIT macros seems to be too much for spatch to reasonably deal
# with.

# So I expressed this one as a regex.

# Whitespace patterns:
req_ws = r'\s+'
opt_ws = r'\s*'
c_identifier = r'([_A-Za-z][_0-9A-Za-z]*)'

pat = ('.*' + r'PyTypeObject' + req_ws
       + c_identifier + opt_ws 
       + r'=' + opt_ws + r'\{' + opt_ws 
       + r'(PyObject_HEAD_INIT\((.*)\)' + opt_ws 
       + r'([0-9]+)' + opt_ws + r',).*'
       )

def fixup_typeobject_initializers(content):
    while True:
        m = re.match(pat, content, re.DOTALL)
        if m:
            if False:
                print m.groups()
                print m.group(2)
                print m.group(3)
                print m.group(4)
                print m.span(2)
            content = (content[:m.start(2)] 
                       + 'PyVarObject_HEAD_INIT(%s, %s)' % (m.group(3),m.group(4))
                       + content[m.end(2):])
        else:
            return content

from lib2to3c import Fix, FixTest
class FixTypeobjectInitializers(Fix):
    def transform(self, string):
        return fixup_typeobject_initializers(string)

import unittest
class TestFixups(FixTest):
    def setUp(self):
        self.fixer = FixTypeobjectInitializers()

    def test_fixups(self):
        self.assertTransformsTo(self.fixer,
                                '''
PyTypeObject DBusPyIntBase_Type = {
    PyObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type))
    0,
    "_dbus_bindings._IntBase",
''',
                          '''
PyTypeObject DBusPyIntBase_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "_dbus_bindings._IntBase",
''')

    def test_fixup_with_comment(self):
        self.assertTransformsTo(self.fixer,
                                '''
PyTypeObject PyFortran_Type = {
    PyObject_HEAD_INIT(0)
    0,                    /*ob_size*/
    "fortran",                    /*tp_name*/
''',
                                '''
PyTypeObject PyFortran_Type = {
    PyVarObject_HEAD_INIT(0, 0)                    /*ob_size*/
    "fortran",                    /*tp_name*/
''')

if __name__ == '__main__':
    unittest.main()
