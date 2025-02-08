$(document).ready(function () {
  // Image preview
  $('input[name="ct_scan"]').change(function (event) {
    var file = event.target.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#image-preview").html(`
                <img src="${e.target.result}" class="img-fluid rounded" style="max-height: 200px;">
            `);
    };

    reader.readAsDataURL(file);
  });

  // Form submission
  $("#detection-form").submit(function (e) {
    e.preventDefault();

    var formData = new FormData(this);

    $.ajax({
      url: "/detect",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#result-container").show();
        $("#result-alert")
          .removeClass("alert-success alert-danger")
          .addClass("alert-" + response.result_class);

        $("#result-text").text(response.result);
        $("#recommendation-text").text(
          "Recommendation: " + response.recommendation
        );
        $("#probability-text").text(
          `Probability of Cancer: ${(response.probability * 100).toFixed(2)}%`
        );
      },
      error: function (xhr) {
        var errorMsg = xhr.responseJSON
          ? xhr.responseJSON.error
          : "An unexpected error occurred";
        alert(errorMsg);
      },
    });
  });
});
