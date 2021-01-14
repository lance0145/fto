$('#wizard').smartWizard('goToStep', 1);
$('.stepContainer').css('height','100%');
$("#wizard").show();

$(".nextStep").click(function(e){
    $(".nextStep").attr('disabled', 'disabled');
    $(".buttonNext").trigger("click");

    setTimeout(function(){
        $(".nextStep").removeAttr('disabled')
    }, 500);
});

$(".previousStep").click(function(e){
    $(".buttonPrevious").trigger("click");
});

$("#application_submit").click(function(e){
    $(".o_website_form_send:eq(0)").trigger("click");
    $(this).attr('disabled','disabled');
});

$("#start_typing").click(function(e){
	$(".typingtestcontainer").show();
	$(".speedtestcontainer").hide();

    var iframe = $("#if1");
    iframe.attr("src", iframe.data("src")); 
})

$("#start_speed").click(function(e){
	$(".speedtestcontainer").show();
	$(".typingtestcontainer").hide();

    var iframe = $("#if2");
    iframe.attr("src", iframe.data("src")); 
})

$("#complete_speed").click(function(e){
    //.has-error .form-control")https://prnt.sc
    //if($("input[name='test_speed_results']").indexOf("https://prnt.sc") === -1)
    if($("input[name='x_test_speed_results']").val() == '') {
        $("input[name='x_test_speed_results']").parent().parent().addClass('has-error');
    } else {
    	$("input[name='x_test_speed_results']").parent().parent().removeClass('has-error');
		$(".speedtestcontainer").hide();
		$(".typingtestcontainer").hide();
		//getSpeedResult();	
    }
})

$("#complete_typing").click(function(e){
	if($("input[name='x_test_type_results']").val() == '') {
        $("input[name='x_test_type_results']").parent().parent().addClass('has-error');
    } else {
    	$("input[name='x_test_type_results']").parent().parent().removeClass('has-error');
		$(".speedtestcontainer").hide();
		$(".typingtestcontainer").hide();
		//getTypingResult()
	}
})

//hide finish button on wizard form
$('.buttonFinish').hide();
$('.actionBar').hide();
$('.wizard_steps').css('padding', '0px');

//disable click event on steps
$(".wizard_steps a").off("click");

//move the basic details form inside the wizard's step 1
$("section#forms").appendTo($("#wizard .stepContainer #step-1"));


$("#validate_basic").click(function(e){
    var errors = false;
    $.each($("#forms").find("input"),function(){
        var attr = $(this).attr('required');
        if (typeof attr !== typeof undefined && attr !== false) {
            if ( $(this).val() == null || typeof $(this).val() == 'undefined' || $(this).val() == ""){
                $(this).addClass('error-validation');
                errors = true;
            } else {
                $(this).removeClass('error-validation');
            }
        }
    });

    var email_pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i;
    var email_input = $("#forms input[name='email_from']").val();
    if(!email_pattern.test(email_input))
    {
        $("#forms input[name='email_from']").addClass('error-validation');
        errors = true;
    } else {
        $("#forms input[name='email_from']").removeClass('error-validation');
    }
    
    if(!errors){
        $(".nextStep").attr('disabled', 'disabled');
        $(".buttonNext").trigger("click");

        setTimeout(function(){
            $(".nextStep").removeAttr('disabled')
        }, 500);
    } else {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    }
})

$("#validate_education").click(function(e){
    var errors = false;
    $.each($("#education_details_content").find("input"),function(){
        var attr = $(this).attr('required');
        if (typeof attr !== typeof undefined && attr !== false) {
            if ( $(this).val() == null || typeof $(this).val() == 'undefined' || $(this).val() == ""){
                $(this).addClass('error-validation');
                errors = true;
            } else {
                $(this).removeClass('error-validation');
            }
        }
    });
    
    if(!errors){
        $(".nextStep").attr('disabled', 'disabled');
        $(".buttonNext").trigger("click");

        setTimeout(function(){
            $(".nextStep").removeAttr('disabled')
        }, 500);
    } else {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
    }
})


$(document).ready(function() {
  //input number only
  $('input[type=number]').on('input blur paste', function(){
   $(this).val($(this).val().replace(/\D/g, ''))
  })

  $("input[name='x_partner_id']").val('');

  $('input[name="partner_phone"]').inputmask("(999)-999-9999", {
    "placeholder": "(000)-000-0000",
    onincomplete: function() {
      $(this).val('');
    }
  });

  $('input[id="SSS"]').inputmask("99-9999999-9", {
    "placeholder": "00-0000000-0",
    onincomplete: function() {
      $(this).val('');
    }
  });

  $('input[id="TIN"]').inputmask("999-999-999", {
    "placeholder": "000-000-000",
    onincomplete: function() {
      $(this).val('');
    }
  });

  $('input[id="PAGIBIG"]').inputmask("9999-9999-9999", {
    "placeholder": "0000-0000-0000",
    onincomplete: function() {
      $(this).val('');
    }
  });

  $('input[id="PHILHEALTH"]').inputmask("99-999999999-9", {
    "placeholder": "00-000000000-0",
    onincomplete: function() {
      $(this).val('');
    }
  });

  $('input[id="Numero de IMSS"]').inputmask("99999999999", {
    "placeholder": "00000000000",
    onincomplete: function() {
      $(this).val('');
    }
  });

  $("input[type='text']").click(function () {
     $(this).select();
  });
});