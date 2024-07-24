let fileInput = document.getElementById("file-input");
let fileList = document.getElementById("files-list");
let numOfFiles = document.getElementById("num-of-files");

let filesArray = []; // Array to keep track of selected files and their list items

fileInput.addEventListener("change", () => {
  let newFilesArray = Array.from(fileInput.files);

  // Update filesArray to include new files
  newFilesArray.forEach(file => {
    if (!filesArray.some(f => f.file === file)) {
      filesArray.push({ file: file, listItem: createFileListItem(file) });
    }
  });

  // Update the UI
  updateFileList();
});

function createFileListItem(file) {
  let listItem = document.createElement("li");

  let fileName = file.name;
  let fileSize = (file.size / 1024).toFixed(1);
  if (fileSize >= 1024) {
    fileSize = (fileSize / 1024).toFixed(1);
    fileSize += "MB";
  } else {
    fileSize += "KB";
  }

  let fileInfo = document.createElement("div");
  fileInfo.innerHTML = `<p>${fileName}</p><p>${fileSize}</p>`;

  let removeButton = document.createElement("button");
  removeButton.textContent = "Remove";
  removeButton.classList.add("remove-button");

  removeButton.addEventListener("click", () => {
    filesArray = filesArray.filter(f => f.file !== file);
    updateFileList();
  });

  listItem.appendChild(fileInfo);
  listItem.appendChild(removeButton);
  
  return listItem;
}

function updateFileList() {
  fileList.innerHTML = ""; // Clear existing file list
  filesArray.forEach(item => {
    fileList.appendChild(item.listItem);
  });

  numOfFiles.textContent = `${filesArray.length} Files Selected`;
}