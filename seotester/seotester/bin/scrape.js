var args = require('system').args;

if (args.length != 3) {
	console.error('Please provide two parameters: source URL and destination file name');
	phantom.exit(1);
}

var page = require('webpage').create();

page.viewportSize = {height: 900, width: 1400}

page.onResourceReceived = function(res) {
    if(res.url == args[1]) {
        console.log(res.status);
    }
}

page.open(args[1], function(e) {
//	page.render(args[2]);
    console.log(page.content);
	phantom.exit();
});
