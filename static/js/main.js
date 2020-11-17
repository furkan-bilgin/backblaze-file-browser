$(document).ready(() => {
    console.log("cool");
    $("#uploadFile").change(function() {
        var formData = new FormData();
        formData.append("file", this.files[0]);
        formData.append("directory", $("#directoryName").val());
        
        $("#files").append($("#fileUploadProgressTemplate").tmpl());
        $("#fileUploadError").addClass("hide");
        
        $.ajax({
            url: "/upload",
            type: "POST",
            xhr: function() {
                var xhr = $.ajaxSettings.xhr();
                if (xhr.upload) {
                    xhr.upload.addEventListener("progress", function(evt) {
                        var percent = (evt.loaded / evt.total) * 100;
                        $("#files").find(".progress-bar").width(percent + "%");
                    }, false);
                }
                return xhr;
            },
            success: function(data) {
                $("#files").children().last().remove();
                $("#uploadFile").closest("form").trigger("reset");

                alert("Upload successful.");
                window.location.reload();
            },
            error: function() {
                $("#fileUploadError").removeClass("hide").text("An error occured!");
                $("#files").children().last().remove();
                $("#uploadFile").closest("form").trigger("reset");
            },
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        }, "json");
    });
})