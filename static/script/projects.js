/* Script for the projects template */

const theParent = document.querySelector('.project-form')
const selectRepo = document.querySelector('#select-repo');
const viewRepo = document.querySelector('#view-repo');
const projectForm = document.querySelector('.project-form');

projectForm.addEventListener('click', (event)=>{
    if (event.target == projectForm) {
        projectForm.style.bottom = "-200%";
    }
});

viewRepo.addEventListener('click', () => {
    projectForm.style.bottom = "0px";
});

document.querySelector('#repo_form').addEventListener('submit', (e) => {
    e.preventDefault();

    const repo_names = document.querySelector('#repository_name').value;
    const repo_url = "/projects/" + encodeURIComponent(repo_names);
    window.location.href = repo_url;

    projectForm.style.bottom = "-200%";
});

try {
    const myList = document.querySelector("#files");
    const languages = document.querySelector("#languages");

    let myLangs = languages.innerText.split(",");
    for (lang of myLangs) {
        const num = lang.split(":")[1].trim();
        try {
            num = parseInt(num);
            alert("Convertible");
        } catch {
            alert("Not convertible");
        }
    }

    const myFiles = myList.innerText.split(",");
    myList.innerHTML = "<h3>Files</h3>";
    for (let i = 0; i < myFiles.length; i++) {
        const listItem = document.createElement("li");
        let text = myFiles[i].split('"')[1];
        listItem.innerText = text;
        listItem.classList.add("list-group-item");
        const ext = extension(text);
        switch (ext) {
            case "py":
                listItem.classList.add("python");
                break;
            case "js":
                listItem.classList.add("javascript");
                break;
            case "html":
                listItem.classList.add("html");
                break;
            case "css":
                listItem.classList.add("css");
                break;
            case "json":
                listItem.classList.add("json");
                break;
            case "md":
                listItem.classList.add("markdown");
                break;
            default:
                listItem.classList.add("default");
                break;
        }

        listItem.classList.add("oct")
        myList.appendChild(listItem);
    }

} catch (e) {
    console.log("No files found");
}

function extension(text) {
    const ext = text.split(".")[1];
    return ext;
}

function create_file_label(text) {
    const label = document.createElement("label");
    label.innerText = text;
    label.classList.add("list-group-item");
    label.classList.add("oct");

    return label;
}
