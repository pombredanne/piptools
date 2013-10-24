# -*- coding: utf-8 -*-
# PEP8:NO, LINT:OK, PY3:NO


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" PIP Tools "
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 30/10/2013 '
__prj__ = ' '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path
from PyQt4.QtGui import QMenu, QInputDialog, QMessageBox, QFileDialog

from PyQt4.QtCore import QProcess

from ninja_ide.core import plugin


HELPMSG = '''<h3> PIP Tools</h3>
<ul>
    <li> PIP Review
    <li> PIP Dumps
</ul>
pip-review checks PyPI and reports available updates.<br>
It uses the list of currently installed packages to check for updates.<br>
Dont overwrite packages, just reports. <br><br>
pip-dump dumps the exact versions of installed packages in your active
environment to your requirements.txt file. <br>
Dont overwrite packages, just reports. <br>
If you have more than one file matching the *requirements.txt pattern
(for example dev-requirements.txt), it will update each of them smartly.<br>
<center><small><i>
This is frontend to <a href="https://github.com/nvie/pip-tools">pip-tools</a>
<br>''' + ''.join((__doc__, ', v', __version__, __license__, 'by', __author__))


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        super(Main, self).initialize(*args, **kwargs)
        self.menu, self.process = QMenu(__doc__), QProcess(self)
        self.process.finished.connect(self._process_finished)
        self.process.error.connect(self._process_finished)
        self.menu.addAction('PIP-Dump', lambda: self.run(0))
        self.menu.addAction('PIP-Review', lambda: self.run(1))
        self.menu.addAction('Kill PIP-Tools Process',
                            lambda: self.process.kill())
        self.menu.addSeparator()
        # self.menu.addAction('Read Debugger Process StandardOutput', lambda: QMessageBox.information(None, __doc__, str(self.process.readAllStandardOutput())))
        # self.menu.addAction('Read Debugger Process StandardError', lambda: QMessageBox.information(None, __doc__, str(self.process.readAllStandardError())))
        self.menu.addAction('PIP-Tools Help',
                        lambda: QMessageBox.information(None, __doc__, HELPMSG))
        self.locator.get_service("menuApp").add_menu(self.menu)

    def run(self, option):
        ' run backend process '
        if option is 0:
            QMessageBox.information(None, __doc__,
            '''pip-dump dumps the exact versions of installed packages in your
            active environment to your requirements.txt file.
            If you have more than one file matching *requirements.txt pattern
            (example dev-requirements.txt), it will update each one smartly.''')
            cmd = '{}pip-dump {} "{}"'.format('chrt -i 0 '
                if str(QInputDialog.getItem(None, __doc__,
                "PIP-Tools Process CPU Priority:", ['LOW CPU Priority',
                'High CPU Priority'], 0, False)[0]) in 'LOW CPU Priority'
                else '',
                '--verbose'
                if str(QInputDialog.getItem(None, __doc__, "PIP-Tools Options:",
                ['verbose', 'none'], 0, False)[0]) in 'verbose'
                else '',
                QFileDialog.getOpenFileName(None,
                "{} - Open requirements.txt".format(__doc__),
                path.expanduser("~"), 'requirements.txt(requirements.txt)'))
        else:
            QMessageBox.information(None, __doc__,
            '''pip-review checks PyPI and reports available updates.
            It uses the list of currently installed packages to check updates.
            Dont overwrite packages, just reports them.''')
            cmd = '{}pip-review --{}'.format('chrt -i 0 '
                if str(QInputDialog.getItem(None, __doc__,
                "PIP-Tools Process CPU Priority:", ['LOW CPU Priority',
                'High CPU Priority'], 0, False)[0]) in 'LOW CPU Priority'
                else '',
                str(QInputDialog.getItem(None, __doc__, "PIP-Tools Options:",
                ['verbose', 'local', 'raw'], 0, False)[0]))
        self.process.start(cmd)
        if not self.process.waitForStarted():
            QMessageBox.information(None, __doc__ + '- ERROR!',
            str(self.process.readAllStandardError()))

    def _process_finished(self):
        ' show results '
        self.locator.get_service("editor").add_editor(
            content=str(self.process.readAllStandardOutput()), syntax='python')

    def finish(self):
        ' clear when finish '
        self.process.kill()


###############################################################################


if __name__ == "__main__":
    print(__doc__)
