const { ipcMain } = require('electron');
const { ipcRenderer } = require('electron');
const spawn = require("child_process").spawn;

function skript(){
  let path_to_directory = __dirname;
  console.log(path_to_directory);
  let path_to_script = path_to_directory + "\\deletesubtitles_new.py";
  console.log(path_to_script);
  const pythonProcess = spawn(
    'python',
    [path_to_script, "-a",leftUpX, "-b",leftUpY, "-c", RightDownX ,"-d",RightDownY, "-e", filePath, "-f", heightOfVideo, "-g", widthOfVideo, "-h", metoda_odstranenia, "-i" , technika_odstranenia, "-j" , detection_on_every_x_frame],
  );  //definujem co je ten moj skript

  pythonProcess.stdout.on('data', (data) => {
    const message = data.toString();
    console.log(message);
    if (message.includes("PROGRESS")) {
      const rows = message.split("\n");
      rows.forEach(element => {
        if(element.startsWith("PROGRESS")) {
          const match = element.match(/PROGRESS:\s*(\d+)/);
          if (match) {
            const progress = match[1];
            const modalBar = document.getElementById('progress_bar');
            modalBar.value = progress;
        }
      }
      });
      // Update the modal window with the message containing "done"
      
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    const message = data.toString();
    if (message.includes("error") || message.includes("Error")) {
      console.error(message);
    }
    else{
      console.warn(message);
    }
  });

  console.log("Zavolalli smne skript");
}

module.exports = { skript }; //exportujem python skript