const spawn = require("child_process").spawn;

function skript(){
  let path_to_directory = __dirname;
  console.log(path_to_directory);
  let path_to_script = path_to_directory + "\\deletesubtitles_new.py";
  console.log(path_to_script);
  const pythonProcess = spawn('python',[path_to_script, "-a",leftUpX, "-b",leftUpY, "-c", RightDownX ,"-d",RightDownY, "-e", filePath, "-f", heightOfVideo, "-g", widthOfVideo, "-h", metoda_odstranenia, "-i" , technika_odstranenia, "-j" , detection_on_every_x_frame]);  //definujem co je ten moj skript

  pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
  });

  console.log("Zavolalli smne skript");
  
}

module.exports = { skript } //exportujem python skript