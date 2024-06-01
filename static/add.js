let animationDots = 1
const original = "正在下載資料中"
let str = original + "."

$("#add-form").submit(e => {
    e.preventDefault()
    $("#status").removeClass("text-success")
    $("#status").removeClass("text-danger")
    $("#status").addClass("text-primary")
    $("#status").text("")
    const formData = new FormData(e.target)
    sendAddRequest(formData)
})


async function sendAddRequest(formData) {
    const intervalId = setInterval(loopDownloadAnimation, 1000);

    const response = await fetch("/add", {
        method: "POST",
        body: formData
    });

    const result = await response.json()
    clearInterval(intervalId)
    if (result.status === "success") {
        $("#status").text("下載成功！")
        $("#status").removeClass("text-primary")
        $("#status").addClass("text-success")
    } else {
        console.log(result)
        $("#status").text("下載失敗！")
        $("#status").removeClass("text-primary")
        $("#status").addClass("text-danger")
    }
}


const loopDownloadAnimation = () => {
    
    if(animationDots == 3) {
        str = original + "."
        animationDots = 1
    } else {
        str += "."
        animationDots++
    }
    $("#status").text(str)
}
