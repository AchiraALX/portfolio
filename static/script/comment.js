const blogParent = document.getElementsByClassName('blog-parent')
const heatParent = document.getElementsByClassName('health_article')
const blogs = document.getElementsByClassName('obj-id');
const comment_container = document.getElementsByClassName('comments-div')
const send_button = document.querySelector('#comm-btn')
const comment_for = document.querySelector('#comment_for')
const date_time = document.getElementsByClassName('date-time')
const idInput = document.querySelector('#id-value')

// Take existing innerText of date_time and convert to date
// and display it in a readable format
for (let i = 0; i < date_time.length; i++) {
    const element = date_time[i];
    const date = new Date(element.innerText)
    element.innerText = date.toDateString()

    element.parentElement.parentElement.style.textDecoration = "none";
    element.style.color = "rebeccapurple";
    element.style.fontWeight = "800";
    element.style.fontSize = "70%";

    // Margin 15px and padding 5px
    element.style.margin = '15px'
    element.style.padding = '5px'


}

const docTitle = document.title.toLowerCase().split(' ')[0];
if (docTitle === 'blogs') {
    const blog_comment = document.getElementsByClassName('comment-parent');
    const idValues = document.getElementsByClassName('id-value');

    for (let i = 0; i < blog_comment.length; i++) {
        const element = blog_comment[i];

        element.addEventListener('click', (event) => {
            if (event.target == element) {
                element.style.height = '0';
                element.style.bottom = '-110%'
            }
        })
    }

    for (let i = 0; i < blogs.length; i++) {
        let element = blogs[i];

        const id = parseInt(element.innerText)
        element.innerText = "Comments";

        element.addEventListener('click', () => {
            blog_comment[i].style.bottom = '0';
            blog_comment[i].style.height = '100%'
            blog_comment[i].style.paddingTop = '8%'
            for (let i = 0; i < blogs.length; i++) {
                if (blogs[i] !== element) {
                    blogs[i].style.display = 'none'
                }
            }

            const active_container = comment_container[i]

            active_container.innerHTML = '<h2 class="comment-title"> Available Reactions </h2> <br>'

            // Get the comment data
            blog_comments(id, active_container)

            const idValue = idValues[i]
            idValue.value = id
        });
    }

    for (let i = 0; i < blogParent.length; i++) {
        blogs[i].style.display = 'none'

        blogParent[i].addEventListener('click', (event) => {
            if (event.target == blogParent[i]) {
                if (blogs[i].style.display === 'none') {
                    blogs[i].style.display = 'block';
                } else {
                    blogs[i].style.display = 'none';
                }
            }
        })
    }
}

if (docTitle === 'wellness') {
    const art_comments = document.getElementsByClassName('comment-parent')
    for (let i = 0; i < art_comments.length; i++) {
        const element = art_comments[i];

        element.addEventListener('click', (event) => {
            if (event.target == element) {
                element.style.height = '0';
                element.style.bottom = '-110%'
            }
        })
    }

    for (let i = 0; i < blogs.length; i++) {
        let element = blogs[i];

        const id = parseInt(element.innerText)
        element.innerText = "Comments";

        element.addEventListener('click', () => {
            art_comments[i].style.bottom = '0';
            art_comments[i].style.height = '100%'
            art_comments[i].style.paddingTop = '8%'
            for (let i = 0; i < blogs.length; i++) {
                if (blogs[i] !== element) {
                    blogs[i].style.display = 'none'
                }
            }

            const active_container = comment_container[i]

            active_container.innerHTML = '<h2 class="comment-title"> Available Reactions </h2> <br>'
            // Get the comment data
            fetch(`http://localhost:5000/article_comments?id=${id}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    if (data.length <= 0) {
                        active_container.innerHTML = '<h2 class="o-comment"> No comments yet </h2>'
                    } else {
                        for (let i = 0; i < data.length; i++) {
                            const element = data[i];
                            const comment = document.createElement('div')
                            comment.classList.add('commented')
                            comment.classList.add('oct')
                            comment.innerHTML = `
                                <div class="comment-content oct">
                                <p>${element.comment}</p>
                                </div>
                            `
                            active_container.appendChild(comment)
                        }
                    }
                });

            const idValue = document.querySelector('#id-value')
            idValue.value = id
        });
    }

    for (let i = 0; i < heatParent.length; i++) {
        let element = heatParent[i];
        blogs[i].style.display = 'none'

        element.addEventListener('click', (event) => {
            if (event.target == element) {
                if (blogs[i].style.display === 'none') {
                    blogs[i].style.display = 'block';
                } else {
                    blogs[i].style.display = 'none';
                }
            }
        });
    }

}

function blog_comments(id, active_container) {
    fetch(`http://localhost:5000/blog_comments?id=${id}`)
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.length <= 0) {
                active_container.innerHTML = '<h2 class="o-comment"> No comments yet </h2>'
            } else {
                for (let i = 0; i < data.length; i++) {
                    const element = data[i];
                    const comment = document.createElement('div')
                    comment.classList.add('commented')
                    comment.classList.add('oct')
                    comment.innerHTML = `
                                    <div class="comment-content oct">
                                        <p>${element.comment}</p>
                                    </div>
                                `
                    active_container.appendChild(comment)
                }
            }
        });
}