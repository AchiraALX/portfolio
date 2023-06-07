document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const drop_menu = document.querySelector('.drop-menu');
    const menu_btn = document.querySelector('#menu');
    const parent = document.querySelector('#parent')


    drop_menu.style.top = '-100%'
    menu_btn.addEventListener('click', () => {
        if (drop_menu.style.top === '-100%') {
            drop_menu.style.top = '0';
        } else {
            drop_menu.style.top = '-100%'
        }
    });

    if (title() === 'register' || title() === 'home') {
        const parent_form = document.querySelector('#parent-form');
        const parent_form_first = document.querySelector('#parent-form-first');
        const parent_form_second = document.querySelector('#parent-form-second');
        const confirm = document.querySelector('#confirm');
        const right = document.querySelector('#right');
        const left = document.querySelector('#left');

        if (parent_form_second.style.height === "0px") {
            confirm.style.display = "none";
        }

        right.addEventListener('click', () => {
            parent_form_first.style.height = "0px";
            parent_form_second.style.height = "auto";
            confirm.style.display = "block";
        });

        left.addEventListener('click', () => {
            parent_form_first.style.height = "auto";
            parent_form_second.style.height = "0px";
            confirm.style.display = "none";
        });
    }

    if (title() === 'projects') {
        document.querySelector('#repo_form').addEventListener('submit', (e) => {
            e.preventDefault();

            const repo_name = document.querySelector('#repository_name').value;
            const repo_url = "/projects/" + encodeURIComponent(repo_name);
            window.location.href = repo_url;
        });
    }

    if (title() === 'home') {
        const index_blog = document.querySelector('#index-blog');
        const index_heat = document.querySelector('#index-health');

        // Fetch the data
        fetch_data(2, index_blog, index_heat);

    }

    if (title() === '404') {
        parent.style.display = 'none';
    }

    if (title() === 'login') {
        parent.style.backgroundColor = 'transparent';
    }

    if (title() === 'register') {
        parent.style.backgroundColor = 'transparent'
    }

});

function title() {
    return document.title.toLowerCase().split(' ')[0];
}

function fetch_data(num, blog_element, heat_element) {
    // Build the url with the specified number
     fetch(`http://127.0.0.1:5000/index_heat_and_blog?num=${num}`)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            blog_data = data.blogs;
            blog_data.forEach(blog => {
                const div = document.createElement('div');
                style_element(div);
                div.innerHTML = `
                    <h1>${blog.blogTitle}</h1>
                    <p>${blog.blogContent}</p>
                    <a href="/blog/${blog.id}">Read More</a>
                    `
                blog_element.appendChild(div);
            });
            heats_data = data.heats;
            heats_data.forEach(heat => {
                const div = document.createElement('div');
                style_element(div);
                div.classList.add('heat');
                div.innerHTML = `
                    <h1>${heat.title}</h1>
                    <p>${heat.content}</p>
                    <a href="/heat/${heat.id}">Read More</a>
                    `
                heat_element.appendChild(div);
            });
        })
        .catch(error => console.error('Error:', error));

}

function style_element(element) {
    element.classList.add('oct');
    element.classList.add('index-art');
    element.style.width = "100%";
    element.style.padding = "20px";
    element.style.margin = "15px auto";
}

// Scroll offSet