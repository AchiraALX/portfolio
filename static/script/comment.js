const blogParent = document.getElementsByClassName('blog-parent')
const heatParent = document.getElementsByClassName('health_article')
const blogs = document.getElementsByClassName('obj-id');
const comment_parent = document.querySelector('.comment-parent')
const comment_container = document.querySelector('.comments-div')
const send_button = document.querySelector('#comm-btn')
const comment_for = document.querySelector('#comment_for')
const date_time = document.getElementsByClassName('date-time')

// Take existing innerText of date_time and convert to date
// and display it in a readable format
for (let i = 0; i < date_time.length; i++) {
    const element = date_time[i];
    const date = new Date(element.innerText)
    element.innerText = date.toDateString()

    // Style it absolute to the right-top
    element.style.position = 'absolute'
    element.style.right = '0'
    element.style.top = '0'

    // Add oct class to it
    element.classList.add('oct')

    // Margin 15px and padding 5px
    element.style.margin = '15px'
    element.style.padding = '5px'


}

comment_parent.addEventListener('click', (event) => {
    if (event.target == comment_parent) {
        comment_parent.style.height = '0';
        comment_parent.style.bottom = '-100%'
    }
})

const docTitle = document.title.toLowerCase().split(' ')[0];
if (docTitle === 'blogs') {
    for (let i = 0; i < blogs.length; i++) {
        let element = blogs[i];

        const id = parseInt(element.innerText)
        element.innerText = "Comments";

        element.addEventListener('click', () => {
            comment_parent.style.bottom = '0';
            comment_parent.style.height = '100%'
            comment_parent.style.paddingTop = '8%'
            for (let i = 0; i < blogs.length; i++) {
                if (blogs[i] !== element) {
                    blogs[i].style.display = 'none'
                }
            }

            comment_container.innerHTML = '<h2 class="comment-title"> Available Reactions </h2> <br>'

            // Get the comment data
            fetch(`http://localhost:5000/blog_comments?id=${id}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    if (data.length <= 0) {
                        comment_container.innerHTML = '<h2 class="o-comment"> No comments yet </h2>'
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
                            comment_container.appendChild(comment)
                        }
                    }
                });

            const idValue = document.querySelector('#id-value')
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
    for (let i = 0; i < heatParent.length; i++) {
        let element = heatParent[i];

        element.addEventListener('click', () => {
            alert("You need to be logged in to comment")
        });
    }

}

function get_blog_id(id) {
    return id
}