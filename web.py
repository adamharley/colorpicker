import sys
sys.path.append("lib/Adafruit_NeoPixel_FTDI")
sys.path.append("lib/cherrypy")
import os, os.path
import cherrypy
import Adafruit_NeoPixel_FTDI as neo


class myapp(object):
	@cherrypy.expose
	def index(self):
		return """<html>
	<head>
		<link rel="stylesheet" type="text/css" href="lib/FlexiColorPicker/themes.css" />
		<style>
		html,
		body {
			margin: 0;
			padding: 0;
		}
		</style>
		<script src="lib/FlexiColorPicker/colorpicker.js"></script>
		<script>
		function updateInputs(hex) {
			var postData = new FormData();
			postData.append("hex", "0x" + hex.substr(1));
	
			var xhr = new XMLHttpRequest();
			xhr.responseType = "document";
			xhr.open("PUT", "/update", true);
			xhr.send(postData);
		}

		document.addEventListener("DOMContentLoaded", function() {
			var cp = ColorPicker(document.getElementById("small"), updateInputs);
			cp.setHex("#cccccc");
		});
		</script>
	</head>
	<body>
		<div id="small" class="cp cp-small"></div>
	</body>
</html>"""

	@cherrypy.expose
	def update(self, hex):
		pixels = neo.Adafruit_NeoPixel(7)
		for i in range(7):
			pixels.setPixelColor(i, hex)
		
		pixels.show()

if __name__ == '__main__':
	conf = {
		'global': {
			'server.socket_port': 9999,
		},
		'/': {
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/js': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './js'
		},
		'/lib': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './lib'
		}
	}
	cherrypy.quickstart(myapp(), '/', conf)