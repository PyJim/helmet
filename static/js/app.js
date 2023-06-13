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

