document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#repo_form').addEventListener('submit', (e) => {
        e.preventDefault();

        const repo_name = document.querySelector('#repository_name').value;
        const repo_url = "/projects/" + encodeURIComponent(repo_name);
        window.location.href = repo_url;
    });
});

// Scroll offSet