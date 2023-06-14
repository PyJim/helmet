const faqs = document.querySelectorAll(".faq");

faqs.forEach(faq => {
    faq.addEventListener("click", () =>{
        faq.classList.toggle("active");
    })
})

const nav_links = document.querySelectorAll(".navlinks");

nav_links.forEach(link => {

    link.addEventListener("click", function(){
        nav_links.forEach(link =>{
        link.classList.remove("active");
    });

        this.classList.add("active");
    });
});

const create_new_post = document.getElementById("create_new_post");
create_new_post.addEventListener("click", function(){
    let create_post = document.getElementById("create_post");
    create_post.classList.toggle("active");
});

const create_new_event = document.getElementById("create_new_event");
create_new_event.addEventListener("click", function(){
    let create_event = document.getElementById("create_event");
    create_event.classList.toggle("active");
});

const submit_button = document.getElementById("submit-button");
submit_button.addEventListener("click", function(){
    let create_post = document.getElementById("create_post");
    create_post.classList.remove("active");
    let create_event = document.getElementById("create_event");
    create_event.classList.remove("active");
});