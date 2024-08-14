const { app, BrowserWindow } = require('electron')

function createWindow() {
    window = new BrowserWindow({ 
    	width: 1200,
    	height: 640
    });
    
    /*var python = require('child_process').spawn('python', ['./hello.py']);
	python.stdout.on('data',function(data){
    		console.log("data: ",data.toString('utf8'));
	});*/
	
    var pyshell = require('python-shell');

    pyshell.run('engine.py', function(err, results) {
        if (err) throw err;
        console.log('engine.py finished.');
        console.log('results', results);
        
    });

    //window.loadFile('templates/index.html')
    window.loadURL('http://localhost:8210');
    window.webContents.openDevTools()

}


app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})