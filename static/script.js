async function predict() {

    let fileInput = document.getElementById("imageInput");
    let modelType = document.getElementById("model_type").value;

    let formData = new FormData();
    formData.append("image", fileInput.files[0]);
    formData.append("model_type", modelType);

    let response = await fetch("/predict", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    document.getElementById("resultBox").innerHTML =
        "<h3>Result:</h3><p>" + data.result + "</p>";
}