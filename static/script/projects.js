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
