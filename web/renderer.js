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
    if (message.includes("PROGRESS") ) {
      const rows = message.split("\n");
      rows.forEach(element => {
        if(element.startsWith("PROGRESS")) {
          const match = element.match(/PROGRESS:\s*(\d+)/);
          if (match) {
            const progress = match[1];
            const modalBar = document.getElementById('progress_bar');
            modalBar.value = progress;
            if (progress == 1000){
              document.getElementById('close_button').style.display = "block";
              document.getElementById('text_modal').innerHTML = "Video has been succesfully released. It is in the same foder as original video. You can close the app now."
            }
            else if (progress == 951){
              document.getElementById('text_modal').innerHTML = "The audio is being processed. Almost done."

            }
          }
        };
      });
    }
      else if(message.includes("CAS_ODMAZANIA") ){
        const rows = message.split("\n");
        rows.forEach(element => {
          if(element.startsWith("CAS_ODMAZANIA")) {
            const match = element.match(/CAS_ODMAZANIA:\s*(\d+)/);
            if (match) {
              const cas_v_minutach = match[1];
              const modalBar = document.getElementById('text_modal');
              if(cas_v_minutach == 1){
                modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately 1 minute.";
              }
              else if(cas_v_minutach == 0){
                modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately less than 1 minute.";
              }
              else if(cas_v_minutach > 1 && cas_v_minutach < 60){
                modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately " + cas_v_minutach+" minutes.";
              }
              else if(cas_v_minutach > 60 ){
                const cas_v_hodinach = Math.floor(cas_v_minutach / 60 * 10) / 10; // calculates hours with one decimal place
                modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately " + cas_v_hodinach.toFixed(1) + " hours.";
              }
              
            };      
          }   
        });
      }
  });

  pythonProcess.stderr.on('data', (data) => {
    const message = data.toString();
    if (message.includes("Error")|| message.includes("Errno")) {
      console.error(message);
    }
    else{
      console.warn(message);
    }
  });

  console.log("Zavolalli smne skript");
}

module.exports = { skript }; //exportujem python skript