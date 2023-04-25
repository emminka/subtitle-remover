const { app, BrowserWindow, Menu, globalShortcut  } = require('electron')
const path = require('path')
const log = require('electron-log')

/*
const {PythonShell} = require('python-shell');

let pyshell = new PythonShell('script.py');

pyshell.send(JSON.stringify([10]))

pyshell.on('message', function(message) {
  console.log(message);
})

pyshell.end(function (err) {
  if (err){
    throw err;
  };
  console.log('finished');
});*/

function createWindow () {
  const win = new BrowserWindow({
    width: 1170,
    height: 729,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
  }
  })

  

  //win.setMenu(null)

  win.loadFile('index.html')

  // Remove the default menu bar
  // Listen for the ready-to-show event
  win.once('ready-to-show', () => {
    // Remove the default menu bar
    Menu.setApplicationMenu(null);
    // Show the window
    win.show();
  });
}

function openDevTools() {
  const win = BrowserWindow.getFocusedWindow();
  if (win) {
    win.webContents.openDevTools();
  }
}

app.whenReady().then(() => {
  // Register a global shortcut for opening the developer tools
  globalShortcut.register('CommandOrControl+Shift+I', openDevTools);
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  };
});

