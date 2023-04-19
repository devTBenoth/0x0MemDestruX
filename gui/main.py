import gi, subprocess, os
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, GLib, Vte
lib_path = os.path.abspath("../src")
os.environ["LD_LIBRARY_PATH"] = f"{os.getenv('LD_LIBRARY_PATH', '')}:{lib_path}"
class bufferGUI(Gtk.Window):
    def error_dialog(title, message):
        dialog = Gtk.MessageDialog(
            transient_for=None,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
    def __init__(self):
        Gtk.Window.__init__(self, title="Bufferoverflow GUI")
        self.set_default_size(580, 380)
        self.set_resizable(False)
        self.connect("destroy", Gtk.main_quit)
        
        # Enable CSS Provider
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_path("utils/css/style.css")
        screen = Gdk.Screen.get_default()
        styleContext = self.get_style_context()
        styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Get Style Context
        styleContext = self.get_style_context()
        styleContext.add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        # Set background color using CSS
        styleContext.add_class("bg-color")

        # Create Fixed
        fixed = Gtk.Fixed()
        self.add(fixed)

        # Author Label
        self.author = Gtk.Label(label="github.com/devtbenoth")
        self.author.get_style_context().add_class("labels")
        fixed.put(self.author, 400, 5)

        # Main Label
        self.mLabel = Gtk.Label()
        self.mLabel.set_markup("<b> BUFFEROVERFLOW GUI </b>")
        self.mLabel.get_style_context().add_class("mainHeader")
        fixed.put(self.mLabel, 50, 50)

        # IP Label
        self.ipLabel = Gtk.Label(label="IP ADDRESS")
        self.ipLabel.get_style_context().add_class("labels")
        fixed.put(self.ipLabel, 100, 110)

        self.ipBox = Gtk.Entry()
        self.ipBox.set_max_length(16)
        self.ipBox.get_style_context().add_class("inputs")
        self.ipBox.set_size_request(200, 1)
        fixed.put(self.ipBox, 50, 140)

        # PORT Label
        self.portLabel = Gtk.Label(label="PORT")
        self.portLabel.get_style_context().add_class("labels")
        fixed.put(self.portLabel, 378, 110)

        # PORT Textbox
        self.portBox = Gtk.Entry()
        self.portBox.get_style_context().add_class("inputs")
        self.portBox.set_size_request(200, 1)
        fixed.put(self.portBox, 300, 140)
        
        # vulnName label
        self.vulnLabel = Gtk.Label(label="VULN NAME (Optional)")
        self.vulnLabel.get_style_context().add_class("labels")
        fixed.put(self.vulnLabel, 68, 195)

        # vulnName Textbox
        self.vuln = Gtk.Entry()
        self.vuln.get_style_context().add_class("inputs")
        self.vuln.set_size_request(200, 1)
        fixed.put(self.vuln, 50, 225)

        # bufferSize label
        self.bufferSizeLabel = Gtk.Label(label="Buffer Size")
        self.bufferSizeLabel.get_style_context().add_class("labels")
        fixed.put(self.bufferSizeLabel, 358, 195)

        # bufferSize Textbox
        self.bufferSizeText = Gtk.Entry()
        self.bufferSizeText.get_style_context().add_class("inputs")
        self.bufferSizeText.set_size_request(200, 1)
        fixed.put(self.bufferSizeText, 300, 225)

        # Finish Button
        finButton = Gtk.Button(label="GO BUFF!")
        finButton.get_style_context().add_class("finish-button")
        finButton.connect("clicked", self.on_button_clicked)
        finButton.set_size_request(110, 40)
        fixed.put(finButton, 223, 280)

        # IP Address Result Label
        self.ipAddress = Gtk.Label(label="IP ADDRESS: ")
        self.ipAddress.get_style_context().add_class("topSmallLabels")
        fixed.put(self.ipAddress, 12, 5)
        
        # Port Result Label
        self.resultPortLabel = Gtk.Label(label="PORT: ")
        self.resultPortLabel.get_style_context().add_class("topSmallLabels")
        fixed.put(self.resultPortLabel, 12, 28)

        # Result Buffer Size Label
        self.bufferSizeLabel = Gtk.Label(label="Buffer Size: ")
        self.bufferSizeLabel.get_style_context().add_class("bottomSmallLabels")
        fixed.put(self.bufferSizeLabel, 410, 340)

        self.show_all()
    def on_button_clicked(self, widget):
        ipAddress = self.ipBox.get_text()
        if len(ipAddress) > 12:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="ERROR",
            )
            dialog.format_secondary_text("IP adresi 12 karakterden fazla olamaz.")
            dialog.run()
            dialog.destroy()
        self.ipAddress.set_text("IP ADDRESS: " + ipAddress)
        portNo = self.portBox.get_text()
        if len(portNo) >= 10:
            portDialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="ERROR"
            )
            portDialog.format_secondary_text("Port Input Cannot be More Than 10 Characters!")
            portDialog.run()
            portDialog.destroy()
        self.resultPortLabel.set_text("PORT: " + portNo)
        vulnName = self.vuln.get_text()
        bufferSize = self.bufferSizeText.get_text()

        p = subprocess.Popen(['../src/program', str(ipAddress), str(portNo), str(bufferSize), str(vulnName)], stdout=subprocess.PIPE)
        out, err = p.communicate()
        buffer_size_str = out.decode().strip()
        self.bufferSizeLabel.set_text("Buffer Size: " + buffer_size_str)

def main():
    win = bufferGUI()
    Gtk.main()

if __name__ == "__main__":
    main()