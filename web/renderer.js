const spawn = require("child_process").spawn;

function skript(){
  const pythonProcess = spawn('python',["./deletesubtitles_new.py"]);  //definujem co je ten moj skript

  pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
  });

  console.log("Zavolalli smne skript");
}

module.exports = { skript } //exportujem python skript