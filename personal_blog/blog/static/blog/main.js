document.addEventListener('DOMContentLoaded', () => {

    // Use navigation to toggle between views
    document.querySelector('#allPosts').addEventListener('click', load_all_posts);

    //By default, show all posts
    load_all_posts();

});

function load_all_posts() {

    // clear everything firt
    document.querySelector('#all-posts').replaceChildren();

    // show all posts div and hide the others
    document.querySelector('#all-posts').style.display = 'block';
    document.querySelector('#selected-post').style.display = 'none';

    // show div name
    document.querySelector('#all-posts').innerHTML = `<h1>All Posts</h1>`;

    // fetch all posts
    fetch('/graphql/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query: `
                    {
                        allPosts {
                            id
                            title
                            status
                            publishedDate
                            author {
                                username
                            }
                        }
                    }
                    `
        }),
    })
        .then(response => response.json())
        .then(posts => {
            console.log(posts);

            const data = posts['data']['allPosts'];

            for (p in data) {

                const status = data[p]['status'];

                if (status === true) {
                    const post_id = data[p]['id'];
                    const title = data[p]['title'];
                    const author = data[p]['author']['username'];

                    const pDate = new Date(data[p]['publishedDate']);

                    // display created emails
                    let div = document.createElement('div');

                    div.innerHTML = `
                        <p><a href="#">${title}</a> - ${pDate.toLocaleString()} (${author})</p>
                        `

                    document.getElementById('all-posts').appendChild(div);

                    div.addEventListener('click', () => {

                        // fetch selected post
                        fetch('/graphql/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json',
                            },
                            body: JSON.stringify({
                                query: `
                                    {
                                        postByKey (postKey: ${post_id}) {
                                            title
                                            body
                                            publishedDate
                                            author {
                                                username
                                            }
                                        }
                                    }
                                    `
                            }),
                        })
                            .then(response => response.json())
                            .then(post => {
                                console.log(post);

                                // show div, hide the others
                                document.querySelector('#all-posts').style.display = 'none';
                                const selected_div = document.querySelector('#selected-post');

                                // create style objects
                                const styles = {
                                    display: 'flex',
                                    flexDirection: 'column',
                                };

                                Object.assign(selected_div.style, styles);

                                const dt = post['data']['postByKey'];

                                const titl = dt['title'];
                                const auth = dt['author']['username'];
                                const p_dt = new Date(dt['publishedDate']);
                                const body = dt['body'];

                                // set title
                                document.querySelector('#selected-post').innerHTML =
                                    `<h3 class="post-title">${titl}</h3>`
                                    + `<p class="post-author">Author: ${auth}</p>`
                                    + `<p class="post-date">Publication Date: ${p_dt.toLocaleString()}</p>`
                                    + `<p class="post-body">${body}</p>`
                                    ;

                            })
                    });

                }

            }

        })
}