chrome.action.onClicked.addListener((tab) => {
    let url = tab.url;
    fetch("http://localhost:5000/run_scraper", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.result);
        });
});
