setInterval(() => {
    next()
}, 5000);

dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
        console.log(currentSlide)
        init(i)
        currentSlide = i
    })
})

    }, time);
}