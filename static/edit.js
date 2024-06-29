$("#edit-form").submit(e => {
    e.preventDefault()
    let formData = new FormData(e.target)

    fetch("/edit", {
        method: "POST",
        body: formData
    }).then(
        response => response.json()
    ).then(
        json => {
            if (json.status === "success") {
                window.alert("編輯成功！")
                e.target.reset()
            } else {
                window.alert("編輯失敗！")
            }
        }
    )
})
