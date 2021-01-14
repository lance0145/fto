
$(document).ready(function() {

  $(document).on('click', 'input[name="partner_phone"]', function (event) {
    setTimeout(function(){
      $('input[name="partner_phone"]').inputmask("(999)-999-9999", {
        "placeholder": "(000)-000-0000",
        onincomplete: function() {
          $(this).val('');
        }
      });

      $("input[type='text']").click(function () {
         $(this).select();
      });
    }, 500);
  });


  //$("div[name='x_details_identification'] tr a").off();
  //$(document).off('click', 'td div[name="x_identification_id"]');
  $(document).on('click', 'td div[name="x_identification_id"]', function (event) {
      setTimeout(function(){
        //$("input[type='text']").off();
        $("input[type='text']").on("focus",function(){
          if ($(this).val() == "SSS") {
            $(this).closest("tr").find("input[name='x_value']").inputmask("99-9999999-9", {
              "placeholder": "00-0000000-0",
              onincomplete: function() {
                $(this).val('');
              }
            });
          } else if ($(this).val() == "TIN") {
            $(this).closest("tr").find("input[name='x_value']").inputmask("999-999-999", {
              "placeholder": "000-000-000",
              onincomplete: function() {
                $(this).val('');
              }
            });
          } else if ($(this).val() == "PAGIBIG") {
            $(this).closest("tr").find("input[name='x_value']").inputmask("9999-9999-9999", {
                "placeholder": "0000-0000-0000",
                onincomplete: function() {
                  $(this).val('');
                }
              });
          } else if ($(this).val() == "PHILHEALTH") {
            $(this).closest("tr").find("input[name='x_value']").inputmask("99-999999999-9", {
                "placeholder": "00-000000000-0",
                onincomplete: function() {
                  $(this).val('');
                }
              });
          } else if ($(this).val() == "Numero de IMSS") {
            $(this).closest("tr").find("input[name='x_value']").inputmask("99999999999", {
                "placeholder": "00000000000",
                onincomplete: function() {
                  $(this).val('');
                }
              });
          }
        });
       }, 500);
  });

});
