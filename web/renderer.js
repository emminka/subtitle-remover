////////////////////////
// Emma Krompascikova //
// Bachelor Thesis    //
// Hardsub Remover    //
// May 2023           //
////////////////////////

const spawn = require("child_process").spawn;

function call_script() {
  let path_to_directory = __dirname;
  console.log(path_to_directory);
  let path_to_script = path_to_directory + "\\delete_subtitles.py";
  console.log(path_to_script);
  const pythonProcess = spawn(
    'python',
    [path_to_script, "-a", leftUpX, "-b", leftUpY, "-c", RightDownX, "-d", RightDownY, "-e", filePath, "-f", heightOfVideo, "-g", widthOfVideo, "-h", method_of_removing, "-i", technique_of_removing, "-j", detection_on_every_x_frame],
  );  //define what goes into my script

  pythonProcess.stdout.on('data', (data) => {
    const message = data.toString();
    console.log(message);
    if (message.includes("PROGRESS")) {
      const rows = message.split("\n");
      rows.forEach(element => {
        if (element.startsWith("PROGRESS")) {
          const match = element.match(/PROGRESS:\s*(\d+)/);
          if (match) {
            const progress = match[1];
            const modalBar = document.getElementById('progress_bar');
            modalBar.value = progress;
            if (progress == 1000) {
              document.getElementById('close_button').style.display = "block";
              document.getElementById('text_modal').innerHTML = "Video has been succesfully released. It is in the same folder as original video. You can close the app now."
            }
            else if (progress == 951) {
              document.getElementById('text_modal').innerHTML = "The audio is being processed. Almost done."

            }
          }
        };
      });
    }
    else if (message.includes("TIME_OF_REMOVING")) {
      const rows = message.split("\n");
      rows.forEach(element => {
        if (element.startsWith("TIME_OF_REMOVING")) {
          const match = element.match(/TIME_OF_REMOVING:\s*(\d+)/);
          if (match) {
            const time_in_minutes = match[1];
            const modalBar = document.getElementById('text_modal');
            if (time_in_minutes == 1) {
              modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately 1 minute.";
            }
            else if (time_in_minutes == 0) {
              modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately less than 1 minute.";
            }
            else if (time_in_minutes > 1 && time_in_minutes < 60) {
              modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately " + time_in_minutes + " minutes.";
            }
            else if (time_in_minutes > 60) {
              const time_in_hours = Math.floor(time_in_minutes / 60 * 10) / 10; // calculates hours with one decimal place
              modalBar.innerHTML = "Subtitles are being removed. Please do not close the window. Removal will take approximately " + time_in_hours.toFixed(1) + " hours.";
            }
          };
        }
      });
    }
  });

  pythonProcess.stderr.on('data', (data) => {
    const message = data.toString();
    if (message.includes("Error") || message.includes("Errno")) {
      console.error(message);
    }
    else {
      console.warn(message);
    }
  });
  console.log("Script was called.");
}

module.exports = { call_script };
