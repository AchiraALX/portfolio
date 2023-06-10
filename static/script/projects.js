/* Script for the projects template */

const theParent = document.querySelector('.project-form')
const selectRepo = document.querySelector('#select-repo');
const projectForm = document.querySelector('.project-form');
const caughtUp = document.querySelectorAll('.caught-up');

// Add an event listener to .title to redirect to previous page
const myTitle = document.querySelector(".title");
myTitle.style.cursor = "pointer";
myTitle.addEventListener("click", () => {
    window.location.href = "/projects";
});


// Hide the caught up message if caughtUp is not null
if (caughtUp.length === 1) {
    caughtUp.forEach((message) => {
        message.addEventListener('click', () => {
            projectForm.style.bottom = "0%";
        });
    });
}

projectForm.addEventListener('click', (event)=>{
    if (event.target == projectForm) {
        projectForm.style.bottom = "-200%";
    }
});

// Check if the url ends with projects
if (window.location.href.endsWith("projects")) {
    const repoName = document.querySelectorAll('.repo-name');
    const viewRepo = document.querySelector('#view-repo');
    repoName.forEach((repo) => {
        repo.parentElement.addEventListener('click', () => {
            // redirect to the repo page
            const repo_url = "/projects?" + encodeURIComponent(repo.innerText);
            window.location.href = repo_url;
        });
    });

    try {
        viewRepo.addEventListener('click', () => {
            projectForm.style.bottom = "0px";
        });
    } catch (e) {}
}

const myForm = document.querySelector('#repo_form');

myForm.addEventListener('submit', (e) => {
    e.preventDefault();
    myForm.submit();
    projectForm.style.bottom = "-200%";
});

try {
    const myList = document.querySelector("#files");

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

// Confirm the the url does not end with projects
if (!window.location.href.endsWith("projects") && caughtUp.length === 0) {
    const markedText = document.querySelector("#repo-readme").innerText;
    const htmlText = convert_markdown(markedText);
    document.querySelector("#repo-readme").innerHTML = htmlText;

    alert(htmlText)
};

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

// Convert the markDown to HTML using showdown
function convert_markdown(text) {
    const converter = new showdown.Converter();
    const html = converter.makeHtml(text);
    return html;
}
